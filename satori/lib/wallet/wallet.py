import os
from satori import config
from satori.lib.apis.disk import WalletApi
import ravencoin.base58
from ravencoin.wallet import P2PKHRavencoinAddress, CRavencoinSecret

class TransactionStruct():
    
    def __init__(self, raw, vinVoutsTxs):
        self.txid = self.getTxid(raw)
        self.height = self.getHeight(raw)
        self.confirmations = self.getConfirmations(raw)
        self.sent = self.getSent(raw)
        self.received = self.getReceived(raw, vinVoutsTxs)
    
    def getTxid(self, raw):
        return raw.get('txid', 'unknown txid')
    
    def getHeight(self, raw):
        return raw.get('height', 'unknown height')
    
    def getConfirmations(self, raw):
        return raw.get('confirmations', 'unknown confirmations')
    
    def getSent(self, raw):
        sent = {}
        for vout in raw.get('vout', []):
            if 'asset' in vout:
                name = vout.get('asset', {}).get('name', 'unknown asset')
                amount = float(vout.get('asset', {}).get('amount', 0))
            else:
                name = 'Ravencoin'
                amount = float(vout.get('value', 0))
            if name in sent:
                sent[name] = sent[name] + amount
            else:
                sent[name] = amount
        return sent

    def getReceived(self, raw, vinVoutsTxs):
        received = {}
        for vin in raw.get('vin', []):
            position = vin.get('vout', None)
            for tx in vinVoutsTxs:
                for vout in tx.get('vout', []):
                    if position == vout.get('n', None):
                        if 'asset' in vout:
                            name = vout.get('asset', {}).get('name', 'unknown asset')
                            amount = float(vout.get('asset', {}).get('amount', 0))
                        else:
                            name = 'Ravencoin'
                            amount = float(vout.get('value', 0))
                        if name in received:
                            received[name] = received[name] + amount
                        else:
                            received[name] = amount
        return received
    
    def getAsset(self, raw):
        return raw.get('txid', 'unknown txid')

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
        self.rvn = None
        self.transactionHistory = None
        self.transactions = []
    
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

    def showStats(self):
        ''' returns a string of stats properly formatted '''
        def invertDivisibility(divisibility:int):
            return (16 + 1) % (divisibility + 8 + 1);
        
        divisions = self.stats.get('divisions', 8)
        circulatingSats = self.stats.get('sats_in_circulation', 100000000000000) / int('1' + ('0'*invertDivisibility(int(divisions))))
        headTail = str(circulatingSats).split('.')
        if headTail[1] == '0' or headTail[1] == '00000000':
            circulatingSats = f"{int(headTail[0]):,}"
        else:
            circulatingSats = f"{int(headTail[0]):,}" + '.' + f"{headTail[1][0:4]}" + '.' + f"{headTail[1][4:]}"
        return f'''
    Circulating Supply: {circulatingSats}
    Decimal Points: {divisions}
    Reissuable: {self.stats.get('reissuable', False)}
    Issuing Transactions: {self.stats.get('source', {}).get('tx_hash', 'a015f44b866565c832022cab0dec94ce0b8e568dbe7c88dce179f9616f7db7e3')}
    '''
        
    def showBalance(self, rvn=False):
        ''' returns a string of balance properly formatted '''
        def invertDivisibility(divisibility:int):
            return (16 + 1) % (divisibility + 8 + 1);
        
        if rvn:
            balance = self.rvn / int('1' + ('0'*8))
        else:
            balance = self.balance / int('1' + ('0'*invertDivisibility(int(self.stats.get('divisions', 8)))))
        headTail = str(balance).split('.')
        if headTail[1] == '0':
            return f"{int(headTail[0]):,}"
        else:
            return f"{int(headTail[0]):,}" + '.' + f"{headTail[1][0:4]}" + '.' + f"{headTail[1][4:]}"
        
    def get(self, allWalletInfo=False):
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
            
            if allWalletInfo:
                x = interpret(conn.send(
                    'blockchain.scripthash.get_balance', 
                    self.scripthash))
                self.rvn = x.get('confirmed', 0) + x.get('unconfirmed', 0)
                #>>> b.send("blockchain.scripthash.get_balance", script_hash('REsQeZT8KD8mFfcD4ZQQWis4Ju9eYjgxtT'))
                #b'{"jsonrpc":"2.0","result":{"confirmed":18193623332178,"unconfirmed":0},"id":1656046285682}\n'
                self.transactionHistory = interpret(conn.send(
                    'blockchain.scripthash.get_history', 
                    self.scripthash)) 
                #b.send("blockchain.scripthash.get_history", script_hash('REsQeZT8KD8mFfcD4ZQQWis4Ju9eYjgxtT'))
                #b'{"jsonrpc":"2.0","result":[{"tx_hash":"a015f44b866565c832022cab0dec94ce0b8e568dbe7c88dce179f9616f7db7e3","height":2292586}],"id":1656046324946}\n'
                self.transactions = []
                for tx in self.transactionHistory:
                    raw = interpret(conn.send(
                        'blockchain.transaction.get',
                        tx.get('tx_hash', ''), True))
                    txs = []
                    for vin in raw.get('vin', []):
                        txs.append(interpret(conn.send(
                            'blockchain.transaction.get',
                            vin.get('txid', ''), True)))
                    self.transactions.append(TransactionStruct(raw=raw, vinVoutsTxs=txs)) 
                    #>>> b.send("blockchain.transaction.get", 'a015f44b866565c832022cab0dec94ce0b8e568dbe7c88dce179f9616f7db7e3')
                    #b'{"jsonrpc":"2.0","result":"0200000001aece4f378e364682d77ea345581f4880edd0709c2bf524320b223e7c66aaf25b000000006a473044022079b86eae8bf1974be0134387f6db11a49f273660ec2ea0ce98bb5cf31dfb70d702200b1d46a748f2dea4753175f9f695a16dfdbdbdb50400076cd28165795a80b30a012103571524d47ad9240a9674c2085959c60ea62c5d5567b62e0bfd4d40727bba7a8affffffff0400743ba40b0000001976a914f62e63b933953a680f3c3a63324948293ba47d1688ac52b574088c1000001976a9143d5143a9336eaf44990a0b4249fcb823d70de52c88ac00000000000000002876a9143d5143a9336eaf44990a0b4249fcb823d70de52c88acc00c72766e6f075341544f5249217500000000000000003276a9143d5143a9336eaf44990a0b4249fcb823d70de52c88acc01672766e71065341544f524900407a10f35a00000001007500000000","id":1656046440320}\n'
                    #print(bytes.fromhex('68656c6c6f').decode('utf-8'))

                
                
