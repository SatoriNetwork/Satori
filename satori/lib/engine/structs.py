import json
import pandas as pd 
import datetime as dt

class HyperParameter:
    
    def __init__(
        self,
        name:str='n_estimators',
        value=3,
        limit=1,
        minimum=1,
        maximum=10,
        kind:'type'=int
    ):
        self.name = name
        self.value = value
        self.test = value
        self.limit = limit
        self.min = minimum
        self.max = maximum
        self.kind = kind

class Observation:
    
    def __init__(self, data):
        self.data = data
        self.parse(data)

    def parse(self, data):
        ''' {
            'simpleEURCleaned': {
                'observation-id': 3675, 
                'observed-time': 2022-02-16 02:52:45.794120, 
                'content': {
                    'High': 0.81856, 
                    'Low': 0.81337, 
                    'Close': 0.81512}}}
            note: if observed-time is missing, define it here.
        '''
        j = json.loads(data)
        self.streamId = list(j.keys())[0]
        self.observedTime = j[self.streamId].get('observed-time', str(dt.datetime.utcnow()))
        self.observationId = j[self.streamId]['observation-id']
        self.content = j[self.streamId]['content']
        if isinstance(self.content, dict):
            self.df = pd.DataFrame(
                {(self.streamId, target): values for target, values in self.content.items}, 
                index=[self.observedTime])
        elif not isinstance(self.content, dict):
            self.df = pd.DataFrame(
                {(self.streamId, self.streamId): [self.content]}, 
                index=[self.observedTime])
