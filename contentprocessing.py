import logging
import queue
import threading

class ProcessContent(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        # Call parent's __init__
        super().__init__(group=group, target=target, name=name)

        # Save the thread name and keyword arguments
        self.name = name
        self.content_queue = kwargs['content_queue']

    def run(self):
        logging.debug('ProcessContent thread starting')

        while True:
            msg = self.content_queue.get()
            if msg is None: break
            logging.debug(msg)
            self.content_queue.task_done()

        logging.debug('ProcessContent thread ending')
