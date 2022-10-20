import requests 

def payloads():
    from satori import Wallet
    w = Wallet()()             
    requests.post('http://localhost:5002/register/wallet', json=w.registerPayload())
    #from satori.apis import system
    #w.authPayload()
    #'{"message": "2022-10-20 20:14:02.322147", "pubkey": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "address": "RPBG9hf93Uge2SgZt4K1mRNyJeTTcKe8kt", "signature": "IHi9HH21rED8hZsTio6Q488qi/cSZ5DRgWSN9rsqTSGcJiXk3v1qECXVYB2ptcTk5dGThqpCmqJCXP2/gR4ubL8="}'
    #system.devicePayload()
    #{'ram_total_gb': 32, 'ram_available_percent': 49.16639057975354, 'cpu': 8, 'disk_total': 475, 'disk_free': 66, 'bandwidth': 'unknown'}

if __name__ == '__main__':
    payloads();