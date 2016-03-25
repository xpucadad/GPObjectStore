import logging
import queue
import threading

class ProcessContent(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        super().__init__(group=group, target=target, name=name)
        self.name = name
        self.content_queue = kwargs['content_queue']

    def run(self):
        print("ProcessContent thread")
        logging.info('ProcessContent thread starting')
        while True:
            msg = self.content_queue.get()
            if msg is None: break
            logging.info(msg)
            print(msg)
            self.content_queue.task_done()
        logging.info('ProcessContent thread ending')
