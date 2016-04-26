import logging
#import struct
import unittest
from unittest import mock

import hashes
import test_utils
#from time import sleep

import accounts
from accounts import Account
from wallets import Wallet

class WalletsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_newWallet(self):
        # Create a wallet
        wallet = Wallet('test_wallets_w1.dat')

        # Create 2 accounts with Names
        a1_name = 'account 1'
        a1 = wallet.createNewAccount(a1_name)
        a1_raw_address = a1.getAddress()
        a1_b58_address = a1.getB58Address()

        a2_name = 'account 2'
        a2 = wallet.createNewAccount(a2_name)
        a2_raw_address = a2.getAddress()
        a2_b58_address = a2.getB58Address()

        # Retrieve the accounts by address and compare to the originals
        t1n = wallet.findNamedAccount(a1_name)
        self.assertTrue(a1.equals(t1n))
        t1a = wallet.findAccount(a1_raw_address)
        self.assertTrue(a1.equals(t1a))
        t1b = wallet.findAccount(a1_b58_address)
        self.assertTrue(a1.equals(t1b))

        t2n = wallet.findNamedAccount(a2_name)
        self.assertTrue(a2.equals(t2n))
        t2a = wallet.findAccount(a1_raw_address)
        self.assertTrue(a2.equals(t2a))
        t2b = wallet.findAccount(a1_b58_address)
        self.assertTrue(a2.equals(t2b))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(WalletsTestCase('test_newWallet'))
    return suite

if __name__ == '__main__':
    log_file = 'test_wallets.log'
    test_utils.setup_logging(log_file)

    logging.info('Log started in file %s', log_file)
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
    logging.info('Log ended')
