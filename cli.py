import errno
import select
import socket
import sys

# Informacoes do servidor ao qual se conectar
HEARDER_SIZE = 10
IP = "127.0.0.1"
PORT = 4200

my_user = input("User: ")

# Criando socket para comunicacao
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.connect((IP, PORT))
socket_tcp.setblocking(False)

username = my_user.encode('utf-8')
username_header = f'{len(username):<{HEARDER_SIZE}}'.encode('utf-8')
socket_tcp.send(username_header + username)

while True:
    message = input(f'{my_user} > ')
    # message = ""

    if message:
        message = message.encode('utf-8')
        message_header = f'{len(message) :< {HEARDER_SIZE}}'.encode('utf-8')
        socket_tcp.send(message_header + message)
    try:
        while True:
            # receive msg
            username_header = socket_tcp.recv(HEARDER_SIZE)
            if not len(username_header):
                print('connection closed by the server')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = socket_tcp.recv(username_length).decode('utf-8')

            message_header = socket_tcp.recv(HEARDER_SIZE)
            message_length = int(message_header.decode('utf-8').strip())
            message = socket_tcp.recv(message_length).decode('utf-8')
            print(f'{username} > {message}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('REading error', str(e))

        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()
