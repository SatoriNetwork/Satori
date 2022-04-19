from itertools import product
from functools import partial
import pandas as pd
import satori
import os

from satori.lib.engine.structs import SourceStreamTargets

# accept optional data necessary to generate models data and learner
def getEngine():
    '''
    called by the flask app to start the Engine.
    returns None or Engine.
    
    returns None if no memory of data or models is found (first run)
    returns Engine if memory of data or models is found or provided.
    ''' 
    
    def getExistingDataManager():
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
                'Raw': satori.ModelManager.rawDataMetric,
                ## daily percentage change, 1 day ago, 2 days ago, 3 days ago... 
                **{f'Daily{i}': partial(satori.ModelManager.dailyPercentChangeMetric, yesterday=i) for i in list(range(1, 31))},
                ## rolling period transformation percentage change, max of the last 7 days, etc... 
                **{f'Rolling{tx[0:3]}{i}': partial(satori.ModelManager.rollingPercentChangeMetric, window=i, transformation=tx)
                    for tx, i in product('sum() max() min() mean() median() std()'.split(), list(range(2, 21)))},
                ## rolling period transformation percentage change, max of the last 50 or 70 days, etc... 
                **{f'Rolling{tx[0:3]}{i}': partial(satori.ModelManager.rollingPercentChangeMetric, window=i, transformation=tx)
                    for tx, i in product('sum() max() min() mean() median() std()'.split(), list(range(22, 90, 7)))}
            },
            'features': {
                ('streamrSpoof', 'simpleEURCleanedHL', 'DiffHighLow'): 
                    partial(
                        generateCombinedFeature, 
                        columns=[
                            ('streamrSpoof', 'simpleEURCleanedHL', 'High'), 
                            ('streamrSpoof', 'simpleEURCleanedHL', 'Low')])
            },
            'override': False}
        return {
            satori.ModelManager(
                modelPath='modelHigh.joblib',
                sourceId='streamrSpoof',
                streamId='simpleEURCleanedHL',
                targetId='High',
                targets=[SourceStreamTargets(
                    source='streamrSpoof', 
                    stream='simpleEURCleanedHL', 
                    targets=['High', 'Low'])],
                pinnedFeatures=[('streamrSpoof', 'simpleEURCleanedHL', 'DiffHighLow')],
                chosenFeatures=[
                    ('streamrSpoof', 'simpleEURCleanedHL', 'DailyHigh21'), 
                    ('streamrSpoof', 'simpleEURCleanedHL', 'RollingHigh14std'), 
                    ('streamrSpoof', 'simpleEURCleanedHL', 'RollingHigh50max'), 
                    ('streamrSpoof', 'simpleEURCleanedHL', 'RollingLow50min'), 
                    ('streamrSpoof', 'simpleEURCleanedHL', 'High'), 
                    ('streamrSpoof', 'simpleEURCleanedHL', 'Low'), 
                    ('streamrSpoof', 'simpleEURCleanedHL', 'DiffHighLow'),
                ],
                **kwargs),
            satori.ModelManager(
                modelPath='modelLow.joblib',
                sourceId='streamrSpoof',
                streamId='simpleEURCleanedHL',
                targetId='Low',
                targets=[SourceStreamTargets(
                    source='streamrSpoof', 
                    stream='simpleEURCleanedHL', 
                    targets=['High', 'Low'])],
                pinnedFeatures=[('streamrSpoof', 'simpleEURCleanedHL', 'Low')],
                chosenFeatures=[
                    ('streamrSpoof', 'simpleEURCleanedHL', 'DailyLow21'), 
                    ('streamrSpoof', 'simpleEURCleanedHL', 'RollingLow14std'), 
                    ('streamrSpoof', 'simpleEURCleanedHL', 'RollingLow50min'), 
                    ('streamrSpoof', 'simpleEURCleanedHL', 'RollingHigh50max'), 
                    ('streamrSpoof', 'simpleEURCleanedHL', 'High'), 
                    ('streamrSpoof', 'simpleEURCleanedHL', 'Low'), 
                    ('streamrSpoof', 'simpleEURCleanedHL', 'DiffHighLow'),
                ],
                **kwargs),
            satori.ModelManager(
                modelPath='modelClose.joblib',
                sourceId='streamrSpoof',
                streamId='simpleEURCleanedC',
                targetId='Close',
                targets=[
                    SourceStreamTargets(
                        source='streamrSpoof', 
                        stream='simpleEURCleanedHL', 
                        targets=['High', 'Low']),
                    SourceStreamTargets(
                        source='streamrSpoof', 
                        stream='simpleEURCleanedC', 
                        targets=['Close'])],
                chosenFeatures=[
                    ('streamrSpoof', 'simpleEURCleanedC', 'Close'),
                    ('streamrSpoof', 'simpleEURCleanedHL', 'High'),
                    ('streamrSpoof', 'simpleEURCleanedHL', 'Low'),
                    ('streamrSpoof', 'simpleEURCleanedHL', 'DiffHighLow'),
                    ('streamrSpoof', 'simpleEURCleanedHL', 'DailyCLose7'),
                ],
                **kwargs)
            }
    
    # todo: use settings...
    dataSettings = satori.config.dataSettings()
    if dataSettings != {}:
        return None
    return satori.Engine(
        view=satori.View(),
        data=getExistingDataManager(),
        models=getExistingModelManager()
        )