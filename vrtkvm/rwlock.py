from time import time
from threading import Condition, Lock, currentThread


class ReadWriteLock(object):
    def __init__(self):
        self.__condition = Condition(Lock())

        self.__writer = None
        self.__upgradewritercount = 0
        self.__pendingwriters = []

        self.__readers = {}


    def acquireRead(self,timeout=None):

        global endtime
        if timeout is not None:
            endtime = time() + timeout
        me = currentThread()

        self.__condition.acquire()

        try:
            if self.__writer is me:

                self.__writercount += 1
                return
            while True:
                if self.__writer is None:

                    if self.__upgradewritercount or self.__pendingwriters:
                        if me in self.__readers:
                            self.__readers[me] += 1
                            return
                    else:

                        self.__readers[me] = self.__readers.get(me,0) + 1
                        return
                if timeout is not None:
                    remaining = endtime - time()

                    if remaining <= 0:
                        raise RuntimeError("Acquiring read lock timed out")
                    self.__condition.wait(remaining)
        finally:
            self.__condition.release()

    def acquireWrite(self,timeout=None):

        global endtime
        if timeout is not None:
            endtime = time() + timeout

        me,upgradewriter = currentThread(),False
        self.__condition.acquire()

        try:
            if self.__writer is me:
                self.__writercount += 1
                return

            elif me in self.__readers:

                if self.__upgradewritercount:

                    raise  ValueError(
                        " Inevitable dead lock,denying write lock"
                    )
                upgradewriter = True

                self.__upgradewritercount = self.__readers.pop(me)
            else:

                self.__pendingwriters.append(me)
            while True:
                if not self.__readers and self.__writer is None:

                    if self.__upgradewritercount:
                    # upgrade write lock
                        if self.__upgradewritercount:
                            self.__writer = me
                            self.__writercount = self.__upgradewritercount + 1
                            self.__upgradewritercount = 0
                            return

                    elif self.__pendingwriters[0] is me:

                        self.__writer = me
                        self.__writercount = 1
                        self.__pendingwriters = self.__pendingwriters[1:]
                        return
                    if timeout is not None:
                        remaining = endtime - time()
                        if remaining <= 0:
                            if upgradewriter:
                                self.__readers[me] = self.__upgradewritercount
                                self.__upgradewritercount = 0
                            else:

                                self.__pendingwriters.remove(me)
                            raise  RuntimeError("Acquiring write lock timed out")
                        self.__condition.wait(remaining)
                    else:
                        self.__condition.wait()
        finally:
            self.__condition.release()



    def release(self):
        me = currentThread()
        self.__condition.acquire()
        try:
            if self.__writer is me:

                self.__writercount -= 1
                if not self.__writercount:

                    self.__writer = None
                    self.__condition.notifyAll()
                elif me in self.__readers:

                    self.__readers[me] -= 1
                    if not self.__readers[me]:
                        #no more read locks

                        del self.__readers[me]

                        if not self.__readers:

                            self.__condition.notifyAll()
                else:
                    raise ValueError("Trying to release unheld lock")
        finally:
            self.__condition.release()