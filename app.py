from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    timestamp = datetime.now()
    emit('message', {'username': username, 'message': message, 'timestamp': timestamp}, broadcast=True)

def start_server():
    socketio.run(app, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    start_server()
