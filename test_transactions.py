import hashes
import logging
import struct
import test_utils
import unittest
from unittest import mock

from transactions import Transaction

class TransactionsTestCase(unittest.TestCase):
    original_content = 'The quick brown fox jumps over the lazy dog.'
    expected_transaction_digest = 'a51a910ecba8a599555b32133bf1829455d55fe576677b49cb561d874077385c'
    expected_full_transaction = '80000000010000000000000000000000000000000000000000000000000000000000000000000000a51a910ecba8a599555b32133bf1829455d55fe576677b49cb561d874077385c25e9ed562003a30c790000002c00000054686520717569636b2062726f776e20666f78206a756d7073206f76657220746865206c617a7920646f672e'

    def setUp(self):
        self.byte_content = self.original_content.encode()

    def test_newTransaction(self):
        # Create a new transaction
        txn = Transaction()
        txn.setContent(self.byte_content)
        digest = txn.getDigest()

        # Verify the header digest from farming to
        # the expected one
        self.assertEqual(   digest.hex(),
                            self.expected_transaction_digest,
                            'Wrong transaction digest')

        # Check the contents of the full block against
        # the expected content
        inBytes = txn.toBytes()
        self.assertEqual(inBytes.hex(),
                            self.expected_full_transaction,
                            'Wrong full transaction content')

        with open('test_txn_one.dat', 'wb') as f:
            f.write(inBytes)

    def test_loadedBlock(self):
        # load the generated block from the file
        with open('test_txn_one.dat', 'rb') as f:
            version = f.read(4)
            size_in_bytes = f.read(4)
            content_size = struct.unpack('I', size_in_bytes)[0]
            content = f.read(content_size)

            read_block = bytearray()
            read_block.append(version)
            read_block.append(size_in_bytes)
            read_block.append(content)

        # Convert the read in block to a transaction object
        txn_in = Transaction()
        txn_in.parseFromBytes(read_block)

        # Get the content and convert to a string
        loadedContent = txn_in.getContent()
        loadedString = loadedContent.decode('utf-8')

        # Make sure it matches the original input
        self.assertEqual(   loadedString,
                            self.original_content,
                            'Content not correctly loaded')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TransactionsTestCase('test_newTransaction'))
    suite.addTest(TransactionsTestCase('test_loadedBlock'))
    return suite

if __name__ == '__main__':
    test_utils.setup_logging('test_transactions.log')

    logging.info('Log started in file test_transactions.log')
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
    logging.info('Log ended')
