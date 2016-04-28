import logging
import struct

# Project files
from accounts import Account
import hashes

class Wallet():
    address_to_account = dict()
    name_to_account = dict()

    def __init__(self):
        pass

    def loadFromFile(self, file):
        with open(file, 'rb') as f:
            while True:
                raw_size = f.read(4)
                if len(raw_size) < 4: break
                size = struct.unpack('I', raw_size)[0]
                buffer = f.read(size)
                account = Account('')
                account.fromBytes(buffer)
                self.__addAccount(account)

    def saveToFile(self, file):
        with open(file,'wb') as f:
        # Loop through all the accounts
            for account in self.address_to_account.values():
                # Convert to byte
                account_in_bytes = account.toBytes()
                # Write to file
                length = len(account_in_bytes)
                buffer = bytearray()
                buffer.extend(struct.pack('I', length))
                buffer.extend(account_in_bytes)
                f.write(buffer)

    def createNewAccount(self, name):
        if name != '' and name in self.name_to_account:
            debugging.error("There is already an account named %s. Please use a different name.", name)
        account = Account(name)
        account.generateKeys()
        self.__addAccount(account)

        return account

    def __addAccount(self, account):
        self.address_to_account[account.getAddress()] = account
        name = account.getName()
        if name != '': self.name_to_account[name] = account
        return account

    def findAccount(self, address):
        # if address is a string, assume it's a b58 encoded address
        # if address is bytes, assume it's a "raw" address

        if type(address) == str:
            logging.debug('Wallet.findAccount looking for %s', address)
            # Get the raw address
            try:
                typed_address = hashes.b58decodecheck(address)
            except ResourceWarning as inst:
                logging.error('Invalid address: %s', inst.args)
                raw_address = bytes(0)
                raise
            else:
                # These come back with the version (type) byte at the beginning.
                # We need to remove this.
                raw_address = typed_address[1:]
        elif type(address) == bytes:
            logging.debug('Wallet.findAccount looking for %s', address.hex())
            raw_address = address
        else:
            logging.error('Wallet.findAccount address is of unexpected type: %s, %s', address, type(address))
            raw_address = bytes(0)
            raise ResourceWarning(address, type(address))

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

    def __str__(self):
        out = str(self.address_to_account)
        return out
