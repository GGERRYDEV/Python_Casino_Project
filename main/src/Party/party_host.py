import socket
import threading

players = {}
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind(('0.0.0.0', 5555))

servidor.listen()
print("Waiting for players...")
start = False
def wait_for_players():
    while start == False:
        conexion, direccion = servidor.accept()
        print(f"Someone connected from {direccion}")
        mensaje_recibido = conexion.recv(1024).decode('utf-8')
        print(f"Player: {mensaje_recibido}")
        players[conexion] = {"name": mensaje_recibido, "money": 5000}
        print(players)

    conexion.close()
def start_game():
    global start
    while True:
        print("Type Start to start the game")
        start_host = input()
        if start_host.lower() == "start":
            start = True
        else:
            print("Invalid input. Please type 'Start' to start the game.")

threading.Thread(target=wait_for_players, args=()).start()
threading.Thread(target=start_game, args=()).start()