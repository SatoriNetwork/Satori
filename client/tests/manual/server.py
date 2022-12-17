'''
Here's plan for the server - python server, you checkin with it, it returns a key you use to make a websocket connection with the pubsub server.
'''
import json
import requests
from satori import Wallet
w = Wallet()()


class fixtures():
    @staticmethod
    def streams():
        return {
            0: {},
            1: {'source': 'SATORI', 'author': '2', 'stream': 'stream1', 'target': 'target'},
            2: {'source': 'SATORI', 'author': '1', 'stream': 'stream1_p', 'target': 'target'},
            3: {'source': 'SATORI', 'author': '3', 'stream': 'stream3', 'target': 'target'},
            4: {'source': 'SATORI', 'author': '4', 'stream': 'stream4', 'target': 'target'},
        }

    @staticmethod
    def subscriptions():
        return {
            0: {},
            1: {
                'publisher': {'pubkey': '22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8'},
                # subscribe to this stream...
                'stream': fixtures.streams()[1],
                # because I need it to produce this prediction stream...
                'reason': fixtures.streams()[2],
            },
        }


def register_wallet():
    r = requests.post(
        'http://localhost:5002/register/wallet',
        headers=w.authPayload(asDict=True),
        json=w.registerPayload())
    print(r.status_code, r.text)


register_wallet()
# now, go make a new wallet in the database manually starting with 22...
# now, go make a new wallet in the database manually starting with 32...
# now, go make a new wallet in the database manually starting with 42...


def register_stream(x: int):
    ''' publish raw data'''
    r = requests.post(
        'http://localhost:5002/register/stream',
        headers=w.authPayload(asDict=True),
        json=json.dumps(fixtures.streams()[x]))
    print(r.status_code, r.text)


register_stream(1)
register_stream(2)
register_stream(3)
register_stream(4)
# now manually fix stream 1 in the database to point to wallet 2
# now manually fix stream 3 in the database to point to wallet 3
# now manually fix stream 4 in the database to point to wallet  4
# now manually set the sanctioned to > 0 for streams 1, 3, and 4
# now manually set the predicting for stream 2 to 1


def register_subscription(x: int):
    ''' subscribe to stream '''
    r = requests.post(
        'http://localhost:5002/register/subscription',
        headers=w.authPayload(asDict=True),
        json=json.dumps(fixtures.subscriptions()[x]))
    print(r.status_code, r.text)


register_subscription(1)


def request_primary():
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.get(
        'http://localhost:5002/request/primary',
        headers=w.authPayload(asDict=True))
    print(r.status_code, r.text)


request_primary()


def get_streams(x: int):
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.post(
        'http://localhost:5002/get/streams',
        headers=w.authPayload(asDict=True),
        json=json.dumps(fixtures.streams()[x]))
    print(r.status_code, r.text)


get_streams(1)
get_streams(2)
get_streams(3)
get_streams(4)


def my_streams():
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.post(
        'http://localhost:5002/my/streams',
        headers=w.authPayload(asDict=True),
        json='{}')  # if you want a subset of your streams...
    print(r.status_code, r.text)


my_streams()


def my_publications():
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.post(
        'http://localhost:5002/my/publications',
        headers=w.authPayload(asDict=True))
    print(r.status_code, r.text)


my_publications()


def my_subscriptions():
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.post(
        'http://localhost:5002/my/subscriptions',
        headers=w.authPayload(asDict=True))
    print(r.status_code, r.text)


my_subscriptions()


def my_subscriptions_pins():
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.post(
        'http://localhost:5002/my/subscriptions/pins',
        headers=w.authPayload(asDict=True))
    print(r.status_code, r.text)


my_subscriptions_pins()


def checkin():
    r = requests.post(
        'http://localhost:5002/checkin',
        headers=w.authPayload(asDict=True),
        json=w.registerPayload())
    print(r.status_code, r.text)
    j = r.json()
    # use subscriptions to initialize engine
    print('\nkey', j.get('key'))
    # use subscriptions to initialize engine
    print('\nsubscriptions', j.get('subscriptions'))
    # use publications to initialize engine
    print('\npublications', j.get('publications'))
    # use pins to initialize engine and update any missing data
    print('\npins', j.get('pins'))
    # use server version to use the correct api
    print('\nserver version', j.get('versions', {}).get('server'))
    # use client version to know when to update the client
    print('\nclient version', j.get('versions', {}).get('client'))
    from satoriserver.utils import Crypt
    print('\nkey', Crypt().decrypt(
        toDecrypt=j.get('key'),
        key='thiskeyisfromenv',
        clean=True))


checkin()

if __name__ == '__main__':
    # register_wallet()
    # register_stream()
    # register_subscription(1) # 400 cannot subscribe to your own stream
    # register_subscription(2) # 200 OK
    # register_subscription(1) # 200 OK
    # request_primary()
    # my_streams()
    # get_streams(0)
    # get_streams(2)
    checkin()


# python .\client\tests\manual\server.py
