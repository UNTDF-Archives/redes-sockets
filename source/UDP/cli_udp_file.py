import socket
import sys
import time

HOST = '10.7.70.209'
PORT = 9090
FILENAME = "Libro.pdf"
CHUNK_SIZE = 4096

print("=== CLIENTE UDP ===")

# 1. Autenticación
username = input("Usuario: ").strip()
password = input("Contraseña: ").strip()

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enviar credenciales
credenciales = f"{username}:{password}"
client.sendto(credenciales.encode(), (HOST, PORT))
response, _ = client.recvfrom(1024)
if response == b"AUTH_OK":
    print("Autenticación exitosa.")
else:
    print("Error: Credenciales incorrectas")
    client.close()
    sys.exit(0)

# 2. Selector de Modo de Transmisión
print("\nSeleccione modo de transmisión:")
print("1. Modo con ACK ")
print("2. Modo sin ACK ")
opcion = input("Opción (1 o 2): ").strip()
mode = "SIN_ACK" if opcion == "2" else "CON_ACK"

# Enviar modo elegido
client.sendto(mode.encode(), (HOST, PORT))

# 3. Enviar Nombre del Archivo
client.sendto(FILENAME.encode(), (HOST, PORT))
client.recvfrom(1024) # Esperar ACK_NAME

# 4. Transmisión del Archivo y Medición de Tiempos
print(f"Transmitiendo {FILENAME} en modo {mode}...")

# Iniciar cronómetro antes de enviar el primer fragmento
start_time = time.perf_counter()
chunk_num = 1

with open(FILENAME, "rb") as f:
    while True:
        data = f.read(CHUNK_SIZE)
        if not data:
            break
        
        client.sendto(data, (HOST, PORT))
        print(f"Fragmento {chunk_num} enviado.")
        
        if mode == "CON_ACK":
            # Esperar b"ACK"
            while True:
                ack, _ = client.recvfrom(1024)
                if ack == b"ACK":
                    print(f"ACK recibido para fragmento {chunk_num}.")
                    break
            
        chunk_num += 1

# Enviar marcador de finalización "DONE"
client.sendto(b"DONE", (HOST, PORT))
client.recvfrom(1024) # Esperar ACK_DONE

# Detener cronómetro inmediatamente después de DONE
end_time = time.perf_counter()
elapsed_ms = (end_time - start_time) * 1000

print(f"\nTiempo total transcurrido: {elapsed_ms:.3f} ms")
client.close()
print("Cliente cerrado.")
