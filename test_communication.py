import unittest
import threading
import queue

from ContentProcessing import ContentSender
from ContentProcessing import ContentReciever

#import time
#import struct
#from unittest import mock
#from CBObject import CBObject, CBObjectFactory
#from CBlockChain import CBlockChain

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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(SendRecieveTestCase('test_01'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
