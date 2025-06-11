# cliente_tcp.py
import socket

SERVIDOR = '10.65.4.119'  # Cambiar si se conecta a otra PC
PUERTO = 12344

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((SERVIDOR, PUERTO))
        print("Conectado al servidor.")

        nombre_archivo = cliente.recv(1024).decode()

        if nombre_archivo == "ERROR":
            print("El servidor no encontró el archivo.")
            return

        with open(nombre_archivo, "wb") as f:
            while True:
                datos = cliente.recv(1024)
                if not datos:
                    break
                f.write(datos)

        print(f"Archivo '{nombre_archivo}' recibido y guardado como 'archivo_recibido_{nombre_archivo}'")

if __name__ == "__main__":
    main()
