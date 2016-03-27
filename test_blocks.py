import logging
import struct
import test_utils
import time
import unittest
from unittest import mock

from blocks import Block, BlockFactory

class BlocksTestCase(unittest.TestCase):
    original_content = 'The quick brown fox jumps over the lazy dog.'
    expected_header_digest = '004a6f56702e01bbd97f860de1d39141219e3ef7fdfb883559ba597748cdaf10'
    expected_full_block = '80000000010000000000000000000000000000000000000000000000000000000000000000000000a51a910ecba8a599555b32133bf1829455d55fe576677b49cb561d874077385c25e9ed562003a30c790000002c00000054686520717569636b2062726f776e20666f78206a756d7073206f76657220746865206c617a7920646f672e'

    def setUp(self):
        self.byte_content = self.original_content.encode()
        self.factory = BlockFactory()

    @mock.patch('time.time', return_value=1458432293.434245)
    def test_newBlock(self, mock_object):
        # Create a new object and farm it
        test_block = self.factory.createNew(self.byte_content)
#        pbh = test_block.sha256x2(b'0')
        pbh = bytes(32)
        header_digest = test_block.farm(pbh)

        # Verify the header digest from farming to
        # the expected one
        self.assertEqual(   header_digest.hex(),
                            self.expected_header_digest,
                            'Wrong block header digest')

        # Check the contents of the full block against
        # the expected content
        inBytes = test_block.toBytes()
        self.assertEqual(inBytes.hex(),
                            self.expected_full_block,
                            'Wrong full block content')

        # The validation should return true
        self.assertTrue(test_block.validateHeaderDigest(), 'Invalid header digest')

        with open('test_file_one.dat', 'wb') as f:
            f.write(inBytes)

    def test_loadedBlock(self):
        # load the generated block from the file
        with open('test_file_one.dat', 'rb') as f:
            read_block = bytearray(f.read(4))
            block_size = struct.unpack('I', read_block)[0]
            read_block.extend(f.read(block_size))

        # Convert the binary block to a CBObject
        loadedBlock = self.factory.loadFromBytes(read_block)

        # Get the content and convert to a string
        loadedContent = loadedBlock.getContent()
        loadedString = loadedContent.decode('utf-8')

        # Make sure it matches the original input
        self.assertEqual(   loadedString,
                            self.original_content,
                            'Content not correctly loaded')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(BlocksTestCase('test_newBlock'))
    suite.addTest(BlocksTestCase('test_loadedBlock'))
    return suite

if __name__ == '__main__':
    test_utils.setup_logging('test_blocks.log')

    logging.info('Log started in file test_blocks.log')
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
    logging.info('Log ended')
