import socket
import threading

# Função para lidar com as mensagens recebidas do cliente
def handle_client(client_socket, address):
    while True:
        # Recebe a mensagem do cliente
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            # Se a mensagem estiver vazia, o cliente encerrou a conexão
            print(f'{address} fechou a conexão.')
            break
        else:
            # Imprime a mensagem recebida
            print(f'Mensagem de {address}: {message}')
            # Aqui você pode adicionar a lógica do chat, processar a mensagem e enviar uma resposta

    # Fecha o socket do cliente
    client_socket.close()

# Função para iniciar o servidor
def start_server():
    # Configurações do servidor
    host = '0.0.0.0'  # Define o IP do servidor
    port = 5555  # Define a porta do servidor

    # Cria um socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Define a opção SO_REUSEADDR para permitir a reutilização do endereço
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Vincula o socket ao endereço e porta definidos
    server_socket.bind((host, port))
    # Coloca o socket no modo de escuta
    server_socket.listen()

    print(f'Servidor iniciado em {host}:{port}')

    while True:
        # Aguarda a conexão do cliente
        client_socket, address = server_socket.accept()
        print(f'Conexão estabelecida com {address}')

        # Cria uma nova thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

# Inicia o servidor
start_server()
