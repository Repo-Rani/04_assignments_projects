import socket

HOST = '127.0.0.1'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)

print("Waiting for players to connect...")
player1, addr1 = server.accept()
print("Player 1 connected from", addr1)

player2, addr2 = server.accept()
print("Player 2 connected from", addr2)

def get_choice(player):
    player.send(b"Enter your move (rock/paper/scissors): ")
    return player.recv(1024).decode().strip().lower()

def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return "Draw"
    elif (choice1 == "rock" and choice2 == "scissors") or \
         (choice1 == "scissors" and choice2 == "paper") or \
         (choice1 == "paper" and choice2 == "rock"):
        return "Player 1 wins!"
    else:
        return "Player 2 wins!"

while True:
    choice1 = get_choice(player1)
    choice2 = get_choice(player2)

    result = determine_winner(choice1, choice2)

    player1.send(f"Player 2 chose: {choice2}\n{result}\n".encode())
    player2.send(f"Player 1 chose: {choice1}\n{result}\n".encode())