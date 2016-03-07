import unittest
from GPObjectStore import Object

class GPObjectStoreTestCase(unittest.TestCase):
    def setUp(self):
        self.object = Object()
        self.object.setData(b'abc')
        self.abchash = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

    def tearDown(self):
        self.object = None

    def test_getDigest(self):
        digest = self.object.getHexDigest()
        self.assertEqual(digest, self.abchash, 'incorrect hash value')

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(GPObjectStoreTestCase)
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
