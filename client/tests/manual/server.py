import json
import requests 
from satori import Wallet
w = Wallet()()             

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
    r = requests.post(
        'http://localhost:5002/register/stream',
        headers=w.authPayload(asDict=True),
        json=json.dumps({'source': 'test', 'name': 'test2', 'target':'target'}))
    print(r.status_code, r.text)
    
def request_primary():
    r = requests.post(
        'http://localhost:5002/request/primary',
        headers=w.authPayload(asDict=True),
        json=json.dumps({'id': '1'}))
    print(r.status_code, r.text)    

if __name__ == '__main__':
    #register_wallet()
    #register_stream()
    request_primary()
    