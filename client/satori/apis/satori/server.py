'''
Here's plan for the server - python server, you checkin with it,
it returns a key you use to make a websocket connection with the pubsub server.
'''
import json
import requests
'from satori import Wallet'


class SatoriServerClient(object):
    def __init__(
            self, wallet: 'Wallet', url: str = 'http://localhost:5002/',
            *args, **kwargs):
        super(SatoriServerClient, self).__init__(*args, **kwargs)
        self.wallet = wallet
        self.url = url

    def registerWallet(self):
        r = requests.post(
            self.url + '/register/wallet',
            headers=self.wallet.authPayload(asDict=True),
            json=self.wallet.registerPayload())
        r.raise_for_status()
        return r.json()

    def registerStream(self, stream: dict):
        ''' publish stream {'source': 'test', 'name': 'stream1', 'target': 'target'}'''
        r = requests.post(
            self.url + '/register/stream',
            headers=self.wallet.authPayload(asDict=True),
            json=json.dumps(stream))
        r.raise_for_status()
        return r.json()

    def registerSubscription(self, subscription: dict):
        ''' subscribe to stream '''
        r = requests.post(
            self.url + '/register/subscription',
            headers=self.wallet.authPayload(asDict=True),
            json=json.dumps(subscription))
        r.raise_for_status()
        return r.json()

    def requestPrimary(self):
        ''' subscribe to primary data stream and and publish prediction '''
        r = requests.get(
            self.url + '/request/primary',
            headers=self.wallet.authPayload(asDict=True))
        r.raise_for_status()
        return r.json()

    def getStreams(self, stream: dict):
        ''' subscribe to primary data stream and and publish prediction '''
        r = requests.post(
            self.url + '/get/streams',
            headers=self.wallet.authPayload(asDict=True),
            json=json.dumps(stream))
        r.raise_for_status()
        return r.json()

    def myStreams(self):
        ''' subscribe to primary data stream and and publish prediction '''
        r = requests.post(
            self.url + '/my/streams',
            headers=self.wallet.authPayload(asDict=True),
            json='{}')
        r.raise_for_status()
        return r.json()

    def checkin(self):
        r = requests.post(
            self.url + '/checkin',
            headers=self.wallet.authPayload(asDict=True),
            json=self.wallet.registerPayload())
        r.raise_for_status()
        print(r.status_code, r.text)
        j = r.json()
        # use subscriptions to initialize engine
        print('publications.key', j.get('publications.key'))
        print('subscriptions.key', j.get('subscriptions.key'))
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
        from satoriserver.utils import Crypt
        print('subscriptions.key', Crypt().decrypt(
            toDecrypt=j.get('subscriptions.key'),
            key='thiskeyisfromenv',
            clean=True))
        print('publications.key', Crypt().decrypt(
            toDecrypt=j.get('publications.key'),
            key='thiskeyisfromenv',
            clean=True))
        return r.json()
