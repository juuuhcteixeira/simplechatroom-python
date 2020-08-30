import socket

HEARDER_SIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 4200))

while True:

    full_msg = ''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print(f"new message length: {msg[:HEARDER_SIZE]}")
            msgLen = int(msg[:HEARDER_SIZE])
            new_msg = False

        full_msg += msg.decode("utf-8")

        if len(full_msg)-HEARDER_SIZE == msgLen:
            print('full msg received')
            print(full_msg[HEARDER_SIZE:])
            new_msg = True
            full_msg = ''

    print(full_msg)
