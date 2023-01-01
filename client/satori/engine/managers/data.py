# TODO: refactor see issue #24

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
import datetime as dt
from reactivex.subject import BehaviorSubject
from satori import config
from satori.apis.interfaces.data import DataDiskApi
from satori.engine.managers.model import ModelManager
from satori.concepts.structs import Observation, StreamIdMap
from satori.init.start import StartupDag


class DataManager:

    def __init__(self, disk: DataDiskApi = None, startupDag: StartupDag = None):
        # {source, streams, author, target: latest incremental}
        self.targets = StreamIdMap()
        # {source, stream, author, target: latest predictions}
        self.predictions = StreamIdMap()
        self.listeners = []
        self.newData = BehaviorSubject(None)
        self.disk = disk
        self.startup = startupDag

    def importance(self, inputs: dict = None):
        inputs = inputs or {}
        totaled = {}
        for importances in inputs.values():
            for k, v in importances.items():
                totaled[k] = v + totaled.get(k, 0)
        self.imports = sorted(totaled.items(), key=lambda item: item[1])

    def showImportance(self):
        return [i[0] for i in self.imports]

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

    #################################################################################
    ### most of the fuctions above this point are made obsolete by the new design ###
    #################################################################################

    def runSubscriber(self, models: list[ModelManager]):
        ''' routes new data to the right models '''

        def handleNewData(models: list[ModelManager], observation: Observation):
            ''' append to existing datastream, save to disk, notify models '''

            def remember():
                '''
                cache latest observation for each stream as an Observation object with a DataFrame 
                if it's new returns true so process can continue, if a repeat, return false
                '''
                if observation.key() not in self.targets.keys():
                    self.targets.add(observation.key(), None)
                x = self.targets.get(observation.key())
                if (
                    x is not None and x.observationId is not None and
                    observation.observationId is not None and
                    x.observationId == observation.observationId
                ):
                    return False
                self.targets.add(observation.key(), observation)
                return True

            def saveIncremental():
                ''' save these observations to the right parquet file on disk '''
                self.disk.setAttributes(
                    source=observation.source,
                    author=observation.author,
                    stream=observation.stream).append(observation.df.copy())

            def compress():
                ''' 
                compress if the number of incrementals is high
                could make this responsive to /get/stream/cadence if we wanted.
                '''
                self.disk.setAttributes(
                    source=observation.source,
                    author=observation.author,
                    stream=observation.stream)
                if len(self.disk.incrementals()) > 100:
                    try:
                        self.disk.compress()
                    except Exception:
                        pass

            def tellModels():
                ''' tell the modesl that listen to this stream and these targets '''
                for model in models:
                    if (
                        model.variable.source == observation.source and
                        model.variable.author == observation.author and
                        model.variable.stream == observation.stream and
                        (
                            model.variable.target == observation.target or
                            model.variable.target in observation.content.keys())
                    ):
                        model.targetUpdated.on_next(observation.df)
                    # TODO:
                    # what about features? is that what this is for? (stable model)
                    # also, what about exploratory features? (pilot model)
                    # elif any([key in observation.df.columns for key in model.feature.keys()]):
                    # model.inputsUpdated.on_next(True)
                    # reference model.targets:
                    # if (
                    #    model.targets.sourceId == observation.source and
                    #    model.targets.streamId == observation.stream
                    # ):
                    #    sendUpdates = []
                    #    for modelTarget in model.targets.targets:
                    #        for obsTarget in observation.targets:
                    #            if modelTarget == obsTarget:
                    #                sendUpdates.append(obsTarget)
                    #    model.inputsUpdated.on_next(
                    #        observation.df.loc[:, [
                    #            (observation.source, observation.stream, update)
                    #            for update in sendUpdates]])

            if remember():
                saveIncremental()
                tellModels()
                compress()

        self.listeners.append(self.newData.subscribe(
            lambda x: handleNewData(models, x) if x is not None else None))
        # self.listeners.append(self.newData.subscribe(lambda x: print('triggered')))

    def runPublisher(self, models):
        def publish(model: ModelManager):
            ''' publish to the right source '''

            def remember():
                ''' in memory cache of predictions for each model '''
                self.predictions.add(model.key, model.prediction)
                return True

            def post():
                '''
                here we save prediction to disk, but that'll change once we
                can post it somewhere.

                TODO: for this model look up the source of the prediction stream
                which could be streamr, or satori pubsub, or even something
                else. then post this prediction to that source. If it is streamr
                send it over to the nodeJS server. if it is satori pubsub, send
                use the pubsub connection object in the StartupDag object 
                (meaning, we might have to pass that connection object down to
                this function in the first place.)
                '''
                def saveToDisk():
                    if self.predictions.isFilled(key=model.key):
                        # why is there a for loop here?
                        # we should only have 1 target, and one prediction...
                        # is this really old, from when we thought a model might
                        # have multiple targets, to predict a whole stream?
                        for k, v in self.predictions.getAll(key=model.key):
                            path = config.root(
                                '..', 'predictions', k[0], k[1], k[2] + '.txt')
                            self.disk.savePrediction(
                                path=path, prediction=f'{str(dt.datetime.now())} | {k} | {v}\n')
                        self.predictions.remove(key=model.key)

                def publishToSatori():
                    if self.predictions.isFilled(key=model.key):
                        self.startup.connection.publish(
                            topic=model.key,
                            data=self.predictions.get(key=model.key))

                if model.variable.source == 'streamr':
                    saveToDisk()
                if model.variable.source == 'SATORI':
                    publishToSatori()

            remember()
            post()

        for model in models:
            self.listeners.append(model.predictionUpdate.subscribe(
                lambda x: publish(x) if x else None))
        #    self.listeners.append(model.predictionEdgeUpdate.subscribe(lambda x: publishEdge(x) if x else None))

    def runScholar(self, models):
        '''
        download histories (do not subscribe, these histories are experimental)
        and tell exploratory model managers to use them as inputs in order to 
        evaluat their usefulness. if they are useful, then we will officially 
        use them which means pushing the exploratory model to stable, purging
        the history, subscribing to them, downloading their updated history.

        this function is interconnected with a recommender system larger process
        which uses information about who subscribes to what and predicts what,
        (meaning a map of the network is internally built, or at least similar
        nodes by their inputs and outputs are identified) in order to evaulate
        new datastreams that it might find useful.

        there's a lot to do here but for mvp we'll just randomly sample 
        datastreams from whatever sources are available to us.
        '''

        # look for new useful datastreams - something like this
        # self.download(self.bestOf(self.compileMap(models)))
        # self.availableInputs.append(newInput)
        # for model in models:
        #    model.newAvailableInput.on_next(newInput)
