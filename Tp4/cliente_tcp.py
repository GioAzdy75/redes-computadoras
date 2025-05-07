import socket
import threading

BUFFER_SIZE = 1024

ip_servidor = input("Ingrese IP del servidor: ")
PUERTO = 60000

def recibir(sock):
    while True:
        try:
            datos = sock.recv(BUFFER_SIZE).decode()
            if datos:
                print(datos)
        except:
            break


#Inicio Programa

if __name__ == "__main__":
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((ip_servidor, PUERTO))
    print("Conectado al servidor.")

    hilo_receptor = threading.Thread(target=recibir, args=(cliente,), daemon=True)
    hilo_receptor.start()

    while True:
        mensaje = input()
        cliente.send(mensaje.encode())
        if mensaje.strip().lower() == "exit":
            break

    cliente.close()
