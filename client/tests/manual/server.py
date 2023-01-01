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
            1: {'source': 'SATORI', 'pubkey': '22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8', 'stream': 'stream1', 'target': 'target'},
            2: {'source': 'SATORI', 'pubkey': '02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8', 'stream': 'stream1_p', 'target': 'target'},
            3: {'source': 'SATORI', 'pubkey': '32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8', 'stream': 'stream3', 'target': 'target'},
            4: {'source': 'SATORI', 'pubkey': '42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8', 'stream': 'stream4', 'target': 'target'},
        }

    @staticmethod
    def subscriptions():
        return {
            0: {},
            1: {
                'author': {'pubkey': '22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8'},
                # subscribe to this stream...
                'stream': fixtures.streams()[1],
                # because I need it to produce this prediction stream...
                'reason': fixtures.streams()[2],
            },
            4: {
                'author': {'pubkey': '42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8'},
                # subscribe to this stream...
                'stream': fixtures.streams()[4],
                # because I need it to produce this prediction stream...
                'reason': fixtures.streams()[2],
            },
        }

    @staticmethod
    def pins():
        return {
            0: {},
            1: {'author': {'pubkey': '22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8'}, 'stream': fixtures.streams()[1], 'ipns': 'ipns', 'ipfs': 'ipfs', 'disk': 1, 'count': 27},
            2: {'author': {'pubkey': '02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8'}, 'stream': fixtures.streams()[2], 'ipns': 'ipns', 'ipfs': 'ipfs', 'disk': 2, 'count': 27},
            3: {'author': {'pubkey': '32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8'}, 'stream': fixtures.streams()[3], 'ipns': 'ipns', 'ipfs': 'ipfs', 'disk': 3, 'count': 27},
            4: {'author': {'pubkey': '42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8'}, 'stream': fixtures.streams()[4], 'ipns': 'ipns', 'ipfs': 'ipfs', 'disk': 4, 'count': 27},
        }

    @staticmethod
    def observations():
        return {
            0: {},
            1: {'stream': fixtures.streams()[1], 'value': 1, 'time': 'time1'},
            2: {'stream': fixtures.streams()[2], 'value': 2, 'time': 'time2'},
            3: {'stream': fixtures.streams()[3], 'value': 3, 'time': 'time3'},
            4: {'stream': fixtures.streams()[4], 'value': 4, 'time': 'time4'},
        }


def register_wallet():
    r = requests.post(
        'http://localhost:5002/register/wallet',
        headers=w.authPayload(asDict=True),
        json=w.registerPayload())
    print(r.status_code, r.text)


def register_stream(x: int):
    ''' publish raw data'''
    r = requests.post(
        'http://localhost:5002/register/stream',
        headers=w.authPayload(asDict=True),
        json=json.dumps(fixtures.streams()[x]))
    print(r.status_code, r.text)


def register_subscription(x: int):
    ''' subscribe to stream '''
    r = requests.post(
        'http://localhost:5002/register/subscription',
        headers=w.authPayload(asDict=True),
        json=json.dumps(fixtures.subscriptions()[x]))
    print(r.status_code, r.text)


def register_pins(x: int):
    ''' subscribe to stream '''
    r = requests.post(
        'http://localhost:5002/register/pin',
        headers=w.authPayload(asDict=True),
        json=json.dumps(fixtures.pins()[x]))
    print(r.status_code, r.text)


def register_observations(x: int):
    ''' subscribe to stream '''
    r = requests.post(
        'http://localhost:5002/register/observation',
        headers=w.authPayload(asDict=True),
        json=json.dumps(fixtures.observations()[x]))
    print(r.status_code, r.text)


def request_primary():
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.get(
        'http://localhost:5002/request/primary',
        headers=w.authPayload(asDict=True))
    print(r.status_code, r.text)


def get_streams(x: int):
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.post(
        'http://localhost:5002/get/streams',
        headers=w.authPayload(asDict=True),
        json=json.dumps(fixtures.streams()[x]))
    print(r.status_code, r.text)


def search_streams():
    r = requests.post('http://localhost:5002/search/1')
    print(r.status_code, r.text)


def my_streams():
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.post(
        'http://localhost:5002/my/streams',
        headers=w.authPayload(asDict=True),
        json='{}')  # if you want a subset of your streams...
    print(r.status_code, r.text)


def my_databasetest():
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.post(
        'http://localhost:5002/my/database/test',
        headers=w.authPayload(asDict=True),
        json='{}')  # if you want a subset of your streams...
    print(r.status_code, r.text)


