# a satori node uses the wallet public key to connect to the server via signing a message.
# the message is the date in UTC now that way the server doesn't have to give the client
# a message to sign. so the client just sends up the public key and the sig. done.

import datetime as dt

def payloadForServer(wallet):
    ''' see wallet_auth in server '''
    dateMessage = getFullDateMessage()
    return {
        'message': dateMessage,
        'pubkey': wallet.publicKey,
        'sig': wallet.sign(dateMessage).decode()}
    
def getFullDateMessage():
    ''' returns a string of today's date in UTC like this: "2022-08-01 17:28:44.748691" '''
    return str(dt.datetime.utcnow())