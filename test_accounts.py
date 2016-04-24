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
        address = account.getAddress()
        b58address = account.getB58Address()

        logging.debug('private key: %s', private_key.hex())
        logging.debug('public_key: %s', public_key.hex())
        logging.debug('address: %s', address.hex())
        logging.debug('b58 address: %s', b58address)

        self.assertEqual(private_key.hex(), '49d9b3c86be205880d4400880ff049d9a3ede0c7ba3cb760d41fd156fa64059f', "Incorrect private key!")
        self.assertEqual(public_key.hex(), '49d9b3c86be205880d4400880ff049d9a3ede0c7ba3cb760d41fd156fa64059f', "Incorrect public key!")
        self.assertEqual(address.hex(),'9ff641638012fb19fd5422ec441dd4d16489c7d0', "Incorrect address!")
        self.assertEqual(b58address, '13EFodMzCjU8X8cdAP2TtuTCeJqHR', "Incorrect b58 address!")

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
