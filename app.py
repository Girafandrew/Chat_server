from flask import Flask, render_template, request, jsonify, make_response
from flask_socketio import SocketIO, join_room, leave_room, emit
from datetime import datetime
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['DEBUG'] = True
socketio = SocketIO(app, async_mode='eventlet', logger=True, engineio_logger=True)

# URL do servidor reserva
reserve_server_url = 'http://localhost:5001'

# Lista para armazenar as mensagens do chat
messages = []

# Rota inicial do chat
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

    # Enviar a mensagem para o servidor reserva, se estiver ativo
    try:
        requests.post(f"{reserve_server_url}/add_message", json={'message': formatted_message})
    except requests.exceptions.RequestException:
        print("Error: Failed to connect to the reserve server")

    socketio.emit('new_message', formatted_message, namespace='/chat')
    return ''

# Rota para obter as mensagens atualizadas em formato JSON
@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

# Função para iniciar o servidor web
def start_server():
    socketio.run(app, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Iniciar o servidor principal
    start_server()