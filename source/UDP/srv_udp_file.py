import socket
import sys
import time

HOST = '10.7.70.209'
PORT = 9090
CHUNK_SIZE = 4096

CREDENTIALS = {
    "admin": "admin123",
    "lucas": "redes2026",
}

print("=== SERVIDOR UDP ===")
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))
print(f"Escuchando en {HOST}:{PORT}...")

# 1. Autenticación Básica
packet, client_addr = server.recvfrom(1024)
credenciales = packet.decode().split(":")
if len(credenciales) == 2:
    user, password = credenciales
    if CREDENTIALS.get(user) == password:
        print(f"Usuario '{user}' autenticado con éxito.")
        server.sendto(b"AUTH_OK", client_addr)
    else:
        print("Autenticación fallida.")
        server.sendto(b"AUTH_FAIL", client_addr)
        server.close()
        sys.exit(0)
else:
    server.sendto(b"AUTH_FAIL", client_addr)
    server.close()
    sys.exit(0)

# 2. Selección de Modo de Transmisión
packet, _ = server.recvfrom(1024)
mode = packet.decode()
print(f"Modo de transmisión: {mode}")

# 3. Recibir Nombre del Archivo
packet, _ = server.recvfrom(1024)
filename = packet.decode()
print(f"Archivo a recibir: {filename}")
server.sendto(b"ACK_NAME", client_addr)

# 4. Transferencia de Datos y Medición de Tiempos
start_time = None
end_time = None
partes_recibidas = 0

with open(f"recibido_{filename}", "wb") as f:
    while True:
        packet, _ = server.recvfrom(CHUNK_SIZE + 64)
        
        # Iniciar cronómetro antes del primer fragmento
        if start_time is None:
            start_time = time.perf_counter()
            
        if packet == b"DONE":
            # Detener cronómetro inmediatamente después del DONE
            end_time = time.perf_counter()
            server.sendto(b"ACK_DONE", client_addr)
            break
            
        f.write(packet)
        partes_recibidas += 1
        print(f"Fragmento {partes_recibidas} recibido.")
        
        if mode == "CON_ACK":
            server.sendto(b"ACK", client_addr)
            print(f"ACK enviado para fragmento {partes_recibidas}.")

# Impresión del tiempo total transcurrido
elapsed_ms = (end_time - start_time) * 1000
print(f"\nTiempo total transcurrido: {elapsed_ms:.3f} ms")

server.close()
print("Servidor cerrado.")
