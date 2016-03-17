import unittest

from CBObject import CBObject, CBObjectFactory

class CBObjectTestCase(unittest.TestCase):
    def setUp(self): pass
    def tearDown(self): pass

    def test_newBlock(self):
        data = b'The quick brown fox jumps over the lazy dog.'

        factory = CBObjectFactory()
        block = factory.createNew(data)
        pbh = bytearray(32)
        header_digest = block.farm(pbh)
        block.dumpHeader()
        print(header_digest.hex())
        self.assertTrue(True, 'impossible failure')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(CBObjectTestCase('test_newBlock'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
