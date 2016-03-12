import unittest
import struct
import time
from GPObjectStore import Object
from GPObjectStore import BTCBlockHeader

class GPObjectStoreTestCase(unittest.TestCase):
    def setUp(self):
        self.object = Object()
        self.object.extendData(b'abc')
        self.abcdigest = "4f8b42c22dd3729b519ba6f68d2da7cc5b2d606d05daed5ad5128cc03e6c6358"

    def tearDown(self):
        self.object = None

    def test_getDigest(self):
        digest = self.object.sha256x2()
        hexdigest = digest.hex()
        self.assertEqual(hexdigest, self.abcdigest, 'incorrect digest value')

class BTCBlockHeaderTestCase(unittest.TestCase):
    def setUp(self):
        self.pbh = bytearray(32)
        self.dt = bytearray(4)
        self.bad_digest_message = 'incorrect digest value'
        self.hash_header_digest = "be5d0adf7aa2b47335ee850e766b2d8bc7e9c4560d8b7fccf111883a78e38194"
        self.link_digest1 = "a5a79c2ef8c277d8726ab56726de3c497f471be9f47f5f72aba5022cacf982b5"
        self.link_digest2 = "111bcd61881ec816d1af260903853c190a4a16b865fbc27be27bdb63f0d9e55d"

    def tearDown(self):
        pass

    def test_hashHeader(self):
        block_header = BTCBlockHeader(self.pbh, self.dt)
        block_header.setTimeStamp(5)
        header_digest = block_header.hashHeader()
#        print(header_digest.hex())
        self.assertEqual(header_digest.hex(), self.hash_header_digest, self.bad_digest_message)

    def test_link(self):
        bh1 = BTCBlockHeader(self.pbh, self.dt)
        bh1.setTimeStamp(1)
        d1 = bh1.hashHeader()
#        bh1.print_data()
#        bh1.print_digest()
        self.assertEqual(d1.hex(), self.link_digest1, self.bad_digest_message)
        bh2 = BTCBlockHeader(d1, self.dt)
        bh2.setTimeStamp(2)
        d2 = bh2.hashHeader()
#        bh2.print_data()
#        bh2.print_digest()
        self.assertEqual(d2.hex(), self.link_digest2, self.bad_digest_message)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(GPObjectStoreTestCase('test_getDigest'))
    suite.addTest(BTCBlockHeaderTestCase('test_hashHeader'))
    suite.addTest(BTCBlockHeaderTestCase('test_link'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
