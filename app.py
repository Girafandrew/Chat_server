from flask import Flask, render_template, request, jsonify, make_response
from flask_socketio import SocketIO
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
socketio = SocketIO(app)

# Lista para armazenar as mensagens do chat
messages = []

# Rota inicial do chat
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
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
    message = request.form['message']
    username = request.cookies.get('username')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"{now} - {username}: {message}"
    messages.append(formatted_message)
    socketio.emit('new_message', formatted_message)
    return ''

# Rota para obter as mensagens atualizadas em formato JSON
@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

# Função para iniciar o servidor web
def start_server():
    socketio.run(app)

# Inicia o servidor web
if __name__ == '__main__':
    start_server()
