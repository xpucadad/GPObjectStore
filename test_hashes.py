import logging
#import struct
import test_utils
import time
import unittest

from unittest import mock

import accounts
from accounts import Account

# This is what we're testing
import hashes

class HashesTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def simple_tests(self):
        print()
        self.__encode1_number(10, 'B')
        self.__encode1_number(16, 'H')
        self.__encode1_number(255, '5Q')
        self.__encode1_number(256, '5R')
        self.__encode1_number(257, '5S')
        self.__encode1_number(1024, 'Jf')
        self.__encode1_number(1000000, '68GP')
        self.__encode1_bytes(b'\x00\x00\x0a', 'B')

    def __encode1_number(self, number, result):
        len_bits = number.bit_length()
        len_bytes, remainder = divmod(len_bits, 8)
        if (remainder > 0): len_bytes += 1
        in_bytes = number.to_bytes(len_bytes,'big')
        print(number, len_bytes, end=' ')
        self.__encode1_bytes(in_bytes, result)

    def __encode1_bytes(self, value_in_bytes, result):
        encoded = hashes.b58encode(value_in_bytes)
        print(value_in_bytes.hex(), encoded)
        self.assertTrue(encoded == result, 'Encoding error!')
        return encoded


    @mock.patch('time.time', return_value=1458432293.434245)
    def public_key_tests(self, mock_object):
        print()
        account = Account()
        account.generateKeys()
        raw_address = account.getAddress()
        address = self.__encode1_bytes(raw_address, '3EFodMzCjU8X8cdAP2TtuTCeJqHR')
        print('address', address)
        print('len', len(address))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(HashesTestCase('simple_tests'))
    suite.addTest(HashesTestCase('public_key_tests'))
    return suite

if __name__ == '__main__':
    log_file = 'test_hashes.log'
    test_utils.setup_logging(log_file)

    logging.info('Log started in file %s', log_file)
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
    logging.info('End Logging')
