import logging
import logging.config
import queue
import threading
import time
import unittest

import test_utils

from contentprocessing import ProcessContent

class ProcessContentTestCase(unittest.TestCase):
    def setUp(self):
        logging.debug('setUp')

    def tearDown(self):
        logging.debug('tearDown')

    def test_01(self):
        logging.info('Start test_01')
        content_queue = queue.Queue()
        kwargs = {}
        kwargs['content_queue'] = content_queue

        pct = ProcessContent(name='ProcessContentThread', kwargs=kwargs)

        pct.start()
        content = (b'abc', b'def', b'Love is in the air!')
        for i in content:
            content_queue.put(i)

        content_queue.put(None)
        pct.join()
        logging.info('End test_01')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(ProcessContentTestCase('test_01'))
    return suite

if __name__ == '__main__':
    test_utils.setup_logging('test_contentprocessing.log')

    logging.debug('Log Started')

    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)

    logging.debug('Log Ended')
