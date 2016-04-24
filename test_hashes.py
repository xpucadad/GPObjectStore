import logging
#import struct
import test_utils
import time
import unittest

from unittest import mock

# This is what we're testing
import hashes

class HashesTestCase(unittest.TestCase):
    test_key = '005cc87f4a3fdfe3a2346b6953267ca867282630d3f9b78e64'
    test_key_bytes = bytes.fromhex(test_key)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def simple_tests(self):
        self.__encode1_number(10, '1B')
        self.__encode1_number(16, '1H')
        self.__encode1_number(255, '15Q')
        self.__encode1_number(256, '15R')
        self.__encode1_number(257, '15S')
        self.__encode1_number(1024, '1Jf')
        self.__encode1_number(1000000, '168GP')
        self.__encode1_bytes(b'\x00\x00\x0a', '1B')
        self.__encode1_bytes(self.test_key_bytes, '19TbMSWwHvnxAKy12iNm3KdbGfzfaMFViT')

    def __encode1_number(self, number, result):
        len_bits = number.bit_length()
        len_bytes, remainder = divmod(len_bits, 8)
        if (remainder > 0): len_bytes += 1

        # Need to prefix with the type of b58 code. Here
        # we assume all are addresses.
        in_bytes = bytearray()
        in_bytes.append(0x00)
        in_bytes.extend(number.to_bytes(len_bytes,'big'))
        logging.debug('number %d, bytes %d, in (typed) bytes %s',
            number, len_bytes, in_bytes.hex())
        self.__encode1_bytes(in_bytes, result)

    def __encode1_bytes(self, value_in_bytes, result):
        encoded = hashes.b58encode(value_in_bytes)
        logging.debug('value %s, b58 encoded: %s',
            value_in_bytes.hex(), encoded)
        self.assertTrue(encoded == result, 'Encoding error!')
        return encoded

def suite():
    suite = unittest.TestSuite()
    suite.addTest(HashesTestCase('simple_tests'))
    return suite

if __name__ == '__main__':
    log_file = 'test_hashes.log'
    test_utils.setup_logging(log_file)

    logging.info('Log started in file %s', log_file)
    runner = unittest.TextTestRunner(verbosity = 2)
    test_suite = suite()
    runner.run(test_suite)
    logging.info('End Logging')
