import socket
import threading
import sys

PORT = 60000
BUFFER_SIZE = 1024
BROADCAST_IP = "192.168.100.255"



nombre_usuario = input("Ingrese su nombre de usuario: ")

mensaje_bienvenida = f"{nombre_usuario}:nuevo"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

sock.bind(('',PORT))


def recibir_mensajes():
    while True:
        datos, addr = sock.recvfrom(BUFFER_SIZE)
        mensaje = datos.decode('utf-8')
        usuario, texto = mensaje.split(":", 1)

        if texto == "exit":
            print(f"El usuario {usuario} ({addr[0]}) ha abandonado la conversación")
        elif texto == "nuevo":
            print(f"El usuario {usuario} se ha unido a la conversación")
        else:
            print(f"{usuario} ({addr[0]}) dice: {texto}")


def enviar_mensajes():
    sock.sendto(mensaje_bienvenida.encode('utf-8'), (BROADCAST_IP, PORT))

    while True:
        texto = input()
        mensaje = f"{nombre_usuario}:{texto}"
        sock.sendto(mensaje.encode('utf-8'), (BROADCAST_IP, PORT))

        if texto == "exit":
            break


hilo_recv = threading.Thread(target=recibir_mensajes, daemon=True)
hilo_recv.start()

enviar_mensajes()