# > python satori\spoof\streamr.py

import time
import json
import requests
import datetime as dt
import pandas as pd
from satori import config
from satori.apis import disk
from satori.concepts.structs import StreamId


class Streamr():
    def __init__(self, source: str = None, author: str = None, stream: str = None):
        self.source = source or 'streamrSpoof'
        self.author = author or 'pubkey'
        self.stream = stream or 'simpleEURCleaned'
        df = pd.read_csv(config.root('lib', 'spoof', f'{stream}.csv'))
        existing = disk.Disk(
            StreamId=StreamId(
                source=self.source,
                author=self.author,
                stream=self.stream)).read()
        past = existing.shape[0] if existing is not None else 0
        self.past = df.iloc[:past]
        self.future = df.iloc[past:]
        self.port = config.flaskPort()
        self.incremental = self.getNewData()

    def getNewData(self):  # -> pd.DataFrame:
        ''' incrementally returns mock future data to simulate the passage of time '''
        for i in self.future.index:
            yield pd.DataFrame(self.future.loc[i]).T

    def providePast(self):
        ''' provides the past as json '''
        return self.past.T.to_json()

    def provideIncremental(self):
        ''' observation with row id '''
        return next(self.incremental).T.to_json()

    def provideObservation(self):  # -> int, string:
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
            f'"source":"{self.source}",'
            f'"source":"{self.author}",'
            f'"stream":"{self.stream}",'
            '"time":"' + str(dt.datetime.utcnow()) + '",'
            '"observation":' + str(key) + ','
            '"content":' + content + '}')

    def run(self):
        while True:
            time.sleep(3)
            x = self.provideIncrementalWithId()
            response = requests.post(
                url=f'http://127.0.0.1:{self.port}/subscription/update',
                json=x)
            response.raise_for_status()


'''
from satori.lib.engine.structs import Observation
JSON = (
    '{'
    '"source":"streamrSpoof",'
    '"stream":"simpleEURCleaned",'
    '"time":"2022-04-14 13:53:37.186105",'
    '"observation":3675,'
    '"content":{'
    '"High": 0.81856,'
    '"Low": 0.81337,'
    '"Close": 0.81512}}')
'''
