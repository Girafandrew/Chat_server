from flask import Flask, render_template, request, jsonify, make_response
from flask_socketio import SocketIO
from datetime import datetime
import requests
import multiprocessing
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['DEBUG'] = True
socketio = SocketIO(app, async_mode='eventlet', logger=True, engineio_logger=True)

# Lista para armazenar as mensagens do chat
messages = []

# Rota para adicionar uma mensagem à lista de mensagens
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return 'Username is required.', 400
        resp = make_response(render_template('chat.html', username=username))
        resp.set_cookie('username', username)
        return resp
    username = request.cookies.get('username')
    if not username:
        return render_template('index.html')
    return render_template('chat.html', username=username)


# Rota para receber as mensagens do formulário e adicioná-las à lista de mensagens
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    username = request.cookies.get('username')
    if not username:
        return 'Username not found.', 400
    if not message:
        return 'Message is required.', 400
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"{now} - {username}: {message}"
    messages.append(formatted_message)
    socketio.emit('new_message', formatted_message, namespace='/chat')
    return ''

# Rota para obter as mensagens atualizadas em formato JSON
@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

# Função para verificar se o servidor principal está ativo
def check_primary_server():
    while True:
        try:
            response = requests.get('http://localhost:5000/')
            if response.status_code == 200:
                print('Primary server is active')
                sync_messages_from_primary()
        except requests.exceptions.RequestException:
            print('Primary server is down')
            # Iniciar o servidor reserva na mesma porta do servidor principal
            socketio.run(app, host='0.0.0.0', port=5000)
            break

# Função para sincronizar as mensagens do servidor principal
def sync_messages_from_primary():
    try:
        response = requests.get('http://localhost:5000/get_messages')
        if response.status_code == 200:
            global messages
            messages = response.json()
            print('Messages synchronized with primary server')
    except requests.exceptions.RequestException:
        print('Failed to sync messages with primary server')

# Inicia o servidor reserva e verifica o status do servidor principal
if __name__ == '__main__':
    # Iniciar a verificação do servidor principal em segundo plano
    check_primary_server_process = multiprocessing.Process(target=check_primary_server)
    check_primary_server_process.start()

    # Iniciar o servidor reserva
    socketio.run(app, host='0.0.0.0', port=5001)
