import socket
import threading
import time

players = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 5555))
server.listen()

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) 
        mi_ip = s.getsockname()[0] 
        s.close()
        return mi_ip
    except Exception:
        return "127.0.0.1"

def waiting():
    ip = get_ip()
    print(f"Your IP is: {ip}")
    message = "What's your name?"
    print("How many players are going to play?")
    max_number_players = int(input())
    number_players = 0
    while number_players != max_number_players:
        print("Waiting for players...")
        conexion, address = server.accept()
        conexion.send(message.encode('utf-8'))
        received_message = conexion.recv(1024).decode('utf-8')
        print(received_message)
        players[conexion] = {"name": received_message, "money": 5000, "conexion": conexion}
        number_players += 1
        print(f"{received_message} connected")
        threading.Thread(target=chat, args=(conexion,)).start()
    print("All the players connected, starting the game")
    
def chat(conexion):
    while True:
        try:
            received_message = conexion.recv(1024).decode('utf-8')
            message = f"{players[conexion]['name']}: {received_message}"
            print(message)
            client_conexion = conexion
            for conexion in players:
                if conexion != client_conexion:
                    conexion.send(message.encode('utf-8'))
            conexion = client_conexion
        except:
            break

threading.Thread(target=waiting, args=()).start()