import errno
import select
import socket
import sys

# Informacoes do servidor ao qual se conectar e deve ser o mesmmo do server.py
HEARDER_SIZE = 10
IP = "127.0.0.1"
PORT = 4200

# Recebe o nome do usuario
my_user = input("Usuario: ")

# Criando socket para comunicacao
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.connect((IP, PORT))
socket_tcp.setblocking(False)

# Criando os status do usario
username = my_user.encode('utf-8')
username_header = f'{len(username):<{HEARDER_SIZE}}'.encode('utf-8')
socket_tcp.send(username_header + username)

# criar loop para receber e mandar mensagens

while True:
    #Enquanto a pessoa digita aparece o nome dela e que ela está digitando
    message = input(f'{my_user} > ')

    #Enviando a mensagem
    if message:
        message = message.encode('utf-8')
        message_header = f'{len(message) :< {HEARDER_SIZE}}'.encode('utf-8')
        socket_tcp.send(message_header + message)
    try:
        while True:
            # Para receber a mensagens
            username_header = socket_tcp.recv(HEARDER_SIZE)
            if not len(username_header): #Nao receber nenhum dado
                print('conexao fechada')
                sys.exit() #fecha a conexao com o servidor

            # Para receber os dados do cliente
            username_length = int(username_header.decode('utf-8').strip())
            username = socket_tcp.recv(username_length).decode('utf-8')

            # Para receber a mensagem
            message_header = socket_tcp.recv(HEARDER_SIZE)
            message_length = int(message_header.decode('utf-8').strip())
            message = socket_tcp.recv(message_length).decode('utf-8')

            # Depois de receber os dados e mensagens, imprimimos 
            print(f'{username} > {message}')

    # Tratar erros nas mensagens

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Lendo erro', str(e))

        continue

    except Exception as e:
        print('Erro geral', str(e))
        sys.exit()
