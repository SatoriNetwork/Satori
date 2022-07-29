import sys
_bchr = lambda x: bytes([x])
_bord = lambda x: x[0]
from io import BytesIO as _BytesIO
import ravencoin
from ravencoin import signmessage
from ravencoin.wallet import CRavencoinSecret

class Message(str):   
    '''
    a Message is just a string with these monkey patched functions
    since python-ravencoinlib expects them to be present.
    '''
    
    def GetHash(self):
        return ravencoin.core.Serializable.GetHash(self)
    
    def serialize(self, params={}):
        f = _BytesIO()
        return f.getvalue()

def makeMessage(message:str):
    return Message(message)

def signMessage(key:CRavencoinSecret, message:Message):
    ''' returns binary signature '''
    return signmessage.SignMessage(key, message)

def verifyMessage(address:str, message:Message, sig:bytes):
    ''' returns success bool '''
    return signmessage.VerifyMessage(address, message, sig)
