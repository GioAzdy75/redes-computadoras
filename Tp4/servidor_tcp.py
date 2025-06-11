import socket
import threading
import os

HOST = "0.0.0.0"
PORT = 60000
BUFFER_SIZE = 1024
clientes = []
clientes_lock = threading.Lock()

def enviar_archivo():
    nombre_archivo = input("Ingrese el nombre del archivo a enviar: ")

    if not os.path.exists(nombre_archivo):
        print("El archivo no existe. Cancelando.")
        with clientes_lock:
            for c in clientes:
                try:
                    c.sendall(b"ERROR: Archivo no encontrado.")
                except:
                    pass
        return

    with clientes_lock:
        for c in clientes:
            try:
                # Enviar nombre del archivo
                c.sendall(f"NOMBRE_ARCHIVO:{nombre_archivo}".encode())
            except:
                continue

        with open(nombre_archivo, "rb") as f:
            while (datos := f.read(BUFFER_SIZE)):
                for c in clientes:
                    try:
                        c.sendall(datos)
                    except:
                        pass

    print("Archivo enviado exitosamente.")

def manejar_cliente(conn, addr):
    print(f" + Cliente conectado desde {addr}")
    with clientes_lock:
        clientes.append(conn)

    try:
        while True:
            datos = conn.recv(BUFFER_SIZE).decode()
            if not datos:
                break
            if datos.strip().lower() == "exit":
                print(f" - Cliente {addr} se desconectó.")
                break
            print(f"Cliente ({addr[0]}): {datos}")
    except Exception as e:
        print(f"Error con cliente {addr}: {e}")
    finally:
        conn.close()
        with clientes_lock:
            if conn in clientes:
                clientes.remove(conn)

def aceptar_conexiones(servidor):
    while True:
        conn, addr = servidor.accept()
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo_cliente.start()

def enviar_desde_servidor():
    while True:
        mensaje = input()
        if mensaje.strip().lower() == "exit":
            with clientes_lock:
                if len(clientes) > 0:
                    print("No es posible cerrar el proceso servidor si hay un cliente conectado.")
                    continue
                else:
                    print("Cerrando el servidor...")
                    break

        elif mensaje.startswith("enviar_archivo"):
            enviar_archivo()
        else:
            with clientes_lock:
                for c in clientes:
                    try:
                        c.send(f"Servidor: {mensaje}".encode())
                    except:
                        pass

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(5)
    print(f"Servidor escuchando en el puerto {PORT}...")

    hilo_aceptar = threading.Thread(target=aceptar_conexiones, args=(servidor,), daemon=True)
    hilo_aceptar.start()

    enviar_desde_servidor()
    servidor.close()

if __name__ == "__main__":
    main()
