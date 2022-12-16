# todo create config if no config present, use config if config present
import threading
from itertools import product
from functools import partial
import pandas as pd
import satori
from satori.apis.satori.pub import SatoriPubConn
from satori.apis.satori.sub import SatoriSubConn
from satori.engine.structs import StreamId
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
        self.synced = []

    def start(self):
        if self.full:
            self.startIpfs()
            self.openWallet()
            self.checkin()
            self.pubsub()
            self.sync()
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

    def pubsub(self):
        ''' establish a pubsub connection. '''
        if self.key:
            self.connection = satori.init.establishConnection(
                pubkey=self.wallet.publicKey, key=self.key, startupDag=self)
        # will removing the separate connection pattern.
        # elif self.subscriberKey and self.publisherKey:
        #    self.pubConn = satori.init.establishConnection(self.pubConn)
        #    self.subConn = satori.init.establishConnection(self.subConn)
        else:
            raise Exception('no key provided by satori server')

    def sync(self):
        '''
        download pins (by ipfs address) received from satori server.
        start with the ipfs that the oracle/stream author/publisher has pinned.
        if unable to download, ask the server for all the pins of that stream.
        the other pins will be reported by the subscribers of the stream.
        download them at random.

        context: before we begin this process we will subscribe to the pubsub
        server which will provide us with new observations while we're
        downloading the history. those will be held in reserve until this
        process completes successfully, then they will be processed and saved to
        disk as incrementals one at a time, like normal, so that at the 100
        count we combine just like normal. that way, if we got the history from
        a subscriber our ipfs should match theirs.
        '''

        # we should make the download run in parellel so using async functions
        # here. but in the meantime, we'll do them sequentially.
        for pin in self.nodeDetails.get('pins'):
            ipfs = pin.get('ipfs')
            topic = pin.get('target_stream').split('::')
            if ipfs:
                ipfsCli.get(
                    hash=ipfs,
                    abspath=disk.Disk(
                        id=StreamId(
                            source=topic[0],
                            author=topic[1],
                            stream=topic[2],
                            target=topic[3])).path())
                # this topic should match the pubsub topic
                # because when we get a message from the pubsub server
                # it will have a topic key that we must look for to see if that
                # datastream is done syncing.
                self.synced = [topic]

    def buildEngine(self):
        if self.key:
            self.engine = satori.init.getEngine(self.connection)
            self.engine.run()
        elif self.subscriberKey and self.publisherKey:
            self.engine = satori.init.getEngine(self.connection)
            self.engine.run()
        else:
            raise Exception('no key provided by satori server')
