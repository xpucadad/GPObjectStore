import threading
import time
import queue

class ContentSender():
    def __init__(self, q):
        self.outgoing = q

    def send(self, content):
        self.outgoing.put(content)

class ContentReciever(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        super().__init__(group=group, target=target, name=name)
        self.name = name
        self.incoming = kwargs['incoming']
        self.log = kwargs['log']

    def run(self):
        while True:
            item = self.incoming.get()
            self.log.put(item)
            if item is None:
                break
            time.sleep(5)
            self.incoming.task_done()
