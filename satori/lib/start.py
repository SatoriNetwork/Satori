from itertools import product
from functools import partial
import pandas as pd
import satori
import os

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

        def getNewData():
            ''' incrementally returns mock future data to simulate the passage of time '''
            for i in future.index:
                yield pd.DataFrame(future.loc[i]).T
                
        try:
            df = pd.read_csv(satori.config.dataPath(dataSettings.get('subscription database')))
        except Exception as e:
            print(e)
            # example of data:
            df = pd.DataFrame({
                'High': [
                    0.837240,
                    0.837100,
                    0.828020,
                    0.830290,
                    0.828780,], 
                'Low': [
                    0.830560,
                    0.825830,
                    0.824400,
                    0.823450,
                    0.820280,],
                'Close': [
                    0.835770,
                    0.827200,
                    0.824880,
                    0.827750,
                    0.820550,],})
        past = df.iloc[:round(df.shape[0]*.8)]
        future = df.iloc[round(df.shape[0]*.8):]
        data = satori.DataManager(
            data=past,
            getData=partial(next, getNewData()),
            validateData=satori.DataManager.defaultValidateData,
            appendData=satori.DataManager.defaultAppend)
        return data
    
    def getExistingModelManager():
        ''' generate a set of Model(s) for Engine '''
        
        def generateCombinedFeature(df:pd.DataFrame=None, columns:'list(str)'=None, prefix='Diff'):
            '''
            example of making a feature out of data you know ahead of time.
            most of the time you don't know what kinds of data you'll get...
            '''
            def name() -> str:
                return f'{prefix}{columns[0]}{columns[1]}'

            if df is None:
                return name()

            columns = columns or []
            feature = df.loc[:, columns[0]] - df.loc[:, columns[1]]
            feature.name = name()
            return feature
    
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
                # raw data features
                'raw': satori.ModelManager.rawDataMetric,
                # daily percentage change, 1 day ago, 2 days ago, 3 days ago... 
                **{f'Daily{i}': partial(satori.ModelManager.dailyPercentChangeMetric, yesterday=i) for i in list(range(1, 31))},
                # rolling period transformation percentage change, max of the last 7 days, etc... 
                **{f'Rolling{i}{tx[0:3]}': partial(satori.ModelManager.rollingPercentChangeMetric, window=i, transformation=tx)
                    for tx, i in product('sum() max() min() mean() median() std()'.split(), list(range(2, 21)))},
                # rolling period transformation percentage change, max of the last 50 or 70 days, etc... 
                **{f'Rolling{i}{tx[0:3]}': partial(satori.ModelManager.rollingPercentChangeMetric, window=i, transformation=tx)
                    for tx, i in product('sum() max() min() mean() median() std()'.split(), list(range(22, 90, 7)))}},
            'features': {'DiffHighLow': partial(generateCombinedFeature, columns=['High', 'Low'])},
            'chosenFeatures': ['RawClose', 'RawHigh', 'RawLow', 'DiffHighLow'],
            'override': False}
        return {
            satori.ModelManager(
                modelPath='modelHigh.joblib',
                targetKey='High',
                pinnedFeatures=['DiffHighLow'],
                **kwargs),
            satori.ModelManager(
                modelPath='modelLow.joblib',
                targetKey='Low',
                **kwargs),
            satori.ModelManager(
                modelPath='modelClose.joblib',
                targetKey='Close',
                **kwargs)}
    
    dataSettings = satori.config.dataSettings()
    if dataSettings != {}:
        return None
    return satori.Engine(
        view=satori.View(),
        data=getExistingDataManager(dataSettings),
        models=getExistingModelManager())