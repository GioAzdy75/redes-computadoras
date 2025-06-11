import socket
import threading
import os

BUFFER_SIZE = 1024

ip_servidor = input("Ingrese IP del servidor: ")
PUERTO = 60000

def recibir(sock):
    while True:
        try:
            datos = sock.recv(BUFFER_SIZE)
            if not datos:
                print("Conexión cerrada por el servidor.")
                break

            # Detectamos si es inicio de envío de archivo
            try:
                texto = datos.decode()
                if texto.startswith("NOMBRE_ARCHIVO:"):
                    nombre_archivo = texto.split(":", 1)[1]
                    print(f"Recibiendo archivo: {nombre_archivo}")

                    with open("descarga_" + os.path.basename(nombre_archivo), "wb") as f:
                        while True:
                            datos_archivo = sock.recv(BUFFER_SIZE)
                            # Heurística: si recibimos algo no binario, asumimos que terminó (se puede mejorar)
                            try:
                                if datos_archivo.decode().startswith("Servidor:") or datos_archivo.decode().startswith("NOMBRE_ARCHIVO:"):
                                    print("Archivo recibido completamente.")
                                    print(datos_archivo.decode())
                                    break
                            except:
                                pass
                            if not datos_archivo:
                                break
                            f.write(datos_archivo)
                    continue
                else:
                    print(texto)
            except UnicodeDecodeError:
                # Datos binarios que no son texto, los ignoramos por ahora
                pass

        except Exception as e:
            print("Error al recibir datos:", e)
            break

# Inicio del programa principal
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
