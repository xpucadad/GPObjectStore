import unittest
import time
import struct
from unittest import mock
from CBObject import CBObject, CBObjectFactory
from CBlockChain import CBlockChain

class CBlockChainTestCase(unittest.TestCase):
    filename = 'test_file_two.dat'
    content = ['The quick brown fox jumps over the lazy dog.', 'Another day, another 50 cents.']

    def setUp(self):
        self.block_chain = CBlockChain()
        self.factory = CBObjectFactory()

    def tearDown(self):
        del self.block_chain
        del self.factory

    def test_saveToFile(self):
        self.createBlock(self.content[0])
        self.createBlock(self.content[1])
        block_count = self.block_chain.saveToFile(self.filename)
        self.assertEqual(block_count, 2, 'Incorrect block count')

    def test_loadFromFile(self):
        blocks_loaded = self.block_chain.loadFromFile(self.filename)
        for i in range(0, blocks_loaded):
            content = self.block_chain.getBlockContent(i)
#            print('Block ', i, ':\n')
#            print('\tContent in hex: ', content.hex())
            content_string = content.decode('utf-8')
#            print('\tContent as string: ', content_string)
            self.assertEqual(self.content[i], content_string, 'Wrong content loaded')

    def createBlock(self, text):
        content = text.encode()
        block_object = self.factory.createNew(content)
        pbhd = self.block_chain.getLastBlockDigest()
        block_object.farm(pbhd)
        height = self.block_chain.addBlock(block_object)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(CBlockChainTestCase('test_saveToFile'))
    suite.addTest(CBlockChainTestCase('test_loadFromFile'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
