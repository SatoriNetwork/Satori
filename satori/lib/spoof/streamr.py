# > python satori\spoof\streamr.py   

import time 
import requests
import datetime as dt
import pandas as pd
import satori
import json

df = pd.read_csv(satori.config.root('lib', 'spoof', 'simpleEURCleaned.csv'))
past = df.iloc[:round(df.shape[0]*.8)]
future = df.iloc[round(df.shape[0]*.8):]
port = satori.config.get()['port']

def getNewData(): # -> pd.DataFrame:
    ''' incrementally returns mock future data to simulate the passage of time '''
    for i in future.index:
        yield pd.DataFrame(future.loc[i]).T

incremental = getNewData()

def providePast():
    ''' provides the past as json '''
    return past.T.to_json()

def provideIncremental():
    ''' observation with row id '''
    return next(incremental).T.to_json()
    
def provideObservation(): # -> int, string:
    d = next(incremental).T.to_dict()
    index = list(d.keys())[0]
    return index, json.dumps(d[index])

def provideIncrementalWithId():
    # todo: in the real stream, if the observationId is obviously
    #       a datetime in UTC, we could use that as the observed
    #       time, otherwise, we'll just use our own on update.
    key, content = provideObservation()
    return (
        '{"simpleEURCleaned":{'
        '"observed-time":' + str(dt.datetime.utcnow()) +  ','
        '"observation-id":' + str(key) +  ','
        '"content":' + content + '}}')

def streamr():
    while True:
        time.sleep(5)
        response = requests.post(
            url=f'http://localhost:{port}/subscription/update', 
            json=provideIncrementalWithId())
        response.raise_for_status()
        time.sleep(25)