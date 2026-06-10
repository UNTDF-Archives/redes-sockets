import socket

HOST = '10.7.70.178' 
PORT = 50007         # Puerto no privilegiado
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Servidor ECO TCP esperando conexión...")
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Conectado con: ', addr)
        input("Servidor pausado. Enter para continuar...")

        while True:
            data = conn.recv(1024).decode("utf-8")
            print("Pedido de eco:", data)
            if not data:
                print("Break")
                break
            conn.send(data.encode("utf-8"))
