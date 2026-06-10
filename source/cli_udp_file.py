import socket
import os

HOST = '10.7.70.178'
PORT = 9090
FILENAME = "Libro.pdf"
CHUNK_SIZE = 4096

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if not os.path.exists(FILENAME):
    print("El archivo no existe.")
    exit()

# 1. Enviar nombre del archivo primero
client.sendto(FILENAME.encode(), (HOST, PORT))
ack, _ = client.recvfrom(1024)
print(f"Nombre enviado. Confirmación del servidor: {ack.decode()}")

# 2. Leer y enviar el archivo por partes
with open(FILENAME, "rb") as f:
    data = f.read(CHUNK_SIZE)
    num_parte = 1
    while data:
        print(f"Enviando parte {num_parte}...")
        client.sendto(data, (HOST, PORT))
        
        # Esperar confirmación de la parte enviada
        ack, _ = client.recvfrom(1024)
        print(f"Parte {num_parte} confirmada por el servidor: {ack.decode()}")
        
        num_parte += 1
        data = f.read(CHUNK_SIZE)

# 3. Enviar marcador de finalización
client.sendto(b"DONE", (HOST, PORT))
ack, _ = client.recvfrom(1024)
print(f"Finalización confirmada por el servidor: {ack.decode()}")

client.close()