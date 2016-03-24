import unittest
import threading
import time
import queue

class SendRecieveTestCase(unittest.TestCase):
    def setUp(self): pass
    def tearDown(self): pass

    def test_01(self):
        q = queue.Queue()
        log = queue.Queue()
        s = ContentSender(q)
        kwargs = {}
        kwargs['incoming'] = q
        kwargs['log'] = log
        r1 = ContentReciever(name='r1', kwargs=kwargs)
        r2 = ContentReciever(name='r2', kwargs=kwargs)

        r1.start()
        r2.start()
        content = (b'abc', b'def', b'Love is in the air!')
        for i in content:
            s.send(i)
        s.send(None)
        s.send(None)
        print()

        received = {}
        while True:
            item = log.get()
            if item is None:
                break
            print('Got item: ', item)
            received[item] = True
            log.task_done()

        r1.join()
        r2.join()

        for item in content:
            self.assertTrue(item in received)

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
            time.sleep(2)
            self.incoming.task_done()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(SendRecieveTestCase('test_01'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
