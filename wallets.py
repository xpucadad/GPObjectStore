import logging

# Project files
from accounts import Account
import hashes

class Wallet():
    address_to_account = dict()
    name_to_account = dict()

    def __init__(self, filename):
        self.filename = filename

    def loadFromFile(self, file):
        pass

    def saveToFile(self, file):
        pass

    def createNewAccount(self, name):
        if name != '' and name in self.name_to_account:
            debugging.error("There is already an account named %s. Please use a different name.", name)
        account = Account(name)
        account.generateKeys()
        self.address_to_account[account.getAddress()] = account
        if name != '':
            self.name_to_account[name] = account
        return account

    def findAccount(self, address):
        # if address is a string, assume it's a b58 encoded address
        # if address is bytes, assume it's a "raw" address

        if type(address) == str:
            logging.debug('Wallet.findAccount looking for %s', address)
            # Get the raw address
            typed_address = hashes.b58decodecheck(address)
            # These come back with the version (type) byte at the beginning.
            # We need to remove this.
            raw_address = typed_address[1:]
        elif type(address) == bytes:
            logging.debug('Wallet.findAccount looking for %s', address.hex())
            raw_address = address
        else:
            logging.error('Wallet.findAccount address is of unexpected type: %s', type(address))
            raw_address = bytes(0)

        if raw_address in self.address_to_account:
            account = self.address_to_account[raw_address]
        else:
            logging.info('Account not found with address %s', raw_address.hex())
            account = None

        return account

    def findNamedAccount(self, name):
        if name == '' or name not in self.name_to_account:
            logging.info('No account named %s found.', name)
            return None
        else:
            return self.name_to_account[name]
