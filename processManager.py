import multiprocessing as mp
import uuid
import time

class ProcessManager():
    def __init__(self):
        self.__processes = {}
        self.__requestQ = mp.Queue(32767)
        self.__dataQ = mp.Queue(32767)

    def __del__(self):
        pass

    def main(self):
        pass

# end ProcessManager
        
if __name__ == '__main__':
    newMaster = ProcessManager()
    newMaster.main()