def request():
    return True


class WorkersState:
    idle = 0
    work = 1
    crash = 2


class Worker:
    worker_id: int
    state: int
    tasks: list

    def __init__(self, worker_id: int):
        self.worker_id = worker_id
        self.state = WorkersState.idle
        self.tasks = []

    def __repr__(self):
        return f"Worker({self.worker_id})"

    def add_task(self, task):
        self.state = WorkersState.work
        self.tasks.append(task)

        try:
            res = ''  # Выполнение task
        except Exception as e:
            self.tasks.pop()
            self.state = WorkersState.crash
            raise e
        else:
            self.tasks.pop()
            self.state = WorkersState.idle

        return res


class RequestManager:
    workers: list[Worker]

    def __init__(self, workers: int = 1):
        workers_list = []
        for i in range(workers):
            workers_list.append(Worker(i))
        self.workers = workers_list

    def create_worker(self) -> Worker:
        new_id = len(self.workers)
        new_worker = Worker(new_id)
        self.workers.append(new_worker)

        return new_worker

    def run(self):
        while True:
            if request():
                for worker in self.workers:
                    if worker.state == WorkersState.idle:
                        worker.add_task(request())
                        break


man = RequestManager()
print(man.workers)

man.create_worker()
print(man.workers)
man.create_worker()
print(man.workers)
man.create_worker()
print(man.workers)
