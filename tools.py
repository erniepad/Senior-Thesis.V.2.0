# author: Jimmy Gonzalez Nunez
# date: 27 Oct, 2020
from random import choice
import os

def SetDir(dirName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    return dirName

def ProgressBar(it, total, prefix="", decimals=2, length=30, fill="█"):
    """
    Call in a loop to create terminal progress bar
    @params:
        it          - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        decimals    - Optional  : positive number of decimals in percent
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (it / float(total)))
    filledLength = int(length * it // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print(f"{prefix} |{bar}| {percent}%", end="\r")
    if it == total:
        print(flush=True)


class FArray:
    def __init__(self):
        self.arr = []
        self.hashd = {}

    def insert(self, x):
        if x in self.hashd:
            return False
        s = len(self.arr)
        self.arr.append(x)
        self.hashd[x] = s
        if len(self.arr) != len(self.hashd):
            raise ValueError("arr not equal to hashd")
        return True

    def remove(self, x):
        if len(self.arr) != len(self.hashd):
            raise ValueError("arr not equal to hashd")
        ind = self.hashd.get(x, None)
        if ind is None:  # changed == to is
            return
        s = len(self.arr)
        last = self.arr[s - 1]
        self.arr[ind], self.arr[s - 1] = self.arr[s - 1], self.arr[ind]
        self.hashd[last] = ind  # place before del!
        del self.hashd[x]
        del self.arr[-1]

    def size(self):
        return len(self.arr)

    def clear(self):
        self.arr.clear()
        self.hashd.clear()

    def random(self):
        if len(self.arr) == 0:
            return None
        return choice(self.arr)
