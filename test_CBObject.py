import unittest
import time
from unittest import mock
from CBObject import CBObject, CBObjectFactory

class CBObjectTestCase(unittest.TestCase):
    expected_header_digest = '034670e383dbcd651eefc941685dfd3001abe2eed9ef675876c529eaf784f91d'
    expected_full_block = '800000000100000067050eeb5f95abf57449d92629dcf69f80c26247e207ad006a862d1e4e6498ffa51a910ecba8a599555b32133bf1829455d55fe576677b49cb561d874077385c25e9ed562003a30c6f0000002c00000054686520717569636b2062726f776e20666f78206a756d7073206f76657220746865206c617a7920646f672e'
    def setUp(self):
        pass

    @mock.patch('time.time', return_value=1458432293.434245)
    def test_newBlock(self, mock_object):
        data = b'The quick brown fox jumps over the lazy dog.'

        factory = CBObjectFactory()
        block = factory.createNew(data)
        pbh = block.sha256x2(b'0')
        header_digest = block.farm(pbh)
        #block.dumpHeader()
        #print(header_digest.hex())
        self.assertEqual(   header_digest.hex(),
                            self.expected_header_digest,
                            'Wrong block header digest')
        inBytes = block.toBytes()
        #print(inBytes.hex())
        self.assertEqual(inBytes.hex(),
                            self.expected_full_block,
                            'Wrong full block content')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(CBObjectTestCase('test_newBlock'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
