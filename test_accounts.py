import hashes
import logging
import struct
import test_utils
import unittest
from unittest import mock

import accounts
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

        logging.debug('private key: %s', private_key.hex())
        logging.debug('public_key: %s', public_key.hex())

        self.assertTrue(True, 'Should never fail!')

    def test_signature(self):
        message = b'Suck my dick.'
        account = Account()
        account.generateKeys()
        signature = account.sign(message)
        logging.debug('signature: %s',signature.hex())

        sig_valid = accounts.isValid(
            account.getPublicKey(),
            message,
            signature
        )
        self.assertTrue(sig_valid, "Signature not valid!")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(AccountsTestCase('test_newAccount'))
    suite.addTest(AccountsTestCase('test_signature'))
    return suite

if __name__ == '__main__':
    log_file = 'test_accounts.log'
    test_utils.setup_logging(log_file)

    logging.info('Log started in file %s', log_file)
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
    logging.info('Log ended')
