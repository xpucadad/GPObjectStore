import logging
import logging.config
import queue
import struct
import test_utils
import threading
import time
import unittest

from blocks import Block
from blockchain import BlockChain
from contentprocessing import ProcessContent

class ProcessContentTestCase(unittest.TestCase):
    filename = 'test_contentprocessing.dat'

    def setUp(self):
        self.blockchain = BlockChain()
        self.content_queue = queue.Queue()
        self.block_queue = queue.Queue()
        logging.debug('setUp')

    def tearDown(self):
        del self.block_queue
        del self.content_queue
        del self.blockchain
        logging.debug('tearDown')

    def test_01(self):
        logging.debug('Start test_01')
        kwargs = {}
        kwargs['content_queue'] = self.content_queue
        kwargs['block_queue'] = self.block_queue
        kwargs['blockchain' ] = self.blockchain

        pct = ProcessContent(name='ProcessContentThread', kwargs=kwargs)

        pct.start()
        # For checking purposes, each content should be unique
        input_content = (b'abc', b'def', b'Love is in the air!')
        for i in input_content:
            self.content_queue.put(i)

        self.content_queue.put(None)
        pct.join()

        # Now get all the generated blocks
        received_content = {}
        while True:
            raw_block = self.block_queue.get()
            if (raw_block is None):
                break
            # The block was queued as raw bytes; reconstruct it
            block = Block()
            block.parseFromBytes(raw_block)
            self.assertTrue(block.validateHeaderDigest(), 'Bad header digest')
            logging.debug(block.toBytes().hex())
            block_content = block.getContent()
            received_content[block_content] = True
            logging.info(block_content)
            self.block_queue.task_done()

        # Verify that there is one block with content for
        # each content input.
        for c in input_content:
            print(c)
            self.assertTrue(c in received_content, 'No block generated for ' + c.decode('utf-8'))

        logging.debug('End test_01')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(ProcessContentTestCase('test_01'))
    return suite

if __name__ == '__main__':
    test_utils.setup_logging('test_contentprocessing.log')

    logging.info('Log started in file test_contentprocessing.log')

    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)

    logging.info('Log ended')
