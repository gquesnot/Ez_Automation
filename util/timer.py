from time import time, sleep


def waitFewSec(sec):
    """
    Wait few seconds.
    """
    while sec > 0:
        print(f'\rWaiting {sec}s', end='')
        sec -= 1
        sleep(1)
    print('\r', end='')


class Time:
    start_ = 0
    end_ = 0

    def __init__(self):
        self.start_ = time()

    def end(self):
        self.end_ = time()


class Timer:
    results = []

    def __init__(self):
        self.reset()

    def start(self, e):
        if e not in self.results:
            self.results[e] = []
        self.results[e].append(Time())

    def stop(self, e):
        for elem in self.results[e]:
            if elem.end_ == 0:
                elem.end()
                return

    def printElem(self, toFind):
        print(toFind, ":")
        for elem in self.results[toFind]:
            print(" -", str(elem.end_ - elem.start_))

    def reset(self):
        self.results = []
