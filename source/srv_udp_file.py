import socket

HOST = '10.7.70.178'
PORT = 9090
CHUNK_SIZE = 4096  # Tamaño de cada chunk de datos

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))
print("Servidor listo para recibir archivos...")

# 1. Recibir nombre del archivo
data, addr = server.recvfrom(1024)
filename = data.decode().strip()
print(f"Recibiendo archivo: {filename} desde {addr}")
server.sendto(b"ACK_NAME", addr)  # Confirmar nombre recibido

# 2. Abrir archivo para escritura binaria
with open(f"recibido_{filename}", "wb") as f:
    partes_recibidas = 0
    while True:
        # Recibir pedazo del archivo
        packet, addr = server.recvfrom(CHUNK_SIZE)

        # Usamos un marcador de fin (EOF) enviado por el cliente
        if packet == b"DONE":
            server.sendto(b"ACK_DONE", addr)  # Confirmar fin de transmisión
            break

        f.write(packet)
        
        partes_recibidas += 1
        if partes_recibidas >= 4:
            print("Simulando caída del servidor: Deteniendo antes de enviar ACK_4...")
            break

        print(f"Fragmento {partes_recibidas} recibido. Enviando ACK...")
        server.sendto(f"ACK_{partes_recibidas}".encode(), addr)  # Confirmar fragmento

print(f"Archivo recibido parcialmente ({partes_recibidas} partes). Cerrando servidor.")
server.close()