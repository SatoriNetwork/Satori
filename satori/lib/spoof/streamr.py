# > python satori\spoof\streamr.py   

import time 
import json
import requests
import datetime as dt
import pandas as pd
from satori import config 
from satori.lib.apis import disk

class Streamr():
    def __init__(self):
        self.sourceId = 'streamrSpoof'
        self.streamId = 'simpleEURCleaned'
        df = pd.read_csv(config.root('lib', 'spoof', 'simpleEURCleaned.csv'))
        existing = disk.Api(source=self.sourceId, stream=self.streamId).read()
        past = existing.shape[0] if existing is not None else 0
        self.past = df.iloc[:past]
        self.future = df.iloc[past:]
        self.port = config.get()['port']
        self.incremental = self.getNewData()

    def getNewData(self): # -> pd.DataFrame:
        ''' incrementally returns mock future data to simulate the passage of time '''
        for i in self.future.index:
            yield pd.DataFrame(self.future.loc[i]).T

    def providePast(self):
        ''' provides the past as json '''
        return self.past.T.to_json()

    def provideIncremental(self):
        ''' observation with row id '''
        return next(self.incremental).T.to_json()
        
    def provideObservation(self): # -> int, string:
        d = next(self.incremental).T.to_dict()
        index = list(d.keys())[0]
        return index, json.dumps(d[index])

    def provideIncrementalWithId(self):
        # todo: in the real stream, if the observationId is obviously
        #       a datetime in UTC, we could use that as the observed
        #       time, otherwise, we'll just use our own on update.
        key, content = self.provideObservation()
        return (
            '{'
            f'"source-id":"{self.sourceId}",'
            f'"stream-id":"{self.streamId}",'
            '"observed-time":"' + str(dt.datetime.utcnow()) +  '",'
            '"observation-id":' + str(key) +  ','
            '"content":' + content + '}')

    def run(self):
        while True:
            #time.sleep(0)
            response = requests.post(
                url=f'http://localhost:{self.port}/subscription/update', 
                json=self.provideIncrementalWithId())
            response.raise_for_status()
            #time.sleep(1)

# todo: we want this spoof to open the parquet file and see what the latest observation id is... do we save that in the parque file? probably not. actaully.
#       then it should resume sending from that point. to spoof a real stream.   
'''
from satori.lib.engine.structs import Observation
JSON = (
    '{'
    '"source-id":"streamrSpoof",'
    '"stream-id":"simpleEURCleaned",'
    '"observed-time":"2022-04-14 13:53:37.186105",'
    '"observation-id":3675,'
    '"content":{'
    '"High": 0.81856,'
    '"Low": 0.81337,'
    '"Close": 0.81512}}')
'''