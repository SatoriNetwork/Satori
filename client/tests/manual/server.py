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
            1: {'source': 'SATORI', 'author': '22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8', 'stream': 'stream1', 'target': 'target'},
            2: {'source': 'SATORI', 'author': '02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8', 'stream': 'stream1_p', 'target': 'target'},
            3: {'source': 'SATORI', 'author': '32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8', 'stream': 'stream3', 'target': 'target'},
            4: {'source': 'SATORI', 'author': '42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8', 'stream': 'stream4', 'target': 'target'},
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
            4: {
                'publisher': {'pubkey': '42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8'},
                # subscribe to this stream...
                'stream': fixtures.streams()[4],
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
# now manually fix stream 4 in the database to point to wallet 4
# now manually set the sanctioned to > 0 for streams 1, and 3
# now manually set the predicting for stream 2 to 1


def register_subscription(x: int):
    ''' subscribe to stream '''
    r = requests.post(
        'http://localhost:5002/register/subscription',
        headers=w.authPayload(asDict=True),
        json=json.dumps(fixtures.subscriptions()[x]))
    print(r.status_code, r.text)


register_subscription(1)  # primary
register_subscription(4)  # secondary


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
    # subscriptions by publications - used to init engine
    print('\npublications', j.get('subscriptions_by_publications'))
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


# >>> checkin()
# 200 {"key": "75hwPignMgTlefjBM3fJZr2Z2L86ioM69frY45c01adDyr5K6GcM/U6KJ9epjRN9nlNMsD/NmTIE09gE+M66e7TdsVkIab02YwcQUStXXMeRPngOgics1tQhSL4UG9beXqHRQ9ifDDULeBspaitKT7TQR1cGShw3o+tTlsPWZ8BHTTc43qYFaMFFcXWgP/GND4931KG738VhGQYL1BraJSrgon0bvDI3WHwDsurUln7ZlvYhcRDHUreMV6oMO2/1UuynnAo8DVHe2n3dxBTrerlhlFTRBUcR7oU2KmhY7jPiUMgcl1Vty/n4592L2mE+GQmSty7NkijBLmyWmusv+E3lp341v3Vre1k7Kie+U3HeVNp96As1ZVOQx03kKgCo14KyIX3NaxDiYDP461wOPvFYtojO8c/AEVcm2p0BIgJ8urQ509D0tCO4IzZtnlOHKsS/2tf36iYc22R3nWt+zLVSBqVNC0CzzyWBla+4km90lFZ3kP1oreKE/vhpIErzvjqtWfeLlqW++5Ge9UkKZaGxEQSbSPkfRxnQZk9kmv68QpRkTgwZ8QChkYxpPZLrvDRF6FYvtJtRrQxe9DTDPGktu9SvVRGMV5kp66O+E6AoYKCTP+IW4BvEr7oqXaQZQMAA0qlC/mjVOwd+uGaf/bbM+6ULVqG2YtEjABe7wEezMWZ/Ksk7CsFF471MfhDVUAmoccmsbm5zog2w9w7yBO89/BbkcxUPEL+/hcSx2EQowhQRKwyYHk8Jlv7suX0YB4O0Zrec3jPVgNGQGLstXl2r1AvAEtCN9klwMTzWK0e4/FHvP+yFT26cSW719iaxUZ4ZlccLd9r9+WaSK2NuPYwuifep7C/MY2joy9VnWNDykLwwEVB+PGjdvPLyMJq/ldAjq2dx30rS43wFVDGfrRBeugRixwqVUkUJf5akfwBn2JhEkCETK8Z5QiAdH6ZmeefQK4ztb33ag/BD3KELEpTZjrcFQA3UD9KbWPdB9O5r8KWHfTkVAXxyfaC9kWiT", "subscriber.key": "LTx/yQIbQi49KSUbS4hKxSn+jJB538zmKLxBnA4Y4soV457JHPfaeA4gAWjEGziZOtVaNf3yOG5CiiJxY4wNfaJYhWzeyPIDufTg8W82dhtKGPYdeRRqHiFC0ZqdbScDTdqxEi99W8DUBx5NJFiee3oGpoiLVfOjzgeIzzh3Vn3pDMKqDBPeEYwjxDPhS5KNzEiOt+plkAthJhpvAZTiofpiyXoGJ+gjmRCmz0dmlQJSNw/dNG79S8qmzCWKulH+Z5esq8zlYQHiQq5sEWkUpFoHYFfqeGjPXxikCB5gYqVbOGMAfRcKIoQHAqiDeDb4lzvL1tJJ6PXGtvkXqhoCdOG6QFpsi539x/CxEDl/QbTLccb4hsn9206Cuz0QTHXBvcKiXtqeJL2oTj60Mw1tGJdvdLT1sudHd0ODP926jWA+An4xuLltyDwiT6/KPuWuMTOxj5W9IKeY/3rWKp5r0nRwALBYJLsj6+hvup+CiVzrGk2n+6bRGQxVgZIO/P8I2KvZXfPv9YaSBAoWFBN7mPFT9jtp6nEaEUMBEI7pvlO9ko+2fzuXXHwYtMMCy+Qp9y1adfM0o3AQ4NV27QB7gDAN8OPywrrCXOy/yn3PvSM=", "publisher.key": "75hwPignMgTlefjBM3fJZr2Z2L86ioM69frY45c01adDyr5K6GcM/U6KJ9epjRN9nlNMsD/NmTIE09gE+M66e7TdsVkIab02YwcQUStXXMeRPngOgics1tQhSL4UG9beXqHRQ9ifDDULeBspaitKT7TQR1cGShw3o+tTlsPWZ8BHTTc43qYFaMFFcXWgP/GND4931KG738VhGQYL1BraJSrgon0bvDI3WHwDsurUln7ZlvYhcRDHUreMV6oMO2/1UuynnAo8DVHe2n3dxBTrerlhlFTRBUcR7oU2KmhY7jPiUMgcl1Vty/n4592L2mE+GQmSty7NkijBLmyWmusv+E3lp341v3Vre1k7Kie+U3HeVNp96As1ZVOQx03kKgCo14KyIX3NaxDiYDP461wOPmydKTATSGcIyRMh/5vql24=", "subscriptions": "[{\"id\": 1, \"source\": \"SATORI\", \"author\": \"22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream1\", \"target\": \"target\", \"predicting\": null, \"sanctioned\": 1, \"ts\":
# \"2022-12-17 16:46:32.539\", \"reason_source\": \"SATORI\", \"reason_author\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"reason_stream\": \"stream1_p\", \"reason_target\": \"target\", \"reason_is_primary\": 1}, {\"id\": 3, \"source\": \"SATORI\", \"author\": \"32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream3\", \"target\": \"target\", \"predicting\": null, \"sanctioned\": 1, \"ts\": \"2022-12-17 16:46:36.692\", \"reason_source\": \"SATORI\", \"reason_author\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"reason_stream\": \"stream3_p\", \"reason_target\": \"target\", \"reason_is_primary\": 1},
# {\"id\": 4, \"source\": \"SATORI\", \"author\": \"42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream4\", \"target\": \"target\", \"predicting\": null, \"sanctioned\": null, \"ts\": \"2022-12-17 16:46:38.765\", \"reason_source\": \"SATORI\", \"reason_author\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"reason_stream\": \"stream1_p\", \"reason_target\": \"target\", \"reason_is_primary\": 0}, {\"id\": 4, \"source\": \"SATORI\", \"author\":
# \"42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream4\", \"target\": \"target\", \"predicting\": null, \"sanctioned\": null, \"ts\": \"2022-12-17 16:46:38.765\", \"reason_source\": \"SATORI\", \"reason_author\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"reason_stream\": \"stream3_p\", \"reason_target\": \"target\", \"reason_is_primary\": 0}]", "publications": "[{\"id\": 2,
# \"source\": \"SATORI\", \"author\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream1_p\", \"target\": \"target\", \"predicting\": 1, \"sanctioned\": null, \"ts\": \"2022-12-17 16:46:34.606\", \"predicting_source\": \"SATORI\", \"predicting_author\": \"22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"predicting_stream\": \"stream1\", \"predicting_target\": \"target\"}, {\"id\":
# 5, \"source\": \"SATORI\", \"author\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream3_p\", \"target\": \"target\", \"predicting\": 3, \"sanctioned\": null, \"ts\": \"2022-12-17 16:59:50.523\", \"predicting_source\": \"SATORI\", \"predicting_author\": \"32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"predicting_stream\": \"stream3\", \"predicting_target\": \"target\"}]", "pins": "[]", "versions": {"server": "0.0.1", "client": "0.0.1"}}
#
# key 75hwPignMgTlefjBM3fJZr2Z2L86ioM69frY45c01adDyr5K6GcM/U6KJ9epjRN9nlNMsD/NmTIE09gE+M66e7TdsVkIab02YwcQUStXXMeRPngOgics1tQhSL4UG9beXqHRQ9ifDDULeBspaitKT7TQR1cGShw3o+tTlsPWZ8BHTTc43qYFaMFFcXWgP/GND4931KG738VhGQYL1BraJSrgon0bvDI3WHwDsurUln7ZlvYhcRDHUreMV6oMO2/1UuynnAo8DVHe2n3dxBTrerlhlFTRBUcR7oU2KmhY7jPiUMgcl1Vty/n4592L2mE+GQmSty7NkijBLmyWmusv+E3lp341v3Vre1k7Kie+U3HeVNp96As1ZVOQx03kKgCo14KyIX3NaxDiYDP461wOPvFYtojO8c/AEVcm2p0BIgJ8urQ509D0tCO4IzZtnlOHKsS/2tf36iYc22R3nWt+zLVSBqVNC0CzzyWBla+4km90lFZ3kP1oreKE/vhpIErzvjqtWfeLlqW++5Ge9UkKZaGxEQSbSPkfRxnQZk9kmv68QpRkTgwZ8QChkYxpPZLrvDRF6FYvtJtRrQxe9DTDPGktu9SvVRGMV5kp66O+E6AoYKCTP+IW4BvEr7oqXaQZQMAA0qlC/mjVOwd+uGaf/bbM+6ULVqG2YtEjABe7wEezMWZ/Ksk7CsFF471MfhDVUAmoccmsbm5zog2w9w7yBO89/BbkcxUPEL+/hcSx2EQowhQRKwyYHk8Jlv7suX0YB4O0Zrec3jPVgNGQGLstXl2r1AvAEtCN9klwMTzWK0e4/FHvP+yFT26cSW719iaxUZ4ZlccLd9r9+WaSK2NuPYwuifep7C/MY2joy9VnWNDykLwwEVB+PGjdvPLyMJq/ldAjq2dx30rS43wFVDGfrRBeugRixwqVUkUJf5akfwBn2JhEkCETK8Z5QiAdH6ZmeefQK4ztb33ag/BD3KELEpTZjrcFQA3UD9KbWPdB9O5r8KWHfTkVAXxyfaC9kWiT
#
# subscriptions [
#	{"id": 1, "source": "SATORI", "author": "22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream1", "target": "target", "predicting": null, "sanctioned": 1, "ts": "2022-12-17 16:46:32.539", "reason_source": "SATORI", "reason_author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "reason_stream": "stream1_p", "reason_target": "target", "reason_is_primary": 1},
#	{"id": 3, "source": "SATORI", "author": "32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream3", "target": "target", "predicting": null, "sanctioned": 1, "ts": "2022-12-17 16:46:36.692", "reason_source": "SATORI", "reason_author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "reason_stream": "stream3_p", "reason_target": "target", "reason_is_primary": 1},
#	{"id": 4, "source": "SATORI", "author": "42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream4", "target": "target", "predicting": null, "sanctioned": null, "ts": "2022-12-17 16:46:38.765", "reason_source": "SATORI", "reason_author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "reason_stream": "stream1_p", "reason_target": "target", "reason_is_primary": 0},
# 	{"id": 4, "source": "SATORI", "author": "42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream4", "target": "target", "predicting": null, "sanctioned": null, "ts": "2022-12-17 16:46:38.765", "reason_source": "SATORI", "reason_author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "reason_stream": "stream3_p", "reason_target": "target", "reason_is_primary": 0}]
#
# publications [
#	{"id": 2, "source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream1_p", "target": "target", "predicting": 1, "sanctioned": null, "ts": "2022-12-17 16:46:34.606", "predicting_source": "SATORI", "predicting_author": "22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "predicting_stream": "stream1", "predicting_target": "target"},
# 	{"id": 5, "source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream3_p", "target": "target", "predicting": 3, "sanctioned": null, "ts": "2022-12-17 16:59:50.523", "predicting_source": "SATORI", "predicting_author": "32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "predicting_stream": "stream3", "predicting_target": "target"}]
#
# publications None
#
# pins []
#
# server version 0.0.1
#
# client version 0.0.1
#
# key {
#    "publisher": [
#		{"source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream1_p", "target": "target"},
# 		{"source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream3_p", "target": "target"}],
#    "subscriptions": [
#	   	{"source": "SATORI", "author": "22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream1", "target": "target"},
#	   	{"source": "SATORI", "author": "32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream3", "target": "target"},
# 		{"source": "SATORI", "author": "42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream4", "target": "target"}]}
