import unittest
import time
from unittest import mock
from CBObject import CBObject, CBObjectFactory

class CBObjectTestCase(unittest.TestCase):
    expected_hash = '004a6f56702e01bbd97f860de1d39141219e3ef7fdfb883559ba597748cdaf10'

    def setUp(self):
        pass

    @mock.patch('time.time', return_value=1458432293.434245)
    def test_newBlock(self, mock_object):
        data = b'The quick brown fox jumps over the lazy dog.'

        factory = CBObjectFactory()
        block = factory.createNew(data)
        pbh = bytearray(32)
        header_digest = block.farm(pbh)
        #block.dumpHeader()
        #print(header_digest.hex())
        self.assertEqual(   header_digest.hex(),
                            self.expected_hash,
                            'Incorrect block hash')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(CBObjectTestCase('test_newBlock'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
