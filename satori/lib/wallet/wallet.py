import os
from satori import config
from satori.lib.apis.disk import WalletApi
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
        self.balance = None
        self.stats = None
        self.banner = None
    
    def __repr__(self):
        return f'''Wallet(
    address: {self.address}
    scripthash: {self.scripthash}
    privateKey: {self.privateKey}
    balance: {self.balance}
    stats: {self.stats}
    banner: {self.banner})'''
    
    def init(self):
        ''' try to load, else generate and save '''
        self.load()
        if (self.address == None):
            self.generate()
            self.save()
        # temp
        self.scripthash = self._generateScripthash()            
        self.get()

    def load(self):
        wallet = WalletApi.load(
            walletPath=config.walletPath('wallet.yaml'))
        self.scripthash = wallet['scripthash']
        self.address = wallet['address']
        self.privateKey = wallet['privateKey']

    def save(self):
        WalletApi.save(
            wallet={
                'scripthash': self.scripthash,
                'address': self.address,
                'privateKey': self.privateKey},
            walletPath=config.walletPath('wallet.yaml'))

    def generate(self):
        self._entropy = self._generateEntropy()
        self._privateKeyObj = self._generatePrivateKey()
        self._addressObj = self._generateAddress()
        self.address = str(self._addressObj)
        self.scripthash = self._generateScripthash()
        self.privateKey = str(self._privateKeyObj)

    def _generateScripthash(self):
        # possible shortcut:
        #self.scripthash = '76a914' + [s for s in self._addressObj.to_scriptPubKey().raw_iter()][2][1].hex() + '88ac'
        from base58 import b58decode_check
        from binascii import hexlify
        from hashlib import sha256
        import codecs
        OP_DUP = b'76'
        OP_HASH160 = b'a9'
        BYTES_TO_PUSH = b'14'
        OP_EQUALVERIFY = b'88'
        OP_CHECKSIG = b'ac'
        DATA_TO_PUSH = lambda address: hexlify(b58decode_check(address)[1:])
        sig_script_raw = lambda address: b''.join((OP_DUP, OP_HASH160, BYTES_TO_PUSH, DATA_TO_PUSH(address), OP_EQUALVERIFY, OP_CHECKSIG))
        scripthash = lambda address: sha256(codecs.decode(sig_script_raw(address), 'hex_codec')).digest()[::-1].hex()
        return scripthash(self.address);

    def _generateEntropy(self):
        return os.urandom(32)

    def _generatePrivateKey(self):
        ravencoin.SelectParams('mainnet')
        return CRavencoinSecret.from_secret_bytes(self._entropy)

    def _generateAddress(self):
        return P2PKHRavencoinAddress.from_pubkey(self._privateKeyObj.pub)

    def showBalance(self):
        ''' returns a string of balance properly formatted '''
        def invertDivisibility(divisibility:int):
            return (16 + 1) % (divisibility + 8 + 1);
        
        balance = self.balance / int('1' + ('0'*invertDivisibility(int(self.stats.get('divisions', 8)))))
        headTail = str(balance).split('.')
        if headTail[1] == '0':
            return f"{int(headTail[0]):,}"
        else:
            return f"{int(headTail[0]):,}" + '.' + f"{headTail[1][0:4]}" + '.' + f"{headTail[1][4:]}"
        
    def get(self):
        '''
        this needs to be moved out into an interface with the blockchain,
        but we don't have that module yet. so it's all basically hardcoded for now.
        
        get_asset_balance
        {'confirmed': {'SATORI!': 100000000, 'SATORI': 100000000000000}, 'unconfirmed': {}}
        get_meta
        {'sats_in_circulation': 100000000000000, 'divisions': 0, 'reissuable': True, 'has_ipfs': False, 'source': {'tx_hash': 'a015f44b866565c832022cab0dec94ce0b8e568dbe7c88dce179f9616f7db7e3', 'tx_pos': 3, 'height': 2292586}}
        '''
        def interpret(x:str):
            return json.loads(x.decode('utf-8')).get('result', None)

        #def invertDivisibility(divisibility:int):
        #    return (16 + 1) % (divisibility + 8 + 1);
        #
        #def removeStringedZeros():
        #    
        #    return self.balance[0:len(self.balance) - invertDivisibility(int(self.stats.get('divisions', 8)))] 
        #
        #def removeZeros():
        #    return self.balance / 
        #
        #def splitBalanceOnDivisibility():
        #    return self.balance / int('1' + ('0'*invertDivisibility(int(self.stats.get('divisions', 8)))) )

        import json
        import random
        from satori.lib.apis.blockchain import ElectrumX
        from satori import config 
        hostPorts = config.electrumxServers()
        if len(hostPorts) == 0:
            return 
        hostPort = random.choice(hostPorts)
        conn = ElectrumX(
            host=hostPort.split(':')[0],
            port=int(hostPort.split(':')[1]),
            ssl=True,
            timeout=5)
        name = f'Satori Node {self.address}'
        assetApiVersion = '1.10'
        handshake = interpret(conn.send(
            'server.version', 
            name, 
            assetApiVersion))
        if (
            handshake[0].startswith('ElectrumX Ravencoin')
            and handshake[1] == assetApiVersion
        ):
            self.banner = interpret(conn.send('server.banner'))
            self.balance = interpret(conn.send(
                'blockchain.scripthash.get_asset_balance', 
                self.scripthash)
            ).get('confirmed', {}).get('SATORI', 'unknown')
            self.stats = interpret(conn.send(
                'blockchain.asset.get_meta', 
                'SATORI'))
