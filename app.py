from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
socketio = SocketIO(app)

# Lista para armazenar as mensagens
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    username = request.args.get('username')
    return render_template('chat.html', username=username)

@socketio.on('send_message')
def handle_send_message_event(data):
    messages.append(data)
    emit('receive_message', data, broadcast=True)

@socketio.on('connect')
def handle_connect_event():
    emit('load_messages', messages)

def start_server():
    socketio.run(app, host='0.0.0.0', port=9000)

if __name__ == '__main__':
    start_server()
