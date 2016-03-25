import logging
import queue
import threading
import time
import unittest

from contentprocessing import ProcessContent

class ProcessContentTestCase(unittest.TestCase):
    def setUp(self):
        logging.info('setUp')

    def tearDown(self):
        logging.info('tearDown')

    def test_01(self):
        logging.info('Start test_01')
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
        logging.info('End test_01')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(ProcessContentTestCase('test_01'))
    return suite

if __name__ == '__main__':
    logging.basicConfig(
        filename='test_contentprocessing.log',
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s - %(threadName)s - %(message)s'
    )

    logging.info('Log Started')
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)

    logging.info('Log Ended')
