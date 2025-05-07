import socket
import threading

PORT = 60000
BUFFER_SIZE = 1024
clientes = []
clientes_lock = threading.Lock()

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
    except:
        pass
    finally:
        conn.close()
        with clientes_lock:
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

        # Enviar a todos los clientes conectados
        with clientes_lock:
            for c in clientes:
                try:
                    c.send(f"Servidor: {mensaje}".encode())
                except:
                    pass

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('', PORT))
    servidor.listen(5)
    print(f"Servidor escuchando en el puerto {PORT}...")

    hilo_aceptar = threading.Thread(target=aceptar_conexiones, args=(servidor,), daemon=True)
    hilo_aceptar.start()

    enviar_desde_servidor()
    servidor.close()

if __name__ == "__main__":
    main()