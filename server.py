## importar a biblioteca para usar socket e biblioteca select para administrar varias conexões
import select
import socket

HEARDER_SIZE = 10
IP = "127.0.0.1"
PORT = 4200

##Criação dos sockets 
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

socket_server.bind((IP, PORT))
socket_server.listen()

## Uma lista de clientes em forma de socket, atribuido ao server pois quando os clientes se conectarem estarao ali
socket_list = [socket_server]

clients = {}


##Funcao basica para receber mensagem
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEARDER_SIZE)
        if not len(message_header):
            return False  ##Fecha a conexão se não receber nada 

        message_len = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_len)}
    except:
        return False  ##Fecha a conexão


while True:
    read_sockets, _, exception_sockets = select.select(
        socket_list, [], socket_list) ## De onde conseguimos os dados

    ##Cliente conectou e vamos gerenciar essa conexao
    for notified_socket in read_sockets:
        if notified_socket == socket_server:
            client_socket, client_address = socket_server.accept()

            user = receive_message(client_socket) ##Recebe da funcao anterior basica que criamos
            if user is False: ##Cliente desconectou
                continue

            socket_list.append(client_socket) ##adiocina na lista o cliente
            clients[client_socket] = user #adiciona as infomacoes do cliente na lista de cliente

            ##Mostra na tela que aceitou a conexão de um novo cliente
            print(
                f"Nova conexão de: {client_address[0]}:{client_address[1]} usuario:{user['data'].decode('utf-8')}")
        else:
            message = receive_message(notified_socket)

            ##Caso de algum erro prepara uma mensagem de erro e fala que conexão finalizada e tira o cliente da lista
            if message is False:
                print(
                    f"Conexao fechada de: {clients[notified_socket]['data'].decode('utef-8')}")
                socket_list.remove(notified_socket) ##retira o cliente da lista
                del clients[notified_socket]
                continue

            user = clients[notified_socket] 
            ##Mostra na tela de quem recebeu a mensagem
            print(
                f"Nova mensagem de: {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(
                        user['header'] + user['data'] + message['header'] + message['data']) ##manda os dados do cliente e sua mensagem separadas
            ##Remove da lista o cliente
    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket) 
        del clients[notified_socket]
