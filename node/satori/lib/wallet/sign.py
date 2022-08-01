from ravencoin.wallet import CRavencoinSecret
from ravencoin.signmessage import RavencoinMessage, VerifyMessage, SignMessage

def signMessage(key:CRavencoinSecret, message:'str|RavencoinMessage'):
    ''' returns binary signature '''
    return SignMessage(
        key,
        RavencoinMessage(message) if isinstance(message, str) else message)

def verifyMessage(address:str, message:'str|RavencoinMessage', sig:'bytes|str'):
    ''' returns success bool '''
    return VerifyMessage(
        address,
        RavencoinMessage(message) if isinstance(message, str) else message,
        sig if isinstance(sig, bytes) else sig.decode())
