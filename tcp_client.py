import random
import socket
import threading
import time

HOST = 'localhost'
PORT = 50010


def send_request():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall("10".encode())
        data = s.recv(1024)
    # print('Received', repr(data))


nums = 5
N = 100


def test():
    reqs = []
    for _ in range(nums):
        req = threading.Thread(target=send_request, daemon=True)
        reqs.append(req)

    start = time.time()
    for i in reqs:
        i.start()

    for i in reqs:
        i.join()
    end = time.time()
    print(f"Всего времени: {end - start}, RPC: {round(nums / (end - start))}")

    return end - start


times = []
for i in range(N):
    times.append(test())

print(f"Средний RPC: {round((nums * N) / sum(times))}")
