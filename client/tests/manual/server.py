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

# Checkin Return:
#
# 200 {"key": "75hwPignMgTlefjBM3fJZr2Z2L86ioM69frY45c01adDyr5K6GcM/U6KJ9epjRN9nlNMsD/NmTIE09gE+M66e7TdsVkIab02YwcQUStXXMeRPngOgics1tQhSL4UG9beXqHRQ9ifDDULeBspaitKT7TQR1cGShw3o+tTlsPWZ8BHTTc43qYFaMFFcXWgP/GND4931KG738VhGQYL1BraJSrgon0bvDI3WHwDsurUln7ZlvYhcRDHUreMV6oMO2/1UuynnAo8DVHe2n3dxBTrerlhlFTRBUcR7oU2KmhY7jPiUMgcl1Vty/n4592L2mE+GQmSty7NkijBLmyWmusv+E3lp341v3Vre1k7Kie+U3HeVNp96As1ZVOQx03kKgCozH3U95AePPQdeSF7Ls4KCfJdXm4Fek8hmngzSSskao6c3sqf+Ok7Y9udelfCn98k6dOhW4h01LH7sj1YGKwmtTZ29J1z+My8FuLfj5MNvtpRGkH/lv5fqSNVtwJoj9hVSIQ9BUhN5RGww2csHSSb3st10ou83qG5x5mNI+B5C7b69VTn980d/CD3PXV4Hx4GRjcKMMTDfqBruxfoSVJooypctZuYOHZOgLZLEyNHKqfdVmmESIkF/R9V/urWhaogs6fGI3ioRAZf7HRHTY6m2WfzaFzDln9uO56fDfbYcZktYk16JERGqxNRuD+baAKCjIBvIbHYWkDStJ0qtYby/wm7Oe6HjIUL5xl1JvaJFVEohYLtge40CGKt7S50C5rLWn5o1trFxI7xkicP8Rq/1uKv1bNYY5AZqNGLdrvUcQk+AkacdktQJDeAxiGxAxVeSeD4rrsBwsDjqHOjqqm5zSAzHL+PC5JoaNunPr29HLeoLyK0YV6npC+DoqsxtW4wduJ0DDCYqyq9mA/pLZ9yj3d2ju35EUY9VbKWJJ2brJ+IsRop11VN67zd6FM4lhrbcbODFBV8pwEtBcEshnPTZmugLvPIp7ddhOz8oi1fZ+aefe47qFs3xDUYbOSbxsYrqbSbrrvgyHtt2skJ9nBUH3wknhHrN59u6BcY0S7mroM9EvVHwu+ZD/vljdoduEue1+rEIIk5tu+Kqg83kQTqHEI2/0kmaB/rg2iVI3mKQTKASh0QzmgJgP2vxnkQswWvrvonlJ5fN8BpMFMgI0edkPBFtoSVE61hskvPdGoYBY/d8Q5iXlAF/Pg5RWlsBOwx", "subscriber.key": "LTx/yQIbQi49KSUbS4hKxSn+jJB538zmKLxBnA4Y4soV457JHPfaeA4gAWjEGziZOtVaNf3yOG5CiiJxY4wNfaJYhWzeyPIDufTg8W82dhtKGPYdeRRqHiFC0ZqdbScDTdqxEi99W8DUBx5NJFiee3oGpoiLVfOjzgeIzzh3Vn3pDMKqDBPeEYwjxDPhS5KNzEiOt+plkAthJhpvAZTiofpiyXoGJ+gjmRCmz0dmlQJSNw/dNG79S8qmzCWKulH+Z5esq8zlYQHiQq5sEWkUpFoHYFfqeGjPXxikCB5gYqVbOGMAfRcKIoQHAqiDeDb4lzvL1tJJ6PXGtvkXqhoCdOG6QFpsi539x/CxEDl/QbTLccb4hsn9206Cuz0QTHXBvcKiXtqeJL2oTj60Mw1tGJdvdLT1sudHd0ODP926jWA+An4xuLltyDwiT6/KPuWuMTOxj5W9IKeY/3rWKp5r0nRwALBYJLsj6+hvup+CiVzrGk2n+6bRGQxVgZIO/P8I2KvZXfPv9YaSBAoWFBN7mPFT9jtp6nEaEUMBEI7pvlO9ko+2fzuXXHwYtMMCy+Qp9y1adfM0o3AQ4NV27QB7gDAN8OPywrrCXOy/yn3PvSM=", "publisher.key": "75hwPignMgTlefjBM3fJZr2Z2L86ioM69frY45c01adDyr5K6GcM/U6KJ9epjRN9nlNMsD/NmTIE09gE+M66e7TdsVkIab02YwcQUStXXMeRPngOgics1tQhSL4UG9beXqHRQ9ifDDULeBspaitKT7TQR1cGShw3o+tTlsPWZ8BHTTc43qYFaMFFcXWgP/GND4931KG738VhGQYL1BraJSrgon0bvDI3WHwDsurUln7ZlvYhcRDHUreMV6oMO2/1UuynnAo8DVHe2n3dxBTrerlhlFTRBUcR7oU2KmhY7jPiUMgcl1Vty/n4592L2mE+GQmSty7NkijBLmyWmusv+E3lp341v3Vre1k7Kie+U3HeVNp96As1ZVOQx03kKgCozH3U95AePPQdeSF7Ls4KCfJdXm4Fek8hmngzSSskao6c3sqf+Ok7Y9udelfCn98k6dOhW4h01LH7sj1YGKwmtTZ29J1z+My8FuLfj5MNvtpRGkH/lv5fqSNVtwJoj9hVSIQ9BUhN5RGww2csHSSb3st10ou83qG5x5mNI+B5C7b69VTn980d/CD3PXV4Hx4GRjcKMMTDfqBruxfoSVJooz5Gv244zH+pDHTGFU2YbTA=", "subscriptions": "[{\"id\": 1, \"source\": \"SATORI\", \"author\": \"22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream1\", \"target\": \"target\", \"predicting\": null, \"sanctioned\": 1, \"ts\":
# \"2022-12-17 16:46:32.539\"}, {\"id\": 3, \"source\": \"SATORI\", \"author\": \"32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream3\", \"target\": \"target\", \"predicting\": null, \"sanctioned\": 1, \"ts\": \"2022-12-17 16:46:36.692\"}, {\"id\": 4, \"source\": \"SATORI\", \"author\": \"42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream4\", \"target\": \"target\", \"predicting\": null, \"sanctioned\": 1, \"ts\": \"2022-12-17 16:46:38.765\"}]", "publications": "[{\"id\": 2, \"source\": \"SATORI\", \"author\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream1_p\", \"target\": \"target\", \"predicting\": 1, \"sanctioned\": null, \"ts\": \"2022-12-17 16:46:34.606\"}, {\"id\": 5, \"source\": \"SATORI\",
# \"author\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream3_p\", \"target\": \"target\", \"predicting\": 3, \"sanctioned\": null, \"ts\": \"2022-12-17 16:59:50.523\"}, {\"id\": 6, \"source\": \"SATORI\", \"author\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream4_p\", \"target\": \"target\", \"predicting\": 4, \"sanctioned\": null, \"ts\": \"2022-12-17 17:35:47.996\"}]", "pins": "[]", "versions": {"server": "0.0.1",
# "client": "0.0.1"}}
#
# key 75hwPignMgTlefjBM3fJZr2Z2L86ioM69frY45c01adDyr5K6GcM/U6KJ9epjRN9nlNMsD/NmTIE09gE+M66e7TdsVkIab02YwcQUStXXMeRPngOgics1tQhSL4UG9beXqHRQ9ifDDULeBspaitKT7TQR1cGShw3o+tTlsPWZ8BHTTc43qYFaMFFcXWgP/GND4931KG738VhGQYL1BraJSrgon0bvDI3WHwDsurUln7ZlvYhcRDHUreMV6oMO2/1UuynnAo8DVHe2n3dxBTrerlhlFTRBUcR7oU2KmhY7jPiUMgcl1Vty/n4592L2mE+GQmSty7NkijBLmyWmusv+E3lp341v3Vre1k7Kie+U3HeVNp96As1ZVOQx03kKgCozH3U95AePPQdeSF7Ls4KCfJdXm4Fek8hmngzSSskao6c3sqf+Ok7Y9udelfCn98k6dOhW4h01LH7sj1YGKwmtTZ29J1z+My8FuLfj5MNvtpRGkH/lv5fqSNVtwJoj9hVSIQ9BUhN5RGww2csHSSb3st10ou83qG5x5mNI+B5C7b69VTn980d/CD3PXV4Hx4GRjcKMMTDfqBruxfoSVJooypctZuYOHZOgLZLEyNHKqfdVmmESIkF/R9V/urWhaogs6fGI3ioRAZf7HRHTY6m2WfzaFzDln9uO56fDfbYcZktYk16JERGqxNRuD+baAKCjIBvIbHYWkDStJ0qtYby/wm7Oe6HjIUL5xl1JvaJFVEohYLtge40CGKt7S50C5rLWn5o1trFxI7xkicP8Rq/1uKv1bNYY5AZqNGLdrvUcQk+AkacdktQJDeAxiGxAxVeSeD4rrsBwsDjqHOjqqm5zSAzHL+PC5JoaNunPr29HLeoLyK0YV6npC+DoqsxtW4wduJ0DDCYqyq9mA/pLZ9yj3d2ju35EUY9VbKWJJ2brJ+IsRop11VN67zd6FM4lhrbcbODFBV8pwEtBcEshnPTZmugLvPIp7ddhOz8oi1fZ+aefe47qFs3xDUYbOSbxsYrqbSbrrvgyHtt2skJ9nBUH3wknhHrN59u6BcY0S7mroM9EvVHwu+ZD/vljdoduEue1+rEIIk5tu+Kqg83kQTqHEI2/0kmaB/rg2iVI3mKQTKASh0QzmgJgP2vxnkQswWvrvonlJ5fN8BpMFMgI0edkPBFtoSVE61hskvPdGoYBY/d8Q5iXlAF/Pg5RWlsBOwx
#
# subscriptions [
#	{"id": 1, "source": "SATORI", "author": "22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream1", "target": "target", "predicting": null, "sanctioned": 1, "ts": "2022-12-17 16:46:32.539"},
#	{"id": 3, "source": "SATORI", "author": "32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream3", "target": "target", "predicting": null, "sanctioned": 1, "ts": "2022-12-17 16:46:36.692"},
# {"id": 4, "source": "SATORI", "author": "42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream4", "target": "target", "predicting": null, "sanctioned": 1, "ts": "2022-12-17 16:46:38.765"}]
#
# publications [
#	{"id": 2, "source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream1_p", "target": "target", "predicting": 1, "sanctioned": null, "ts": "2022-12-17 16:46:34.606"},
#	{"id": 5, "source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream3_p", "target": "target", "predicting": 3, "sanctioned": null, "ts": "2022-12-17 16:59:50.523"},
# {"id": 6, "source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream4_p", "target": "target", "predicting": 4, "sanctioned": null, "ts": "2022-12-17 17:35:47.996"}]
#
# pins []
#
# server version 0.0.1
#
# client version 0.0.1
#
# key {"publisher": [
#   {"source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream1_p", "target": "target"},
#   {"source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream3_p", "target": "target"},
#   {"source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream4_p", "target": "target"}],
# "subscriptions": [
#   {"source": "SATORI", "author": "22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream1", "target": "target"},
#   {"source": "SATORI", "author": "32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream3", "target": "target"},
#   {"source": "SATORI", "author": "42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream4", "target": "target"}]}
