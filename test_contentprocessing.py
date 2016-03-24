import unittest
import threading
import time
import queue

from contentprocessing import ProcessContent

class ProcessContentTestCase(unittest.TestCase):
    def setUp(self): pass
    def tearDown(self): pass

    def test_01(self):
        content_queue = queue.Queue()
        kwargs = {}
        kwargs['content_queue'] = content_queue

        t1 = ProcessContent(name='t1', kwargs=kwargs)

        t1.start()
        content = (b'abc', b'def', b'Love is in the air!')
        for i in content:
            content_queue.put(i)

        content_queue.put(None)
        t1.join()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(ProcessContentTestCase('test_01'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
