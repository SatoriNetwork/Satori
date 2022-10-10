# todo create config if no config present, use config if config present
import threading
from itertools import product
from functools import partial
import pandas as pd
import satori

from satori.lib.engine.structs import SourceStreamTarget
import satori.lib.engine.model.metrics as metrics
from satori.lib.apis import disk
from satori.lib.apis import memory
from satori.lib.wallet import Wallet
from satori.lib.apis.server import ClientConnection
from satori.lib.apis.ipfs import cli as ipfs

def startIPFS():
    thread = threading.Thread(target=ipfs.start, daemon=True)
    thread.start()
    return thread 

def establishConnection(wallet: Wallet):
    ''' establishes a connection to the satori server, returns connection object '''
    return ClientConnection(payload=wallet.authPayload())
    # todo send this at some point
    #systemPayload = satori.apis.system.getPayload()
    
# accept optional data necessary to generate models data and learner
def getEngine(connection):
    # todo: use connection if no config present to set yourself up correctly (connnection will provide streams to subscribe to)
    '''
    called by the flask app to start the Engine.
    returns None or Engine.
    
    returns None if no memory of data or models is found (first run)
    returns Engine if memory of data or models is found or provided.
    ''' 
    
    def getExistingDataManager():
        ''' generates DataManager from data on disk '''
        return satori.DataManager(disk=disk.Disk())
    
    def getExistingModelManager():
        ''' generate a set of Model(s) for Engine '''
        
        def generateCombinedFeature(df:pd.DataFrame=None, columns:list[tuple]=None, prefix='Diff'):
            '''
            example of making a feature out of data you know ahead of time.
            most of the time you don't know what kinds of data you'll get...
            '''
            def name() -> tuple:
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
                satori.HyperParameter(
                    name='n_estimators',
                    value=300,
                    kind=int,
                    limit=100,
                    minimum=200,
                    maximum=5000),
                satori.HyperParameter(
                    name='learning_rate',
                    value=0.3,
                    kind=float,
                    limit=.05,
                    minimum=.01,
                    maximum=.1),
                satori.HyperParameter(
                    name='max_depth',
                    value=6,
                    kind=int,
                    limit=1,
                    minimum=10,
                    maximum=2),],
            'metrics':  {
                ## raw data features
                'Raw': metrics.rawDataMetric,
                ## daily percentage change, 1 day ago, 2 days ago, 3 days ago... 
                **{f'Daily{i}': partial(metrics.dailyPercentChangeMetric, yesterday=i) for i in list(range(1, 31))},
                ## rolling period transformation percentage change, max of the last 7 days, etc... 
                **{f'Rolling{tx[0:3]}{i}': partial(metrics.rollingPercentChangeMetric, window=i, transformation=tx)
                    for tx, i in product('sum() max() min() mean() median() std()'.split(), list(range(2, 21)))},
                ## rolling period transformation percentage change, max of the last 50 or 70 days, etc... 
                **{f'Rolling{tx[0:3]}{i}': partial(metrics.rollingPercentChangeMetric, window=i, transformation=tx)
                    for tx, i in product('sum() max() min() mean() median() std()'.split(), list(range(22, 90, 7)))}
            },
            'features': {
                ('streamrSpoof', 'simpleEURCleaned', 'DiffHighLow'): 
                    partial(
                        generateCombinedFeature, 
                        columns=[
                            ('streamrSpoof', 'simpleEURCleaned', 'High'), 
                            ('streamrSpoof', 'simpleEURCleaned', 'Low')])
            },
            'override': False}
        return {
            satori.ModelManager(
                disk=disk.Disk(),
                memory=memory.Memory,
                primary=SourceStreamTarget(
                        source='streamrSpoof', 
                        stream='simpleEURCleaned', 
                        publisher='none',
                        target='High'),
                ancillary=[SourceStreamTarget(
                        source='streamrSpoof', 
                        stream='simpleEURCleaned', 
                        publisher='none',
                        target='Low')],
                pinnedFeatures=[('streamrSpoof', 'simpleEURCleaned', 'DiffHighLow')],
                chosenFeatures=[
                    ('streamrSpoof', 'simpleEURCleaned', 'High'), 
                    ('streamrSpoof', 'simpleEURCleaned', 'Low'), 
                    ('streamrSpoof', 'simpleEURCleaned', 'DiffHighLow'),
                    ('streamrSpoof', 'simpleEURCleaned', 'DailyHigh21'), 
                    ('streamrSpoof', 'simpleEURCleaned', 'RollingLow50min'), 
                    ('streamrSpoof', 'simpleEURCleaned', 'RollingHigh14std'), 
                    ('streamrSpoof', 'simpleEURCleaned', 'RollingHigh50max')],
                **kwargs),
            satori.ModelManager(
                disk=disk.Disk(),
                memory=memory.Memory,
                primary=SourceStreamTarget(
                    source='streamrSpoof', 
                    stream='simpleEURCleaned', 
                    publisher='none',
                    target='Low'),
                ancillary=[
                    SourceStreamTarget(
                        source='streamrSpoof', 
                        stream='simpleEURCleaned', 
                        publisher='none',
                        target='High'),],
                pinnedFeatures=[('streamrSpoof', 'simpleEURCleaned', 'Low')],
                chosenFeatures=[
                    ('streamrSpoof', 'simpleEURCleaned', 'Low'), 
                    ('streamrSpoof', 'simpleEURCleaned', 'High'), 
                    ('streamrSpoof', 'simpleEURCleaned', 'DailyLow21'), 
                    ('streamrSpoof', 'simpleEURCleaned', 'DiffHighLow'),
                    ('streamrSpoof', 'simpleEURCleaned', 'RollingLow14std'), 
                    ('streamrSpoof', 'simpleEURCleaned', 'RollingLow50min'), 
                    ('streamrSpoof', 'simpleEURCleaned', 'RollingHigh50max')],
                **kwargs),
            satori.ModelManager(
                disk=disk.Disk(),
                memory=memory.Memory,
                primary=SourceStreamTarget(
                        source='streamrSpoof', 
                        stream='simpleEURCleaned', 
                        publisher='none',
                        target='Close'),
                ancillary=[
                    SourceStreamTarget(
                        source='streamrSpoof', 
                        stream='simpleEURCleaned', 
                        publisher='none',
                        target='High'),
                    SourceStreamTarget(
                        source='streamrSpoof', 
                        stream='simpleEURCleaned', 
                        publisher='none',
                        target='Low')],
                chosenFeatures=[
                    ('streamrSpoof', 'simpleEURCleaned', 'Close'),
                    ('streamrSpoof', 'simpleEURCleaned', 'High'),
                    ('streamrSpoof', 'simpleEURCleaned', 'Low'),
                    ('streamrSpoof', 'simpleEURCleaned', 'DiffHighLow'),
                    ('streamrSpoof', 'simpleEURCleaned', 'DailyCLose7')],
                **kwargs)
            }
    
    # todo: use existence of something else like wallet file to tell if system setup, or just ask server directly...
    #dataSettings = satori.config.dataSettings()
    #if dataSettings != {}:
    #    return None # this should trigger front end to take them through a process?
    
    return satori.Engine(
        view=satori.View(),
        data=getExistingDataManager(),
        models=getExistingModelManager()
        )