# transaction history
# private key
# qr address
# address
# send
# electrum banner
# about Satori Token - asset on rvn, will be fully convertable to it's own blockchain when Satori is fully decentralized

#>>> b.send("blockchain.scripthash.get_balance", script_hash('REsQeZT8KD8mFfcD4ZQQWis4Ju9eYjgxtT'))
#b'{"jsonrpc":"2.0","result":{"confirmed":18193623332178,"unconfirmed":0},"id":1656046285682}\n'

#b.send("blockchain.scripthash.get_history", script_hash('REsQeZT8KD8mFfcD4ZQQWis4Ju9eYjgxtT'))
#b'{"jsonrpc":"2.0","result":[{"tx_hash":"a015f44b866565c832022cab0dec94ce0b8e568dbe7c88dce179f9616f7db7e3","height":2292586}],"id":1656046324946}\n'

#>>> b.send("blockchain.transaction.get", 'a015f44b866565c832022cab0dec94ce0b8e568dbe7c88dce179f9616f7db7e3')
#b'{"jsonrpc":"2.0","result":"0200000001aece4f378e364682d77ea345581f4880edd0709c2bf524320b223e7c66aaf25b000000006a473044022079b86eae8bf1974be0134387f6db11a49f273660ec2ea0ce98bb5cf31dfb70d702200b1d46a748f2dea4753175f9f695a16dfdbdbdb50400076cd28165795a80b30a012103571524d47ad9240a9674c2085959c60ea62c5d5567b62e0bfd4d40727bba7a8affffffff0400743ba40b0000001976a914f62e63b933953a680f3c3a63324948293ba47d1688ac52b574088c1000001976a9143d5143a9336eaf44990a0b4249fcb823d70de52c88ac00000000000000002876a9143d5143a9336eaf44990a0b4249fcb823d70de52c88acc00c72766e6f075341544f5249217500000000000000003276a9143d5143a9336eaf44990a0b4249fcb823d70de52c88acc01672766e71065341544f524900407a10f35a00000001007500000000","id":1656046440320}\n'
#print(bytes.fromhex('68656c6c6f').decode('utf-8'))

