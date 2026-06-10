import socket
import time

HOST = '10.7.70.209'
PORT = 50007

count = 0

print("=== CLIENTE TCP ECO ===")
print(f"Conectando a {HOST}:{PORT}...")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(">>Enviando solicitud de eco<<")
        while True:
            count += 1
            msg = f"Pedido de eco #{count}"
            start_time = time.perf_counter()
            s.sendall(msg.encode("utf-8"))
            data = s.recv(1024).decode("utf-8")
            elapsed = time.perf_counter() - start_time
            print(f"Respuesta: {repr(data)} - Latencia: {elapsed * 1000:.3f} ms")
            time.sleep(5)
except Exception as e:
    print(f"Error de conexión: {e}")
