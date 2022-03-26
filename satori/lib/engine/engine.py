import threading
import time
from .data import DataManager
from .model import ModelManager
from .view import View

class Engine:

    def __init__(
        self,
        data:DataManager=None,
        model:ModelManager=None,
        models:'set(ModelManager)'=None,
        api:'object'=None,
        view:View=None,
    ):
        '''
        data - a DataManager for the data
        model - a ModelManager for the model
        models - a list of ModelManagers
        '''
        self.data = data
        self.models = models
        self.view = view
        self.api = api
        if model is not None:
            self.models = {self.models + [model]}

    
    def out(self, data=True):
        ''' old functionality that must be accounted for in new design
        if self.view is not None:
            self.view.print(**(
                {
                    'Predictions:\n':predictions,
                    '\nScores:\n':scores
                } if data else {model.targetKey: 'loading... '}))
        '''

    def updateView(self, data=True):
        ''' old functionality that must be accounted for in new design
        predictions[model.targetKey] = model.producePrediction()
        scores[model.targetKey] = f'{round(stable, 3)} ({round(test, 3)})'
        inputs[model.targetKey] = model.showFeatureData()
        if first or startingPredictions != predictions:
            first = False
            if self.api is not None:
                self.api.send(model, predictions, scores)
            if self.view is not None:
                self.view.view(model, predictions, scores)
                out()
        out(data=False)
        '''
    
    def run(self):
        ''' Main '''

        def subscriber():
            '''
            listens for external updates on subscriptions - 
            turn this into a steam rather than a loop - 
            triggered from flask app.
            this should probably be broken out into a service
            that subscribes and a service that listens...
            should be on demand
            '''
            while True:
                time.sleep(.1)
                self.data.runSubscriber(self.models)
                
        def publisher():
            '''
            publishes predictions on demand
            this should probably be broken out into a service
            that creates a stream and a service that publishes...
            '''
            self.data.runPublisher(self.models)

        def scholar():
            ''' always looks for external data and compiles it '''
            while True:
                self.data.runScholar(self.models)

        def predictor(model:ModelManager):
            ''' produces predictions on demand '''
            model.runPredictor(self.data)
        
        def sync(model:ModelManager):
            ''' sync available inputs found and compiled by scholar on demand '''
            model.syncAvailableInputs(self.data)

        def explorer(model:ModelManager):
            ''' always looks for a better model '''
            while True:
                model.runExplorer()

        def watcher(model:ModelManager):
            if self.view:
                self.view.listen(model)
   
        publisher()
        threads = {}
        threads['subscriber'] = threading.Thread(target=subscriber, daemon=True)
        threads['scholar'] = threading.Thread(target=scholar, daemon=True)
        for model in self.models:
            model.buildStable() # we have to run this once for each model to complete its initialization
            predictor(model)
            sync(model)
            watcher(model)
            threads[f'{model.targetKey}.explorer'] = threading.Thread(target=explorer, args=[model], daemon=True)

        for thread in threads.values():
            thread.start()
        
        while threading.active_count() > 0:
            time.sleep(0)

howToRun = '''
# python .\tests\scratch\interprocess.py
learner = Engine(
    data=DataManager(),
    models={
        ModelManager(name='A', inputs=[1,2,3]),
        ModelManager(name='B', inputs=[2,3,4]),
        ModelManager(name='C', inputs=[3,5,6])
        }
    )

learner.run()
'''