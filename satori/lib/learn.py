import threading
import time

import pandas as pd
from matplotlib import pyplot as plt
from IPython.display import clear_output
from .data import DataManager
from .model import ModelManager

class Learner:

    def __init__(
        self, 
        data:DataManager=None,
        model:ModelManager=None,
        models:'set(ModelManager)'=None,
        cooldown:int=0,
        recess:int=0,
        api:'object'=None,
        out:'function'=None,
    ):
        '''
        data - a DataManager for the data
        model - a ModelManager for the model
        models - a list of ModelManagers
        coolDown - to reduce the computational load, sleep for x seconds every iteration
        recess - to reduce bandwidth load (when looking for more data), sleep for x seconds
        '''
        self.data = data
        self.models = models
        self.api = api
        self.out = out
        if model is not None:
            self.models = {self.models + [model]}
        self.cooldown = cooldown
        self.recess = recess

    def run(self, cooldown:int=None, recess:int=None, view:bool=True, points:int=7):
        '''
        most learners have one dataset, but multiple models 
        (like predicting each feature in the dataset)
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
                print('waiting for data...  ')
                print('building models...  ')
                model.buildStable()
                predictions[model.targetKey] = model.producePrediction()
                print('Predictions:', predictions, 'Scores:', scores)
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
                        if callable(self.out):
                            self.out(model, points, predictions, scores)
                        if self.api is not None:
                            self.api.send(model, points, predictions, scores)
                        if view:
                            self.jupyterOut(model, points, predictions, scores)
                        else:
                            clear_output()
                        print(
                            'Predictions:\n', pretty(predictions),
                            '\nScores:\n', pretty(scores))
                print('fetching new data...  ')
        
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
            
    def jupyterOut(self, model, points:int, predictions:dict, scores:dict, ):
        
        def lineWidth(score:str) -> float:
            try: 
                score = (float(score.split()[0])+1)**3
            except:
                score = None
            return min(abs(score or .1), 1)

        #(model.data.iloc[-1*points:]
        #    .append(pd.DataFrame({k: [v] for k, v in predictions.items()}))
        #    .reset_index(drop=True)
        #    .plot(figsize=(8,5), linewidth=3))
        ## to show confidence with linewidth:
        ax = None
        for ix, col in enumerate(model.data.columns.tolist()):
            print(model.targetKey, predictions.get(col))
            ax = (model.data.iloc[-1*points:, [ix]]
                .append(pd.DataFrame({col: [predictions.get(col, 0)]}))
                .reset_index(drop=True)
                .plot(
                    **{'ax': ax} if ax is not None else {},
                    figsize=(8,5), 
                    linewidth=lineWidth(scores.get(col, 0))))
        clear_output()
        plt.show()


# possible improvements:
# 1. optionally show graph of data with latest predictions
# 2. save all (best per datapoint, or per some amount of data or time)
#    models and predict every datapoint after them,
#    that way what they predict can be used as additional features.
#    this seems like a major feature that would require some archetecting.
#    maybe it can learn to keep the best 3 or something.
#    well, and then there's cyclical... idk