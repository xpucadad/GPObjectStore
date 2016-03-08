import unittest
from GPObjectStore import Object

class GPObjectStoreTestCase(unittest.TestCase):
    def setUp(self):
        self.object = Object()
        self.object.setData(b'abc')
        self.abcdigest = "4f8b42c22dd3729b519ba6f68d2da7cc5b2d606d05daed5ad5128cc03e6c6358"

    def tearDown(self):
        self.object = None

    def test_getDigest(self):
        digest = self.object.getHexDigest()
        self.assertEqual(digest, self.abcdigest, 'incorrect hash value')

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(GPObjectStoreTestCase)
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
