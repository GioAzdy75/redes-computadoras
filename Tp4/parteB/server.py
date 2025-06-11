# servidor_tcp.py
import socket
import os

HOST = '0.0.0.0'   # Acepta conexiones desde cualquier IP
PUERTO = 1500

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((HOST, PUERTO))
        servidor.listen(1)
        print(f"Servidor esperando conexiones en el puerto {PUERTO}...")

        conn, addr = servidor.accept()
        print(f"Conexión establecida con {addr}")

        nombre_archivo = input("Ingrese el nombre del archivo a enviar: ")

        if not os.path.exists(nombre_archivo):
            print("El archivo no existe. Cancelando.")
            conn.sendall(b"ERROR")
            return

        conn.sendall(nombre_archivo.encode())
        with open(nombre_archivo, "rb") as f:
            while (datos := f.read(1024)):
                conn.sendall(datos)

        print("Archivo enviado exitosamente.")
        conn.close()

if __name__ == "__main__":
    main()
