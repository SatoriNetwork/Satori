import os
import satori
import ravencoin.base58
from ravencoin.wallet import P2PKHRavencoinAddress, CRavencoinSecret

class Wallet():
    
    def __init__(self):
        self._entropy = None
        self._privateKeyObj = None
        self._addressObj = None
        self.address = None
        self.scripthash = None
        self.privateKey = None

    def load(self):
        wallet = satori.disk.WalletApi.load(
            walletPath=satori.config.walletPath('wallet.yaml'))
        self.scripthash = wallet['scripthash']
        self.address = wallet['address']
        self.privateKey = wallet['privateKey']

    def save(self):
        satori.disk.WalletApi.save(
            wallet={
                'scripthash': self.scripthash,
                'address': self.address,
                'privateKey': self.privateKey},
            walletPath=satori.config.walletPath('wallet.yaml'))

    def generate(self):
        self._entropy = self._generateEntropy()
        self._privateKeyObj = self._generatePrivateKey()
        self._addressObj = self._generateAddress()
        self.scripthash = '76a914' + [s for s in self._addressObj.to_scriptPubKey().raw_iter()][2][1].hex() + '88ac'
        self.address = str(self._addressObj)
        self.privateKey = str(self._privateKeyObj)

    def _generateEntropy(self):
        return os.urandom(32)

    def _generatePrivateKey(self):
        ravencoin.SelectParams('mainnet')
        return CRavencoinSecret.from_secret_bytes(self._entropy)

    def _generateAddress(self):
        return P2PKHRavencoinAddress.from_pubkey(self._privateKeyObj.pub)
    
    def getBalance(self):
        '''
        this needs to be moved out into an interface with the blockchain,
        but we don't have that module yet. 
        
        so it's all basically hardcoded for now.
        '''
#7a2c53a541c5d4396209e18c7cd0ce4aff9f3753
#76a9147a2c53a541c5d4396209e18c7cd0ce4aff9f375388ac
#76a91412ab8dc588ca9d5787dde7eb29569da63c3a238c88ac
