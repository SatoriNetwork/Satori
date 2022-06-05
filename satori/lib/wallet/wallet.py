import os
import satori
import ravencoin.base58
from ravencoin.wallet import P2PKHRavencoinAddress, CRavencoinSecret

class Wallet():
    
    def __init__(self):
        self._entropy = None
        self._privateKeyObj = None
        self.address = None
        self.privateKey = None

    def load(self):
        wallet = satori.disk.WalletApi.load(
            walletPath=satori.config.walletPath('wallet.yaml'))
        self.address = wallet['address']
        self.privateKey = wallet['privateKey']

    def save(self):
        satori.disk.WalletApi.save(
            wallet={
                'privateKey': self.privateKey,
                'address': self.address},
            walletPath=satori.config.walletPath('wallet.yaml'))

    def generate(self):
        self._entropy = self._generateEntropy()
        self._privateKeyObj = self._generatePrivateKey()
        self.address = self._generateAddress()
        self.privateKey = str(self._privateKeyObj)

    def _generateEntropy(self):
        return os.urandom(32)

    def _generatePrivateKey(self):
        ravencoin.SelectParams('mainnet')
        return CRavencoinSecret.from_secret_bytes(self._entropy)

    def _generateAddress(self):
        return str(P2PKHRavencoinAddress.from_pubkey(self._privateKeyObj.pub))