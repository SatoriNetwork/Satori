# to be called by elixir since verification works well in python 
# https://medium.com/stuart-engineering/how-we-use-python-within-elixir-486eb4d266f9

from ravencoin.signmessage import RavencoinMessage, VerifyMessage

def generateAddress(publicKey: str):
    from ravencoin.wallet import P2PKHRavencoinAddress
    from ravencoin.core.key import CPubKey
    return str(
        P2PKHRavencoinAddress.from_pubkey(
            CPubKey(
                bytearray.fromhex(
                    publicKey))))

def verify(message:'str|RavencoinMessage', signature:'bytes|str', publicKey:str=None, address:str=None):
    return VerifyMessage(
        address or generateAddress(publicKey),
        RavencoinMessage(message) if isinstance(message, str) else message,
        signature if isinstance(signature, bytes) else signature.encode())