#>>> b.send("blockchain.transaction.get", 'a015f44b866565c832022cab0dec94ce0b8e568dbe7c88dce179f9616f7db7e3', True)
#RAW
#b'{"jsonrpc":"2.0","result":{"txid":"a015f44b866565c832022cab0dec94ce0b8e568dbe7c88dce179f9616f7db7e3","hash":"a015f44b866565c832022cab0dec94ce0b8e568dbe7c88dce179f9616f7db7e3","version":2,"size":333,"vsize":333,"locktime":0,"vin":[{"txid":"5bf2aa667c3e220b3224f52b9c70d0ed80481f5845a37ed78246368e374fceae","vout":0,"scriptSig":{"asm":"3044022079b86eae8bf1974be0134387f6db11a49f273660ec2ea0ce98bb5cf31dfb70d702200b1d46a748f2dea4753175f9f695a16dfdbdbdb50400076cd28165795a80b30a[ALL] 03571524d47ad9240a9674c2085959c60ea62c5d5567b62e0bfd4d40727bba7a8a","hex":"473044022079b86eae8bf1974be0134387f6db11a49f273660ec2ea0ce98bb5cf31dfb70d702200b1d46a748f2dea4753175f9f695a16dfdbdbdb50400076cd28165795a80b30a012103571524d47ad9240a9674c2085959c60ea62c5d5567b62e0bfd4d40727bba7a8a"},"sequence":4294967295}],"vout":[{"value":500.0,"n":0,"scriptPubKey":{"asm":"OP_DUP OP_HASH160 f62e63b933953a680f3c3a63324948293ba47d16 OP_EQUALVERIFY OP_CHECKSIG","hex":"76a914f62e63b933953a680f3c3a63324948293ba47d1688ac","reqSigs":1,"type":"pubkeyhash",'
#b'{"jsonrpc":"2.0","result":{"txid":"a015f44b866565c832022cab0dec94ce0b8e568dbe7c88dce179f9616f7db7e3","hash":"a015f44b866565c832022cab0dec94ce0b8e568dbe7c88dce179f9616f7db7e3","version":2,"size":333,"vsize":333,"locktime":0,"vin":[{"txid":"5bf2aa667c3e220b3224f52b9c70d0ed80481f5845a37ed78246368e374fceae","vout":0,"scriptSig":{"asm":"3044022079b86eae8bf1974be0134387f6db11a49f273660ec2ea0ce98bb5cf31dfb70d702200b1d46a748f2dea4753175f9f695a16dfdbdbdb50400076cd28165795a80b30a[ALL] 03571524d47ad9240a9674c2085959c60ea62c5d5567b62e0bfd4d40727bba7a8a","hex":"473044022079b86eae8bf1974be0134387f6db11a49f273660ec2ea0ce98bb5cf31dfb70d702200b1d46a748f2dea4753175f9f695a16dfdbdbdb50400076cd28165795a80b30a012103571524d47ad9240a9674c2085959c60ea62c5d5567b62e0bfd4d40727bba7a8a"},"sequence":4294967295}],"vout":[{"value":500.0,"n":0,"scriptPubKey":{"asm":"OP_DUP OP_HASH160 f62e63b933953a680f3c3a63324948293ba47d16 OP_EQUALVERIFY OP_CHECKSIG","hex":"76a914f62e63b933953a680f3c3a63324948293ba47d1688ac","reqSigs":1,"type":"pubkeyhash",'
#>>>