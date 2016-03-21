import unittest
import time
import struct
from unittest import mock
from CBObject import CBObject, CBObjectFactory
from CBlockChain import CBlockChain

class CBlockChainTestCase(unittest.TestCase):
    filename = 'test_file_one.dat'
    blocks_loaded = 0

    def setUp(self):
        self.block_chain = CBlockChain()

    def tearDown(self):
        self.block_chain = 0

    def test_loadFromFile(self):
        print('filename: ', self.filename)
        self.blocks_loaded = self.block_chain.loadFromFile(self.filename)
        print('loaded ', self.blocks_loaded, ' blocks')

        content = self.block_chain.getBlockContent(0)
        print('Content in hex: ', content.hex())
        content_string = content.decode('utf-8')
        print('Content as string: ', content_string)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(CBlockChainTestCase('test_loadFromFile'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
