import threading
import time
from .data import DataManager
from .model import ModelManager
from .view import View

class Learner:

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
            '''
            while True:
                time.sleep(.1)
                self.data.runSubscriber(self.models)
                
        def publisher():
            ''' publishes predictions
            this should probably be broken out into a service
            that creates a stream and a service that publishes...
            '''
            self.data.runPublisher(self.models)

        def scholar():
            ''' looks for external data and compiles it '''
            while True:
                self.data.runScholar(self.models)

        def predictor(model:ModelManager):
            ''' produces predictions '''
            model.buildStable()
            model.runPredictor(self.data)

        
        def explorer(model:ModelManager):
            ''' loop for producing models -
            I think more ideally we'd have a loop that searches hyper params 
            in one model object, we'd also have this explorer which is triggered
            by new data becoming available in a different object... idk a 
            hierarchy of model creation? weird... we'll just use a loop
            and look for new data each iteration. '''
            while True:
                model.runExplorer(self.data)
                #stable, test = model.evaluateCandidate(returnBoth=True)
                #model.buildTest()

        publisher()
        threads = {}
        threads['subscriber'] = threading.Thread(target=subscriber, daemon=True)
        threads['scholar'] = threading.Thread(target=scholar, daemon=True)
        for model in self.models:
            predictor(model)
            #threads[f'{model.targetKey}.explorer'] = threading.Thread(target=explorer, args=[model], daemon=True)

        for thread in threads.values():
            thread.start()

        while threading.active_count() > 0:
            time.sleep(0)

howToRun = '''
# python .\tests\scratch\interprocess.py
learner = Learner(
    data=DataManager(),
    models={
        ModelManager(name='A', inputs=[1,2,3]),
        ModelManager(name='B', inputs=[2,3,4]),
        ModelManager(name='C', inputs=[3,5,6])
        }
    )

learner.run()
'''