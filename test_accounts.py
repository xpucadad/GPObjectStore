import hashes
import logging
import struct
import test_utils
import unittest
from unittest import mock

from accounts import Account

class AccountsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('time.time', return_value=1458432293.434245)
    def test_newAccount(self, mock_object):
        # Create a new accounts
        account = Account()

        # Generate the keys
        account.generateKeys()

        private_key = account.getPrivateKey()
        public_key = account.getPublicKey()

        print()
        print('private key:\t', private_key.hex())
        print('public_key:\t', public_key.hex())

        self.assertTrue(True, 'Should never fail!')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(AccountsTestCase('test_newAccount'))
    return suite

if __name__ == '__main__':
    log_file = 'test_accounts.log'
    test_utils.setup_logging(log_file)

    logging.info('Log started in file %s', log_file)
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
    logging.info('Log ended')
