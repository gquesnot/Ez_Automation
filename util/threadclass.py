from abc import abstractmethod
from threading import Thread, Lock


class ThreadClass:
    def __init__(self):
        self.lock = Lock()
        self.stopped = False
        self.started = False

    def start(self):
        self.stopped = False
        self.started = True
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True
        self.started = False

    def isStarted(self):
        return self.started

    @abstractmethod
    def run(self):
        pass
