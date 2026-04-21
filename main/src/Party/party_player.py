import socket


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("What's your name?")
name = input()
cliente.connect(('127.0.0.1', 5555))

mi_mensaje = name
cliente.send(mi_mensaje.encode('utf-8'))
while True:
    message = input("Type your message: ")
    cliente.send(message.encode('utf-8'))

cliente.close()