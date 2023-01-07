# todo create config if no config present, use config if config present
import time
import threading
import satori
from satori.concepts.structs import StreamId
from satori.apis import disk
from satori.apis.wallet import Wallet
from satori.apis.ipfs import ipfsCli
from satori.apis.satori.server import SatoriServerClient
from satori.apis.satori.pubsub import SatoriPubSubConn


class StartupDag(object):
    ''' a DAG of startup tasks. '''

    def __init__(self, *args):
        super(StartupDag, self).__init__(*args)
        self.full = True
        self.ipfsDaemon = None
        self.paused = False
        self.pauseThread = None
        self.wallet = None
        self.details = None
        self.key = None
        self.connection: SatoriPubSubConn
        self.engine: satori.engine.Engine
        self.publications: list[StreamId] = []
        self.subscriptions: list[StreamId] = []

    def start(self):
        ''' start the satori engine. '''
        if self.full:
            self.startIpfs()
            self.openWallet()
            self.checkin()
            self.buildEngine()
            self.pubsub()
            self.downloadDatasets()

    def startIpfs(self):
        thread = threading.Thread(target=ipfsCli.start, daemon=True)
        thread.start()
        self.ipfsDaemon = thread

    def openWallet(self):
        self.wallet = Wallet()()

    def checkin(self):
        self.details = SatoriServerClient(self.wallet).checkin()
        self.key = self.details.get('key')
        self.subscriberKey = self.details.get('subscriber.key')
        self.publisherKey = self.details.get('publisher.key')
        self.publications = [
            StreamId.fromMap(map=x) for x in self.details.get('publications')]
        self.subscriptions = [
            StreamId.fromMap(map=x) for x in self.details.get('subscriptions')]

    def buildEngine(self):
        ''' start the engine, it will run w/ what it has til ipfs is synced '''
        self.engine = satori.init.getEngine(
            subscriptions=self.subscriptions,
            publications=self.publications,
            startup=self)
        self.engine.run()

    def pubsub(self):
        ''' establish a pubsub connection. '''
        if self.key:
            self.connection = satori.init.establishConnection(
                pubkey=self.wallet.publicKey, key=self.key, startupDag=self)
        else:
            raise Exception('no key provided by satori server')

    def downloadDatasets(self):
        '''
        download pins (by ipfs address) received from satori server.
        start with the ipfs that the oracle/stream author/publisher has pinned.
        '''

        # we should make the download run in parellel so using async functions
        # here. but in the meantime, we'll do them sequentially.
        for pin in self.details.get('pins'):
            ipfs = pin.get('ipfs')
            data = disk.Disk(
                id=StreamId(
                    source=pin.get('stream_source'),
                    author=pin.get('stream_author'),
                    stream=pin.get('stream_stream'),
                    target=pin.get('stream_target')))

            if ipfs:
                # TODO:
                # if this fails ask the server for all the pins of this stream.
                # the other pins will be reported by the subscribers. download
                # them at random.
                now = time.time()
                ipfsCli.get(
                    hash=ipfs,
                    abspath=data.path(temp=True))
                data.mergeTemp(time=now)

    def pause(self, timeout: int = 60):
        ''' pause the engine. '''
        def pauseEngineFor():
            # self.engine.pause()
            self.paused = True
            time.sleep(timeout)
            # self.engine.unpause()
            self.paused = False
            self.pauseThread = None

        thread = threading.Thread(target=pauseEngineFor, daemon=True)
        thread.start()
        self.pauseThread = thread

    def unpause(self):
        ''' pause the engine. '''
        # self.engine.unpause()
        self.paused = False
        self.pauseThread = None
