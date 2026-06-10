import socket
import sys

HOST = '10.7.70.209'
PORT = 50007

print("=== SERVIDOR TCP ECO ===")
print(f"Enlazando en {HOST}:{PORT}...")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print("Servidor ECO TCP esperando conexión...")
        conn, addr = s.accept()
        with conn:
            print("Conectado con:", addr)
            while True:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    print("Conexión finalizada por el cliente.")
                    break
                print("Pedido de eco:", data)
                conn.sendall(data.encode("utf-8"))
except Exception as e:
    print(f"Error en el servidor: {e}")
