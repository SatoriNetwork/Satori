# this is to make sure our design for interprocess communication will work
# we want to have multiple threads modifying and reading the same objects...

import threading
import time
import datetime as dt

class DataManager:
    
    def __init__(self):
        self.updates = {}
        
    def runSubscriber(self):
        print('runSubscriber')

    def runPublisher(self):
        print('runPublisher')

    def runScholar(self):
        print('runScholar')

                
class ModelManager:
    
    def __init__(self, name, inputs):
        self.targetKey = name
        self.inputs = [1,2,3]

    def runPredictor(self):
        print(f'{self.targetKey} runPredictor')

    def runExplorer(self):
        print(f'{self.targetKey} runExplorer')
        # testing that threads die
        #with open('temp.log', mode='a') as f:
        #    f.write(str(dt.datetime.utcnow()))
            

    
class Learner:

    def __init__(
        self,
        data:DataManager=None,
        model:ModelManager=None,
        models:'set(ModelManager)'=None,
    ):
        '''
        data - a DataManager for the data
        model - a ModelManager for the model
        models - a list of ModelManagers
        '''
        self.data = data
        self.models = models
        if model is not None:
            self.models = {self.models + [model]}

    def run(self):
        '''
        Main Loops - one for each model and one for the data manager.
        '''

        def subscriber():
            ''' loop for data '''

            def rest():
                x = 30
                if x == -1:
                    while True:
                        time.sleep(60*60)
                time.sleep(x)

            while True:
                rest()
                self.data.runSubscriber(inputs)

        def publisher():
            ''' loop for data '''

            def rest():
                x = 30
                if x == -1:
                    while True:
                        time.sleep(60*60)
                time.sleep(x)

            while True:
                rest()
                self.data.runPublisher(predictions)

        def scholar():
            ''' loop for data '''

            def rest():
                x = 30
                if x == -1:
                    while True:
                        time.sleep(60*60)
                time.sleep(x)

            while True:
                rest()
                self.data.runScholar(inputs)

        def predictor(model:ModelManager):
            ''' loop for producing predictions '''

            def rest():
                x = 5
                if x == -1:
                    while True:
                        time.sleep(60*60)
                time.sleep(x)

            while True:
                rest()
                model.runPredictor()

        def explorer(model:ModelManager):
            ''' loop for producing models '''
        
            def rest():
                x = 5
                if x == -1:
                    while True:
                        time.sleep(60*60)
                time.sleep(x)

            while True:
                rest()
                model.runExplorer()

        threads = {}
        threads['subscriber'] = threading.Thread(target=subscriber, daemon=True)
        threads['publisher'] = threading.Thread(target=publisher, daemon=True)
        threads['scholar'] = threading.Thread(target=scholar, daemon=True)
        predictions = {}
        scores = {}
        inputs = {}
        for model in self.models:
            threads[f'{model.targetKey}.predictor'] = threading.Thread(target=predictor, args=[model], daemon=True)
            threads[f'{model.targetKey}.explorer'] = threading.Thread(target=explorer, args=[model], daemon=True)
            predictions[model.targetKey] = ''
            scores[model.targetKey] = ''
            inputs[model.targetKey] = []

        for thread in threads.values():
            print('starting')
            thread.start()

        while threading.active_count() > 0:
            time.sleep(0)

# python .\tests\scratch\interprocess.py
learner = Learner(
    data=DataManager(),
    models={
        ModelManager(name='A', inputs=[1,2,3]),
        ModelManager(name='B', inputs=[2,3,4]),
        ModelManager(name='C', inputs=[3,5,6])})

learner.run()