def my_publications():
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.get(
        'http://localhost:5002/my/publications',
        headers=w.authPayload(asDict=True))
    print(r.status_code, r.text)


def my_subscriptions():
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.get(
        'http://localhost:5002/my/subscriptions',
        headers=w.authPayload(asDict=True))
    print(r.status_code, r.text)


def my_subscriptions_pins():
    ''' subscribe to primary data stream and and publish prediction '''
    r = requests.get(
        'http://localhost:5002/my/subscriptions/pins',
        headers=w.authPayload(asDict=True))
    print(r.status_code, r.text)


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


if __name__ != '__main__':
    register_wallet()
    # now, go make a new wallet in the database manually starting with 22...
    # now, go make a new wallet in the database manually starting with 32...
    # now, go make a new wallet in the database manually starting with 42...
    register_stream(1)
    register_stream(2)
    register_stream(3)
    register_stream(4)
    # now manually fix stream 1 in the database to point to wallet 2
    # now manually fix stream 3 in the database to point to wallet 3
    # now manually fix stream 4 in the database to point to wallet 4
    # now manually set the sanctioned to > 0 for streams 1, and 3
    # now manually set the predicting for stream 2 to 1
    register_subscription(1)  # primary
    register_subscription(4)  # secondary
    register_pins(2)  # on publication
    register_pins(3)  # subscription
    register_observations(2)
    register_observations(3)
    request_primary()
    get_streams(1)
    get_streams(2)
    get_streams(3)
    get_streams(4)
    search_streams()
    my_streams()
    my_databasetest()
    my_publications()
    my_subscriptions()
    my_subscriptions_pins()

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
# 200 {"key": "75hwPignMgTlefjBM3fJZr2Z2L86ioM69frY45c01adDyr5K6GcM/U6KJ9epjRN9nlNMsD/NmTIE09gE+M66e7TdsVkIab02YwcQUStXXMeRPngOgics1tQhSL4UG9beXqHRQ9ifDDULeBspaitKT7TQR1cGShw3o+tTlsPWZ8BHTTc43qYFaMFFcXWgP/GND4931KG738VhGQYL1BraJSrgon0bvDI3WHwDsurUln7ZlvYhcRDHUreMV6oMO2/1UuynnAo8DVHe2n3dxBTrerlhlFTRBUcR7oU2KmhY7jPiUMgcl1Vty/n4592L2mE+GQmSty7NkijBLmyWmusv+E3lp341v3Vre1k7Kie+U3HeVNp96As1ZVOQx03kKgCo14KyIX3NaxDiYDP461wOPvFYtojO8c/AEVcm2p0BIgJ8urQ509D0tCO4IzZtnlOHKsS/2tf36iYc22R3nWt+zJNXR3F5MBFCyZJsEiBjahfiUMLep3UFnQHIAj9ksuYg0meDlorL4TJIOGAXONt48czRGYK/k6DKyLcVoMJZFimzAYAdUVPgdgpO8Egw9F1oloEYHjJp31VU9sYWCQQCIdrqoVVucgMdSZySRNLJTCQ9q9BCsv304gJiyvaKqX/9Tw10RVJiYYc+UeH4AZLrINTE9zDB7D893U3Na4WBMbbRofk10IsoAwKPjaMItBrwSxZUyY5s3EddMFnuw33iNmfmdT8igAZEFoygGCKvpcrJbL1DbqGY/EjMAyaG8EjqbSXHnHyIbYYoeevP7JAs/HtYJE308DaY84i81NdaqvOEA6hI4iGrigXoepzdVkSjyM9VcPeP3lDeyvvVX1YopIJjv4Ang4v+iBKScbxYOa8Fcg8ctHOe+eLikyDeeuPaRbTiQcgEVxeNEVhdZhyoFzwiCF4F4cQSqZ5HOZOFPAlFlLUyRiD0yizU+cWVSCAxS5NP4kgi+7nMrQyJNUeUzStZp1wWLKQduHQPLmKuJkMZXR+y0B0tHh1e/XrGjRRL", "subscriber.key": "LTx/yQIbQi49KSUbS4hKxSn+jJB538zmKLxBnA4Y4soV457JHPfaeA4gAWjEGziZfVYG7NxRdO7qCVEyXSguPI6Ct4XZ2pbFgJT7ZLfy//ntABBPQ9zAU9Xb7dURE0XN29YjVHLI7aT8N0cV9n6sTtFXUp+maXKBFfx/iF1+UTUU1n5l0fI9tXA2fgEaLNzRXiHGBvcv0kyYECyn5YwJuPdKtU6QPOz2ue+u60hN88PFF1Y/SnCLv4560ntYiTx6Ok2KtnAphmTzuXWBdN4wmBzGGNBRJZocsbmcrtCpwpVohgqq6BijTOwZeyFrpMjISPGY64qXnoT1no5H2z+U62Nw9HSWH9oweMleF3+Pk/T7esvoJHUf/5y6OEOP5A7ku7GVHyR4+wyw+4rmlRMUbwwLFz2Sq5Eq++3DVoCqV2SWjv++oHwohyLDZcMUlf/qicizvfQ2th32OAX3tO7mobwTfYILdHZS8RdExio1vlucix+cb7RP4AnE8er7eSDu07sYE0osnOaFUUMqAVirkZAUe0QQfqS5CWJZ+tdUw6hfyJjzLikpSyvgIAS6V5/rV9TMSxo5O8evkZJ++x53j97r5+VH2k18VbQWiiYqh0M=", "publisher.key": "75hwPignMgTlefjBM3fJZr2Z2L86ioM69frY45c01adDyr5K6GcM/U6KJ9epjRN9nlNMsD/NmTIE09gE+M66e7TdsVkIab02YwcQUStXXMeRPngOgics1tQhSL4UG9beXqHRQ9ifDDULeBspaitKT7TQR1cGShw3o+tTlsPWZ8BHTTc43qYFaMFFcXWgP/GND4931KG738VhGQYL1BraJSrgon0bvDI3WHwDsurUln7ZlvYhcRDHUreMV6oMO2/1UuynnAo8DVHe2n3dxBTrerlhlFTRBUcR7oU2KmhY7jPiUMgcl1Vty/n4592L2mE+GQmSty7NkijBLmyWmusv+E3lp341v3Vre1k7Kie+U3HeVNp96As1ZVOQx03kKgCo14KyIX3NaxDiYDP461wOPmydKTATSGcIyRMh/5vql24=", "subscriptions": "[{\"source\": \"SATORI\", \"author\": \"22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream1\", \"target\": \"target\", \"sanctioned\":
# 1, \"tspredicting_source\": \"2022-12-23 20:43:12.022\", \"reason_author\": \"SATORI\", \"reason_stream\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"reason_target\": \"stream1_p\", \"reason_is_primary\": \"target\"},
# {\"source\": \"SATORI\", \"author\": \"32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream3\", \"target\": \"target\", \"sanctioned\": 1, \"tspredicting_source\": \"2022-12-23 20:43:16.185\", \"reason_author\": \"SATORI\", \"reason_stream\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"reason_target\": \"stream3_p\", \"reason_is_primary\": \"target\"}, {\"source\": \"SATORI\", \"author\": \"42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream4\", \"target\": \"target\",
# \"tspredicting_source\": \"2022-12-23 20:43:19.643\", \"reason_author\": \"SATORI\", \"reason_stream\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"reason_target\": \"stream1_p\", \"reason_is_primary\": \"target\"}]", "publications": "[{\"source\": \"SATORI\", \"author\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream1_p\", \"target\": \"target\", \"tspredicting_source\": \"2022-12-23 20:43:14.116\", \"predicting_author\": \"SATORI\", \"predicting_stream\": \"22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"predicting_target\": \"stream1\", \"reason_source\": \"target\"}, {\"source\": \"SATORI\", \"author\": \"02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream\": \"stream3_p\", \"target\": \"target\", \"tspredicting_source\": \"2022-12-23 20:52:02.472\", \"predicting_author\": \"SATORI\", \"predicting_stream\": \"32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"predicting_target\": \"stream3\", \"reason_source\": \"target\"}]", "pins": "[{\"ipns\": \"ipns\", \"ipfs\": \"ipfs\", \"disk\": 3, \"count\": 27, \"ts\": \"2022-12-23 22:22:22.717\", \"stream_source\": \"SATORI\", \"stream_author\": \"32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8\", \"stream_stream\": \"stream3\", \"stream_target\": \"target\"}]", "versions": {"server": "0.0.1", "client": "0.0.1"}}
#
# key 75hwPignMgTlefjBM3fJZr2Z2L86ioM69frY45c01adDyr5K6GcM/U6KJ9epjRN9nlNMsD/NmTIE09gE+M66e7TdsVkIab02YwcQUStXXMeRPngOgics1tQhSL4UG9beXqHRQ9ifDDULeBspaitKT7TQR1cGShw3o+tTlsPWZ8BHTTc43qYFaMFFcXWgP/GND4931KG738VhGQYL1BraJSrgon0bvDI3WHwDsurUln7ZlvYhcRDHUreMV6oMO2/1UuynnAo8DVHe2n3dxBTrerlhlFTRBUcR7oU2KmhY7jPiUMgcl1Vty/n4592L2mE+GQmSty7NkijBLmyWmusv+E3lp341v3Vre1k7Kie+U3HeVNp96As1ZVOQx03kKgCo14KyIX3NaxDiYDP461wOPvFYtojO8c/AEVcm2p0BIgJ8urQ509D0tCO4IzZtnlOHKsS/2tf36iYc22R3nWt+zJNXR3F5MBFCyZJsEiBjahfiUMLep3UFnQHIAj9ksuYg0meDlorL4TJIOGAXONt48czRGYK/k6DKyLcVoMJZFimzAYAdUVPgdgpO8Egw9F1oloEYHjJp31VU9sYWCQQCIdrqoVVucgMdSZySRNLJTCQ9q9BCsv304gJiyvaKqX/9Tw10RVJiYYc+UeH4AZLrINTE9zDB7D893U3Na4WBMbbRofk10IsoAwKPjaMItBrwSxZUyY5s3EddMFnuw33iNmfmdT8igAZEFoygGCKvpcrJbL1DbqGY/EjMAyaG8EjqbSXHnHyIbYYoeevP7JAs/HtYJE308DaY84i81NdaqvOEA6hI4iGrigXoepzdVkSjyM9VcPeP3lDeyvvVX1YopIJjv4Ang4v+iBKScbxYOa8Fcg8ctHOe+eLikyDeeuPaRbTiQcgEVxeNEVhdZhyoFzwiCF4F4cQSqZ5HOZOFPAlFlLUyRiD0yizU+cWVSCAxS5NP4kgi+7nMrQyJNUeUzStZp1wWLKQduHQPLmKuJkMZXR+y0B0tHh1e/XrGjRRL
#
# subscriptions [
#   {"source": "SATORI", "author": "22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream1", "target": "target", "sanctioned": 1, "tspredicting_source": "2022-12-23 20:43:12.022", "reason_author": "SATORI", "reason_stream": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "reason_target": "stream1_p", "reason_is_primary": "target"},
# 	{"source": "SATORI", "author": "32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream3", "target": "target", "sanctioned": 1, "tspredicting_source": "2022-12-23 20:43:16.185", "reason_author": "SATORI", "reason_stream": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "reason_target": "stream3_p", "reason_is_primary": "target"},
# 	{"source": "SATORI", "author": "42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream4", "target": "target", "tspredicting_source": "2022-12-23 20:43:19.643", "reason_author": "SATORI", "reason_stream": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "reason_target": "stream1_p", "reason_is_primary": "target"}]
#
# publications [
# 	{"source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream1_p", "target": "target", "tspredicting_source": "2022-12-23 20:43:14.116", "predicting_author": "SATORI", "predicting_stream": "22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "predicting_target": "stream1", "reason_source": "target"},
# 	{"source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream3_p", "target": "target", "tspredicting_source": "2022-12-23 20:52:02.472", "predicting_author": "SATORI", "predicting_stream": "32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "predicting_target": "stream3", "reason_source": "target"}]
#
# pins [
# {"ipns": "ipns", "ipfs": "ipfs", "disk": 3, "count": 27, "ts": "2022-12-23 22:22:22.717", "stream_source": "SATORI", "stream_author": "32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream_stream": "stream3", "stream_target": "target"}]
#
# server version 0.0.1
#
# client version 0.0.1
#
# key
# {"publisher": [
# 	{"source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream1_p", "target": "target"},
# 	{"source": "SATORI", "author": "02a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream3_p", "target": "target"}],
# "subscriptions": [
# 	{"source": "SATORI", "author": "42a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream4", "target": "target"},
# 	{"source": "SATORI", "author": "32a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream3", "target": "target"},
# 	{"source": "SATORI", "author": "22a85fb71485c6d7c62a3784c5549bd3849d0afa3ee44ce3f9ea5541e4c56402d8", "stream": "stream1", "target": "target"}]}
