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
    zero_digest = bytes(32)

    def setUp(self):
        self.block_chain = BlockChain()
        self.content_queue = queue.Queue()
        logging.debug('setUp')

    def tearDown(self):
        logging.debug('tearDown')
        del self.content_queue
        del self.block_chain

    def test_01(self):
        logging.debug('Start test_01')
        kwargs = {}
        kwargs['content_queue'] = self.content_queue
        kwargs['block_chain' ] = self.block_chain

        pct = ProcessContent(name='ProcessContentThread', kwargs=kwargs)

        pct.start()
        # For checking purposes, each content should be unique
        input_content = (b'abc', b'def', b'Love is in the air!')
        for i in input_content:
            self.content_queue.put(i)

        self.content_queue.put(None)
        self.content_queue.join()
        pct.join()

        # Now check the created block chain
        received_content = {}
        digest = self.block_chain.getLastBlockDigest()
        while digest != self.zero_digest:
            block = self.block_chain.getBlockWithDigest(digest)
            raw_content = block.getContent()
            received_content[raw_content] = True
            logging.info(raw_content)
            digest = block.getPreviousBlockHash()

        # Verify that there is one block with content for
        # each content input.
        for c in input_content:
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
