import hashes
import logging
import random
import struct
import test_utils
from time import sleep
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
    @mock.patch('random.random', return_value= 0.0)
    def test_newAccount(self, mock_object1, mockobject2):
        # Create a new accounts
        name = 'test new account'
        account = Account(name)

        # Generate the keys
        account.generateKeys()

        private_key = account.getPrivateKey()
        public_key = account.getPublicKey()
        address = account.getAddress()
        b58address = account.getB58Address()
        set_name = account.getName()

        logging.debug('private key: %s', private_key.hex())
        logging.debug('public_key: %s', public_key.hex())
        logging.debug('address: %s', address.hex())
        logging.debug('b58 address: %s', b58address)
        logging.debug('name: %s', set_name)

        self.assertEqual(private_key.hex(), '1bf1cd4065d7ad80f01b271dcf3121112e97e2553b25a5dad5bfd5cc540f654c', "Incorrect private key!")
        self.assertEqual(public_key.hex(), '1bf1cd4065d7ad80f01b271dcf3121112e97e2553b25a5dad5bfd5cc540f654c', "Incorrect public key!")
        self.assertEqual(address.hex(),'2447daf348074b76b36fbc9ec15f154f5d487a37', "Incorrect address!")
        self.assertEqual(b58address, '14JqQVsxQDSewkkQrJuvCbhZuSHWC2CunJ', "Incorrect b58 address!")
        self.assertEqual(name, set_name, "Incorrect name!")

    def test_signature(self):
        message = b'Suck my dick.'
        account = Account('Felatio')
        account.generateKeys()
        signature = account.sign(message)
        logging.debug('signature: %s',signature.hex())

        sig_valid = accounts.isValid(
            account.getPublicKey(),
            message,
            signature
        )
        self.assertTrue(sig_valid, "Signature not valid!")

    def test_not_equal(self):
        a1 = Account('a1')
        a1.generateKeys()
        a2 = Account('a1')
        a2.generateKeys()

        self.assertFalse(a1.equals(a2),"Accounts should be different!")

    def test_marshalling(self):
        # Create an account and convert it to bytes
        in_name = 'Love that hard cock!'
        account = Account('Visual')
        account.generateKeys()
        buffer = account.toBytes()
#        print('test_marshalling:',buffer.hex())
        logging.debug('Marshalled buffer: %s', buffer.hex())
        # Create a new account from the bytes
        new_account = Account('')
        new_account.fromBytes(buffer)

        # Check if they have the content
        self.assertTrue(new_account.equals(account))

        # Different names should be okay, if all else is the same
        new_name = 'resurected!'
        new_account.setName(new_name)
        self.assertEqual(new_name, new_account.getName(),'Account name not set correctly!')
        self.assertTrue(new_account.equals(account), "Names should not affect Account equality!")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(AccountsTestCase('test_newAccount'))
    suite.addTest(AccountsTestCase('test_signature'))
    suite.addTest(AccountsTestCase('test_marshalling'))
    suite.addTest(AccountsTestCase('test_not_equal'))
    return suite

if __name__ == '__main__':
    log_file = 'test_accounts.log'
    test_utils.setup_logging(log_file)

    logging.info('Log started in file %s', log_file)
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
    logging.info('Log ended')
