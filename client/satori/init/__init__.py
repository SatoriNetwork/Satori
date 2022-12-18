# todo create config if no config present, use config if config present
import threading
from itertools import product
from functools import partial
import pandas as pd
import satori
from satori.apis.satori.pubsub import SatoriPubSubConn
# from satori.apis.satori.pub import SatoriPubConn
# from satori.apis.satori.sub import SatoriSubConn
from satori.engine.structs import StreamId, HyperParameter
from satori.engine import ModelManager
from satori.engine.view import View
import satori.engine.model.metrics as metrics
from satori.apis.wallet import Wallet
from satori.apis import disk
from satori.apis import memory
from satori.apis.ipfs import ipfsCli
from satori.apis.satori.server import SatoriServerClient
from satori.init.start import StartupDag


def establishConnection(pubkey: str, key: str, startupDag: StartupDag):
    ''' establishes a connection to the satori server, returns connection object '''

    def router(response: str):
        '''
        response needs to tell me what stream this is for, and what the value is
        the default router should accept the message and hold it in memory until
        the ipfs sync process is complete. Once it is complete it should send
        each message in reserve to the system that saves it to disk and routes
        it to the engine.
        '''

        def saveToDisk():
            ''' save to disk '''
            pass

        def routeToEngine():
            ''' route to engine '''
            pass

        # add to reserve.topic
        # if response.topic in startupDag.synced:
        #    for item in reserve.topic:
        #        # send to system that saves it to disk
        #        #saveToDisk()
        #        # send it to engine
        #        #routeToEngine()

    return SatoriPubSubConn(
        uid=pubkey,
        router=router,
        payload=key)
    # payload={
    #    'publisher': ['stream-a'],
    #    'subscriptions': ['stream-b', 'stream-c', 'stream-d']})


# accept optional data necessary to generate models data and learner


def getEngine(subscriptions: list[StreamId], publications: list[StreamId]):
    '''
    called by the flask app to start the Engine.
    returns None or Engine.

    returns None if no memory of data or models is found (first run)
    returns Engine if memory of data or models is found or provided.
    '''

    def generateDataManager():
        ''' generates DataManager from data on disk '''
        return satori.DataManager(disk=disk.Disk())

    def generateModelManager():
        ''' generate a set of Model(s) for Engine '''

        def generateCombinedFeature(
            df: pd.DataFrame = None,
            columns: list[tuple] = None,
            prefix='Diff'
        ):
            '''
            example of making a feature out of data you know ahead of time.
            most of the time you don't know what kinds of data you'll get...
            '''
            def name():
                return (columns[0][0], columns[0][1], f'{prefix}{columns[0][2]}{columns[1][2]}')

            if df is None:
                return name()

            columns = columns or []
            feature = df.loc[:, columns[0]] - df.loc[:, columns[1]]
            feature.name = name()
            return feature

        # these will be sensible defaults based upon the patterns in the data
        kwargs = {
            'hyperParameters': [
                HyperParameter(
                    name='n_estimators',
                    value=300,
                    kind=int,
                    limit=100,
                    minimum=200,
                    maximum=5000),
                HyperParameter(
                    name='learning_rate',
                    value=0.3,
                    kind=float,
                    limit=.05,
                    minimum=.01,
                    maximum=.1),
                HyperParameter(
                    name='max_depth',
                    value=6,
                    kind=int,
                    limit=1,
                    minimum=10,
                    maximum=2), ],
            'metrics':  {
                # raw data features
                'Raw': metrics.rawDataMetric,
                # daily percentage change, 1 day ago, 2 days ago, 3 days ago...
                **{f'Daily{i}': partial(metrics.dailyPercentChangeMetric, yesterday=i) for i in list(range(1, 31))},
                # rolling period transformation percentage change, max of the last 7 days, etc...
                **{f'Rolling{tx[0:3]}{i}': partial(metrics.rollingPercentChangeMetric, window=i, transformation=tx)
                    for tx, i in product('sum() max() min() mean() median() std()'.split(), list(range(2, 21)))},
                # rolling period transformation percentage change, max of the last 50 or 70 days, etc...
                **{f'Rolling{tx[0:3]}{i}': partial(metrics.rollingPercentChangeMetric, window=i, transformation=tx)
                    for tx, i in product('sum() max() min() mean() median() std()'.split(), list(range(22, 90, 7)))}
            }}
        return {
            ModelManager(
                variable=StreamId(
                    source=publication.get('predicting_source'),
                    author=publication.get('predicting_author'),
                    stream=publication.get('predicting_stream'),
                    target=publication.get('predicting_target')),
                output=publication,
                targets=[
                    StreamId(
                        source=subscription.source,
                        author=subscription.author,
                        stream=subscription.stream,
                        targets=subscription.target)
                    # will be unique by publication, no need to enforce
                    for subscription in subscriptions
                    if (
                        subscription.get('reason_source') == publication.get('source') and
                        subscription.get('reason_author') == publication.get('author') and
                        subscription.get('reason_stream') == publication.get('stream') and
                        subscription.get(
                            'reason_target') == publication.get('target')
                    )],
                disk=disk.Disk(),
                memory=memory.Memory,
                **kwargs)
            for publication in publications
        }

    return satori.Engine(
        data=generateDataManager(),
        models=generateModelManager()
    )
