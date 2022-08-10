def generateKey(streamName):
    f'''ipfs key gen {streamName}'''

def associateKeyWithStream(key, streamName):
    '''saves locally tells server'''
    generateKey(streamName)
    tellServer(key, streamName)

def tellServer(key, streamName):
    '''endpoint'''

def get(key):
    '''curl https://gateway.ipfs.io/ipns/{key}'''

def publish(ipfs, streamName):
    f'''ipfs name publish --key={streamName} /ipfs/{ipfs}'''


def getMostPopular(ipnsKeys):
    '''
    do we want to get most popluar (a heuristic)
    or do we want to see which one has the longest data?
    more true, but more work. do this first.'''
    {key:
        f'ipfs name resolve --key={key}'
        for key in ipnsKeys}