import socket
import threading
import time
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("What's your friend ip?")
ip = input()
client.connect((ip, 5555))

question = client.recv(1024).decode('utf-8')
name = input(f"{question}\n")
client.send(name.encode('utf-8'))

def receive_message():
    while True:
        try:
            receive_message = client.recv(1024).decode('utf-8')
            print("\r" + " " * 50 + "\r", end="")
            print(receive_message)
            print("You: ", end="", flush=True)
        except:
            break

def send_messages():
    while True:
        try:
            message = input()
            client.send(message.encode('utf-8'))
            print("You: ", end="", flush=True)
        except:
            break

threading.Thread(target=receive_message, args=()).start()
threading.Thread(target=send_messages, args=()).start()