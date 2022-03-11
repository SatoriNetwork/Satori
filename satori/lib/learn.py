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
        cooldown:int=0,
        recess:int=0,
        api:'object'=None,
        view:View=None,
    ):
        '''
        data - a DataManager for the data
        model - a ModelManager for the model
        models - a list of ModelManagers
        coolDown - to reduce the computational load
        recess - to reduce bandwidth load (when seeking data)
        '''
        self.data = data
        self.models = models
        self.view = view
        self.api = api
        if model is not None:
            self.models = {self.models + [model]}
        self.cooldown = cooldown
        self.recess = recess

    def run(self, cooldown:int=None, recess:int=None):
        '''
        Main Loops - one for each model and one for the data manager.
        cooldown: sleep for x seconds between Model exploration iterations
        recess: number of seconds to sleep before looking for data again
                (-1 = disable, do not fetch data (sleep indefinitely))
        view: print out results to Jupyter notebook


        '''

        def dataWaiter():

            def rest():
                x = recess or self.recess
                if x == -1:
                    while True:
                        time.sleep(60*60)
                time.sleep(x)


            while True:
                rest()
                self.data.runOnce(inputs)


        def learner(model:ModelManager):

            def pretty(x:dict):
                return '\n '.join([f' {k}: {v}' for k, v in x.items()])

            def rest():
                time.sleep(cooldown or self.cooldown)

            first = True
            while True:
                if self.view is not None:
                    self.view.print('waiting for data...  ', 'building models...  ')
                model.buildStable()
                predictions[model.targetKey] = model.producePrediction()
                if self.view is not None:
                    self.view.print('Predictions:', predictions, 'Scores:', scores)
                while model.data.shape == self.data.data.shape and model.data.shape[0] > 0:
                    rest()
                    startingPredictions = predictions.copy()
                    model.buildTest()
                    stable, test = model.evaluateCandidate(returnBoth=True)
                    predictions[model.targetKey] = model.producePrediction()
                    scores[model.targetKey] = f'{round(stable, 3)} ({round(test, 3)})'
                    inputs[model.targetKey] = model.showFeatureData()
                    if first or startingPredictions != predictions:
                        first = False
                        if self.api is not None:
                            self.api.send(model, predictions, scores)
                        if self.view is not None:
                            print('view is not None')
                            self.view.view(model, predictions, scores)
                            self.view.print(
                            'Predictions:\n', pretty(predictions),
                            '\nScores:\n', pretty(scores))
                if self.view is not None:
                    self.view.print('fetching new data...  ')

        thread = threading.Thread(target=dataWaiter)
        thread.start()
        threads = {'dataWaiter': thread}
        predictions = {}
        scores = {}
        inputs = {}
        for model in self.models:
            thread = threading.Thread(target=learner, args=[model])
            thread.start()
            threads[model.targetKey] = thread
            predictions[model.targetKey] = ''
            scores[model.targetKey] = ''
            inputs[model.targetKey] = []
