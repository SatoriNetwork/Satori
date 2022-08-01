# a satori node uses the wallet public key to connect to the server via signing a message.
# the message is the date in UTC now that way the server doesn't have to give the client
# a message to sign. so the client just sends up the public key and the sig. done.

import datetime as dt
from satori.lib.wallet import Wallet

def payloadForServer(wallet: Wallet):
    '''
    we can avoid sending the message if we just go off date, otherwise, we'll send it
    we always want to make sure the message is different each time we connect, 
    so snoopers can't attack. but we don't want to keep a record of each login on the
    server so, the server checks that the date is recent (same day, or same hour),
    or if we send the full message we can verify the message and verify the date
    down to within a few seconds. anyway. thats the idea. 
    # elixir code [h, _] = String.split(DateTime.to_string(DateTime.utc_now)," ")
    
    we could save the last login time on the user object or something. then verify
    the date is current, but get the whole message and verify that the messge is
    greater than the saved message as the last time they logged in.
    # verify DateTime.compare(more_recent_dt, preivous_dt) is :gt
    '''
    dateMessage = getFullDateMessage()
    return {
        'message': dateMessage,
        'pubkey': wallet.publicKey,
        'sig': wallet.sign(dateMessage).decode(),}
    
def getDateMessage():
    ''' returns a string of today's date in UTC like this: "2022-08-01" '''
    return getFullDateMessage().split()[0]

def getFullDateMessage():
    ''' returns a string of today's date in UTC like this: "2022-08-01 17:28:44.748691" '''
    return str(dt.datetime.utcnow())