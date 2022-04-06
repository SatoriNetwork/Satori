'''
the DataManager should save the streams to a database on disk as a parquet file
so that the model managers can get their data easily.

the DataManager object could even run as a separate server.
it should be as light weight as possible, handling data streams and their
updates constantly. any downtime it has should be spent aggregating new
datasets that might be of use to the Modelers. It does not evaluate them using
the predictive power score, but could access the global map of publishers and
their subscribers on chain, thereby acting as a low-computation recommender
system for the Modelers since it doesn't actually compute any scores. The
DataManager needs lots of disk space, both ram and short term memory. It also
needs high bandwidth capacity. If it serves only one modeler it need not be
separate from the modeler, but if it serves many, it should be on its own
hardware.

Basic Reponsibilities of the DataManager:
1. listen for new datapoints on all datastreams used by ModelManagers
    A. download and save new datapoints
    B. notify relevant ModelManagers new data is available (see 2.)
2. produce a query whereby to pull data for each model from disk.
    A. list the datasets to pull
    B. for each dataset list the columns
    C. filter by recent data (model managers can add this part if they want)
3. search for useful data streams
    A. generate a map of all pub sub relationships from the chain
    B. find similar subscribers: compare the model manager's inputs to other
       subscribers inputs
    C. find a likely group of useful publishers: of all the similar subscribers
       (by input) what group of publishers (by input or metadata) do they
       subscribe to that this model manager does not?
    D. find a unique datastream in the group: one that few or zero similar
       subscriber subscribe to
    E. download the datastream and notify model manager
4. garbage collect stale datastreams
'''
import pandas as pd
import datetime as dt
from reactivex.subject import BehaviorSubject

from satori.lib.engine.structs import Observation
from satori.lib.apis import disk

