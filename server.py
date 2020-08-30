import select
import socket

HEARDER_SIZE = 10
IP = "127.0.0.1"
PORT = 4200

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

socket_server.bind((IP, PORT))
socket_server.listen()

socket_list = [socket_server]

clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEARDER_SIZE)
        if not len(message_header):
            return False

        message_len = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_len)}
    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(
        socket_list, [], socket_list)

    for notified_socket in read_sockets:
        if notified_socket == socket_server:
            client_socket, client_address = socket_server.accept()

            user = receive_message(client_socket)
            if user is False:
                continue

            socket_list.append(client_socket)
            clients[client_socket] = user

            print(
                f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
        else:
            message = receive_message(notified_socket)

            if message is False:
                print(
                    f"closed connection from {clients[notified_socket]['data'].decode('utef-8')}")
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(
                f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(
                        user['header'] + user['data'] + message['header'] + message['data'])
    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]
