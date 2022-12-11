# todo create config if no config present, use config if config present
import threading
from itertools import product
from functools import partial
import pandas as pd
import satori
from satori.apis.satori.pub import SatoriPubConn
from satori.apis.satori.sub import SatoriSubConn
from satori.engine.structs import SourceStreamTargets
import satori.engine.model.metrics as metrics
from satori.apis.wallet import Wallet
from satori.apis import disk
from satori.apis import memory
from satori.apis.ipfs import ipfsCli
from satori.apis.satori.server import SatoriServerClient


class StartupDag(object):
    ''' a DAG of startup tasks. '''

    def __init__(self, *args):
        super(StartupDag, self).__init__(*args)
        self.full = True

        self.ipfsDaemon
        self.wallet
        self.nodeDetails
        self.key
        self.subscriberKey
        self.publisherKey
        self.connection
        self.engine

    def start(self):
        if self.full:
            self.startIpfs()
            self.openWallet()
            self.checkin()
            self.sync()
            self.pubsub()
            self.engine()

    def startIpfs(self):
        thread = threading.Thread(target=ipfsCli.start, daemon=True)
        thread.start()
        self.ipfsDaemon = thread

    def openWallet(self):
        self.wallet = Wallet()()

    def checkin(self):
        self.nodeDetails = SatoriServerClient(self.wallet).checkin()
        self.key = self.nodeDetails.get('key')
        self.subscriberKey = self.nodeDetails.get('subscriber.key')
        self.publisherKey = self.nodeDetails.get('publisher.key')

    def sync(self):
        for pin in self.nodeDetails.get('pins'):
            ipfs = pin.get('ipfs')
            if ipfs:
                ipfsCli.get(
                    hash=ipfs
                    # 'parse "target" column into observation id: w.pubkey:s.source:s.name:s.target'
                    abspath=SourceStreamTargets(
                        stream=pin.get('target').split(':')[2],
                        targets=[pin.get('target').split(':')[3]],
                        source='|'.join(
                            pin.get('target').split(':')[0:2])))

    def pubsub(self):
        if self.key:
            self.connection = satori.init.establishConnection(self.key)
        elif self.subscriberKey and self.publisherKey:
            self.pubConn = satori.init.establishConnection(self.pubConn)
            self.subConn = satori.init.establishConnection(self.subConn)
        else:
            raise Exception('no key provided by satori server')

    def buildEngine(self):
        if self.key:
            self.engine = satori.init.getEngine(self.connection)
            self.engine.run()
        elif self.subscriberKey and self.publisherKey:
            self.engine = satori.init.getEngine(self.connection)
            self.engine.run()
        else:
            raise Exception('no key provided by satori server')