class DataManager:

    def __init__(
        self,
        dataPath:str='data.parquet',
        getData:'function'=None,
        validateData:'function'=None,
        appendData:'function'=None,
    ):
        self.dataPath = dataPath
        self.dataOriginal = pd.DataFrame()
        self.sources = {} # dictionary of streams by source and their latest incremental
        self.everything = {}  # a set of all the column names (stream ids) I've seen before.
        self.resetIncremental()
        self.getData = getData or DataManager.defaultGetData
        self.validateData = validateData or DataManager.defaultValidateData
        self.appendData = appendData or DataManager.defaultAppendData
        self.listeners = []
        self.newData = BehaviorSubject(Observation)
        self.run()

    @staticmethod
    def defaultGetData() -> pd.DataFrame:
        return pd.DataFrame({'a': [1]})  # rest call or something

    @staticmethod
    def defaultValidateData(
        data:pd.DataFrame,
        existing:pd.DataFrame,
        resetIndex=True,
    ) -> bool:
        ''' you may not want to reset index if it's a date you'd like to compare against '''
        def lastRow():
            if resetIndex:
                return existing.iloc[-1:,:].reset_index(drop=True)
            return existing.iloc[-1:,:]

        if (
            data.empty
            or not (0 < data.iloc[0,0] < 2) or not (0 < data.iloc[0,0] < 2) or not (0 < data.iloc[0,0] < 2)
            or lastRow().equals(data)  # perhaps you're calling before the data has changed...
        ):
            return False
        return True

    @staticmethod
    def defaultAppend(
        data:pd.DataFrame,
        existing:pd.DataFrame,
        resetIndex=True,
    ) -> pd.DataFrame:
        ''' you may not want to reset index if it's a date you'd like to compare against '''
        x = existing.append(data)
        if resetIndex:
            return x.reset_index(drop=True)
        return x

    def importance(self, inputs:dict = None):
        inputs = inputs or {}
        totaled = {}
        for importances in inputs.values():
            for k, v in importances.items():
                totaled[k] = v + totaled.get(k, 0)
        self.imports = sorted(totaled.items(), key=lambda item: item[1])

    def showImportance(self):
        return [i[0] for i in self.imports]

    def get(self):
        ''' gets the latest update for the data 
        * this function is no longer used. it was used for
          pulling data, now we're on a reactive system where
          we get the data pushed to us as soon as its avilable
        '''
        self.getOriginal()
        self.getExploratory()
        self.getPurge()

    def getOriginal(self):
        ''' gets the latest update for the data '''
        self.incremental = self.getData()

    def getExploratory(self):
        '''
        asks an endpoint for the history of an unseen datastream.
        provides showImportance and everythingSeenBefore perhaps...
        scores each history against each of my original data columns
        Highest are kept, else forgotten (not included in everything)
        a 'timer' is started for each that is kept so we know when to
        purge them if not picked up by our models, so the models need
        a mechanism to recognize new stuff and test it out as soon as
        they see it.
        '''
        pass

    def getPurge(self):
        ''' in charge of removing columns that aren't useful to our models '''
        pass

    def validate(self) -> bool:
        ''' appends the latest change to data '''
        if self.validateData(self.incremental, self.data):
            return True
        self.resetIncremental()
        return False

    def save(self):
        ''' gets the latest update for the data '''
        self.data.to_parquet(self.dataPath)

    def run(self, inputs:dict = None):# -> bool:
        ''' runs all three steps '''
        #if inputs:
        #    self.importance(inputs)
        self.get()
        self.append()
        self.save()
        return True
        
    def runOnce(self, inputs:dict = None):# -> bool:
        ''' run denotes a loop, there's no loop but now its explicit '''
        return self.run(inputs)
    
    #################################################################################
    ### most of the fuctions above this point are made obsolete by the new design ###
    #################################################################################
    
    def runSubscriber(self, models: list):
        ''' triggered from the flask app '''
        
        def handleNewData(models, observation: Observation):
            ''' append to existing datastream, save to disk, notify models '''
            
            def remember():
                ''' cache latest observation for each stream as DataFrame with observed-time '''
                if observation.sourceId not in self.sources.keys():
                    self.sources[observation.sourceId] = {observation.streamId: None}
                self.sources[observation.sourceId][observation.streamId] = observation.df
        
            def saveIncremental():
                ''' save these observations to the right parquet file on disk '''
                disk.Api(source=observation.sourceId, stream=observation.streamId).write(observation.df)
            
            def tellModels():
                ''' tell the modesl that listen to this stream and these targets '''
                for model in models:
                    if model.targetId in observation.df.columns:
                        model.targetUpdated.on_next(observation.df)
                    # not right, close. features really needs to be a streamId + targetId...
                    #elif any([key in observation.df.columns for key in model.feature.keys()]): 
                    #    model.inputsUpdated.on_next(True)
                    # reference model.targets:
                    if (
                        model.targets.sourceId == observation.sourceId and
                        model.targets.streamId == observation.streamId 
                    ):
                        sendUpdates = []
                        for modelTarget in model.targets.targets:
                            for obsTarget in observation.targets:
                                if modelTarget == obsTarget:
                                    sendUpdates.append(obsTarget)
                        model.inputsUpdated.on_next(
                            observation.df.loc[:, [
                                (observation.sourceId, observation.streamId, update) 
                                for update in sendUpdates]])
                                    
                        
                    
                    
            remember()
            saveIncremental()
            tellModels()
            
        self.listeners.append(self.newData.subscribe(lambda x: handleNewData(models, x) if x is not None else None))
                

    def runPublisher(self, models):
        def publish(model):
            ''' probably a rest call to the NodeJS server so it can pass it to the streamr light client '''
            with open(f'{model.id}.txt', 'w') as f:
                f.write(f'{model.prediction}, {str(dt.datetime.now())} {model.prediction}')
        
        def publishEdge(model):
            ''' probably a rest call to the NodeJS server so it can pass it to the streamr light client '''
            with open(f'{model.id}.txt', 'w') as f:
                f.write(f'{model.predictionEdge}, {str(dt.datetime.now())} {model.predictionEdge}')
                
        for model in models:
            self.listeners.append(model.predictionUpdate.subscribe(lambda x: publish(x) if x else None))
            self.listeners.append(model.predictionEdgeUpdate.subscribe(lambda x: publishEdge(x) if x else None))
    
    def runScholar(self, models):
        ''' download histories and tell model sync '''
        ## look for new useful datastreams - something like this
        #self.download(self.bestOf(self.compileMap(models)))
        #self.availableInputs.append(newInput)
        #for model in models:
        #    model.newAvailableInput.on_next(newInput)
