import unittest
import time
import struct
from unittest import mock
from CBObject import CBObject, CBObjectFactory
from CBlockChain import CBlockChain

class CBlockChainTestCase(unittest.TestCase):
    filename = 'test_file_two.dat'
    content = ['The quick brown fox jumps over the lazy dog.', 'Another day, another 50 cents.', "All's well that ends well", 'Four score and seven years ago...']
    zero_digest = bytes(32)

    def setUp(self):
        self.block_chain = CBlockChain()
        self.factory = CBObjectFactory()

    def tearDown(self):
        del self.block_chain
        del self.factory

    def test_saveToFile(self):
        num_contents = len(self.content)
        for i in range(num_contents):
            self.createBlock(self.content[i])

        block_count = self.block_chain.saveToFile(self.filename)
        self.assertEqual(block_count, num_contents, 'Incorrect block count')

    def test_loadFromFile(self):
        blocks_loaded = self.block_chain.loadFromFile(self.filename)
        for i in range(blocks_loaded):
            content = self.block_chain.getBlockContent(i)
            content_string = content.decode('utf-8')
            self.assertEqual(self.content[i], content_string, 'Wrong content loaded')

    def test_walkChain(self):
        # Load the block chain
        blocks_loaded = self.block_chain.loadFromFile(self.filename)
        self.assertTrue(blocks_loaded > 0, "No blocks loaded!")
        # start with the top

        print()
        print("Full block chain:")

        digest = self.block_chain.getLastBlockDigest()
        while digest != self.zero_digest:
            block = self.block_chain.getBlockWithDigest(digest)
            content = block.getContent()
            print("digest: ", hash)
            print("content: ", content.decode('UTF-8'))
            digest = block.getPreviousBlockHash()

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