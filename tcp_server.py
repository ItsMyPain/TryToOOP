import socket
import threading
import time


def answer(conn: socket.socket, addr: tuple[str, int]):
    with conn:
        data = conn.recv(1024)
        time.sleep(int(data) / 1000)
        conn.sendall(data)


HOST = '127.0.0.1'
PORT = 50010
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        threading.Thread(target=answer, args=s.accept(), daemon=True).start()
