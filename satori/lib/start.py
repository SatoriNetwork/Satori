from itertools import product
from functools import partial
import pandas as pd
import satori
import os

from satori.lib.engine.structs import SourceStreamTargets

# accept optional data necessary to generate models data and learner
def getEngine(path=None):
    '''
    called by the flask app to start the Engine.
    returns None or Engine.
    
    returns None if no memory of data or models is found (first run)
    returns Engine if memory of data or models is found or provided.
    ''' 
    
    def getExistingDataManager(dataSettings:dict = None):
        ''' generates DataManager from data on disk '''
        data = satori.DataManager()
        return data
    
    def getExistingModelManager():
        ''' generate a set of Model(s) for Engine '''
        
        def generateCombinedFeature(df:pd.DataFrame=None, columns:list[tuple]=None, prefix='Diff'):
            '''
            example of making a feature out of data you know ahead of time.
            most of the time you don't know what kinds of data you'll get...
            '''
            def name() -> tuple:
                return (columns[0][0], columns[0][1], 'DiffHighLow')

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
                'Raw': satori.ModelManager.rawDataMetric,
                ## daily percentage change, 1 day ago, 2 days ago, 3 days ago... 
                #**{f'Daily{i}': partial(satori.ModelManager.dailyPercentChangeMetric, yesterday=i) for i in list(range(1, 31))},
                ## rolling period transformation percentage change, max of the last 7 days, etc... 
                #**{f'Rolling{i}{tx[0:3]}': partial(satori.ModelManager.rollingPercentChangeMetric, window=i, transformation=tx)
                #    for tx, i in product('sum() max() min() mean() median() std()'.split(), list(range(2, 21)))},
                ## rolling period transformation percentage change, max of the last 50 or 70 days, etc... 
                #**{f'Rolling{i}{tx[0:3]}': partial(satori.ModelManager.rollingPercentChangeMetric, window=i, transformation=tx)
                #    for tx, i in product('sum() max() min() mean() median() std()'.split(), list(range(22, 90, 7)))}
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
                modelPath='modelHigh.joblib',
                sourceId='streamrSpoof',
                streamId='simpleEURCleaned',
                targetId='High',
                pinnedFeatures=[('streamrSpoof', 'simpleEURCleaned', 'DiffHighLow')],
                targets=[SourceStreamTargets(
                    source='streamrSpoof', 
                    stream='simpleEURCleaned', 
                    targets=['High', 'Low'])],
                chosenFeatures=[
                    ('streamrSpoof', 'simpleEURCleaned', 'High'), 
                    ('streamrSpoof', 'simpleEURCleaned', 'Low'), 
                    ('streamrSpoof', 'simpleEURCleaned', 'DiffHighLow'),
                ],
                **kwargs),
            #satori.ModelManager(
            #    modelPath='modelLow.joblib',
            #    streamId='simpleEURCleaned',
            #    targetId='Low',
            #    chosenFeatures=[('streamrSpoof', 'simpleEURCleaned', 'Low')],
            #    **kwargs),
            #satori.ModelManager(
            #    modelPath='modelClose.joblib',
            #    streamId='simpleEURCleaned',
            #    targetId='Close',
            #    chosenFeatures=[('streamrSpoof', 'simpleEURCleaned', 'Close')],
            #    **kwargs)
            }
    
    dataSettings = satori.config.dataSettings()
    if dataSettings != {}:
        return None
    return satori.Engine(
        view=satori.View(),
        data=getExistingDataManager(dataSettings),
        models=getExistingModelManager()
        )