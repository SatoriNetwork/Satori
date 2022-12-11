import json
import time
from satoriserver.utils import Crypt
from satori.apis.satori import SatoriPubSubConn


def run():
    wait = 20
    conn = Client(
        uid='pubkey-b',
        payload={
            'publisher': ['stream-b'],
            'subscriptions': ['stream-a', 'stream-c', 'stream-d']})
    while True:
        time.sleep(wait)
        conn.publish(topic='stream-b', data='data for stream-b')
        time.sleep(wait)
    conn.disconnect()


run()
