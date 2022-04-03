import json
import pandas as pd 

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
                'content': {
                    'High': 0.81856, 
                    'Low': 0.81337, 
                    'Close': 0.81512}}}'''
        j = json.loads(data)
        self.streamId = list(j.keys())[0]
        self.observationId = j[self.streamId]['observation-id']
        self.content = j[self.streamId]['content']
        if isinstance(self.content, dict):
            self.df = pd.DataFrame(
                self.content, 
                index=[self.observationId])
            self.df.index.name = self.streamId  # perhaps the index name should be the type of index it is (datetime, str, other?)
            #self.df.name = self.streamId  # perhaps we should monkeypatch the name of the stream here instead.
        elif not isinstance(self.content, dict):
            self.df = pd.DataFrame(
                {self.streamId: [self.content]}, 
                index=[self.observationId])
            self.df.index.name = self.streamId  # perhaps the index name should be the type of index it is (datetime, str, other?)
            #self.df.name = self.streamId  # perhaps we should monkeypatch the name of the stream here instead.
