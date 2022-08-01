from ravencoin.wallet import CRavencoinSecret
from ravencoin.signmessage import RavencoinMessage, VerifyMessage, SignMessage


## solved by RavencoinMessage
#import sys
#_bchr = lambda x: bytes([x])
#_bord = lambda x: x[0]
#from io import BytesIO as _BytesIO
#import ravencoin
#class Message(str):   
#    '''
#    a Message is just a string with these monkey patched functions
#    since python-ravencoinlib expects them to be present.
#    '''
#    
#    def GetHash(self):
#        return ravencoin.core.Serializable.GetHash(self)
#    
#    def serialize(self, params={}):
#        f = _BytesIO()
#        return f.getvalue()

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
