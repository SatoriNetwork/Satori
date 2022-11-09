import json
import requests 
from satori import Wallet
w = Wallet()()             

# TODO make a set of fixtures for testing

class fixtures():
    @staticmethod
    def streams(): 
        return {
            0: {},
            1: {'source': 'test', 'name': 'stream1', 'target':'target'},
            2: {'source': 'test'},
        }
        
    @staticmethod
    def subscriptions(): 
        return {
            0: {},
            1: {'publisher': {'pubkey': '12a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8'}, 
                'stream': {
                    'source': 'source', 
                    'name': 'name pred', 
                    'target': 'target'}},
        }


def register_wallet():
    r = requests.post(
        'http://localhost:5002/register/wallet',
        headers=w.authPayload(asDict=True),
        json=w.registerPayload())
    print(r.status_code, r.text)
    #from satori.apis import system
    #w.authPayload()
    #'{"message": "2022-10-20 20:14:02.322147", "pubkey": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "address": "RPBG9hf93Uge2SgZt4K1mRNyJeTTcKe8kt", "signature": "IHi9HH21rED8hZsTio6Q488qi/cSZ5DRgWSN9rsqTSGcJiXk3v1qECXVYB2ptcTk5dGThqpCmqJCXP2/gR4ubL8="}'
    #system.devicePayload()
    #{'ram_total_gb': 32, 'ram_available_percent': 49.16639057975354, 'cpu': 8, 'disk_total': 475, 'disk_free': 66, 'bandwidth': 'unknown'}

def register_stream():
    ''' publish raw data'''
    r = requests.post(
        'http://localhost:5002/register/stream',
        headers=w.authPayload(asDict=True),
        json=json.dumps(fixtures.streams()[1]))
    print(r.status_code, r.text)

def register_subscription(x:int):
    ''' subscribe to stream '''
    r = requests.post(
        'http://localhost:5002/register/subscription',
        headers=w.authPayload(asDict=True),
        json=json.dumps(fixtures.subscriptions()[x]))
    print(r.status_code, r.text)
    
def request_primary():
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.get(
        'http://localhost:5002/request/primary',
        headers=w.authPayload(asDict=True))
    print(r.status_code, r.text)    


def get_streams(x:int):
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.post(
        'http://localhost:5002/get/streams',
        headers=w.authPayload(asDict=True),
        json=json.dumps(fixtures.streams()[x]))
    print(r.status_code, r.text)  
    
def my_streams():
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.post(
        'http://localhost:5002/my/streams',
        headers=w.authPayload(asDict=True),
        json='{}')
    print(r.status_code, r.text)  
    
def checkin():
    r = requests.post(
        'http://localhost:5002/checkin',
        headers=w.authPayload(asDict=True),
        json=w.registerPayload())
    print(r.status_code, r.text)  
    j = r.json()
    print('j', j)
    # use subscriptions to initialize engine 
    print('subscriptions', j.get('subscriptions'))
    # use publications to initialize engine
    print('publications', j.get('publications'))
    # use pins to initialize engine and update any missing data
    print('pins', j.get('pins'))
    # use server version to use the correct api
    print('server version', j.get('versions', {}).get('server'))
    # use client version to know when to update the client
    print('client version', j.get('versions', {}).get('client'))
    
    
if __name__ == '__main__':
    #register_wallet()
    #register_stream()
    #register_subscription(1) # 400 cannot subscribe to your own stream
    #register_subscription(2) # 200 OK
    #register_subscription(1) # 200 OK
    #request_primary()
    #my_streams()
    #get_streams(0)
    #get_streams(2)
    checkin()
    

# python .\client\tests\manual\server.py