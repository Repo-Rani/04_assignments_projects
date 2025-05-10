import socket

HOST = '127.0.0.1'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    data = client.recv(1024).decode()
    if "Enter your move" in data:
        move = input(data)
        client.send(move.encode())
    else:
        print(data)