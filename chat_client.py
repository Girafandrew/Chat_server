import socket
import threading

# Função para lidar com as mensagens recebidas do servidor
def receive_messages(client_socket):
    while True:
        try:
            # Recebe a mensagem do servidor
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(f"Erro ao receber mensagem do servidor: {str(e)}")
            break

# Função para enviar mensagens para o servidor
def send_message(client_socket):
    while True:
        # Solicita ao usuário que digite uma mensagem
        message = input()

        try:
            # Envia a mensagem para o servidor
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Erro ao enviar mensagem para o servidor: {str(e)}")
            break

# Função para iniciar o cliente
def start_client():
    # Configurações do servidor
    host = 'localhost'  # Endereço IP do servidor
    port = 5555  # Porta do servidor

    # Cria um socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta-se ao servidor
        client_socket.connect((host, port))
        print(f"Conectado ao servidor {host}:{port}")

        # Inicia uma thread para receber mensagens do servidor
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        # Inicia uma thread para enviar mensagens para o servidor
        send_thread = threading.Thread(target=send_message, args=(client_socket,))
        send_thread.start()
    except Exception as e:
        print(f"Erro ao conectar-se ao servidor: {str(e)}")
        client_socket.close()

# Inicia o cliente
start_client()
