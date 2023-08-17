import socket
import threading
import time


class WorkersState:
    idle = 0
    work = 1
    crash = 2


class Worker:
    thread: threading.Thread
    conn: socket.socket
    addr: tuple[str, int]
    log: bool

    def __init__(self, conn: socket.socket, addr: tuple[str, int], log: bool):
        self.conn = conn
        self.addr = addr
        self.log = log
        self.thread = threading.Thread(target=self.answer, daemon=True)

    def answer(self):
        with self.conn:
            data = self.conn.recv(1024)
            time.sleep(int(data) / 1000)
            self.conn.sendall(data)
        if self.log:
            print(f'Ответил на {self.addr}')

    def start(self):
        self.thread.start()

    def wait(self):
        self.thread.join()

    def __repr__(self):
        return f"Worker({self.thread.ident})"


class Manager:
    log: bool
    running: bool
    mx: int

    def __init__(self, log=False):
        self.log = log
        self.pool = None
        self.running = False

    def run(self, host: str = '127.0.0.1', port: int = 50010):
        self.running = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            print(f'Started оn {host}:{port}')

            try:
                while self.running:
                    s.listen()
                    conn, addr = s.accept()
                    if self.log:
                        print(f'Подключено к {addr}')
                    Worker(conn, addr, self.log).start()

            except BaseException as e:
                print('Waiting all for stop')
                raise e


man = Manager()
man.run()
