import os
import json
from functools import partial
from .config import root, get, put, env, var


root = partial(root, os.path.abspath(__file__))
get = partial(get, root=root)
put = partial(put, root=root)
env = partial(env, get=get, root=root)

settingsPathName = 'SATORI_SETTINGS_PATH'
defaultSource = 'streamr'

def settingsPath():
    '''
    the settings path is where a file lives that tells satori
    how it is setup to run. if the file doesn't exist or is empty
    satori assumes this is the first time it has ever run and will
    take the user through steps to create a settings file.
    preliminary outline of a .satori.json file:
    {
        "publications": {
            "stream id": "details"
        },
        "data path": "/repos/satori/data",
        "model path": "/repos/satori/models",
        "realtive data path": "./data",
        "realtive model path": "./models"
    }
    '''
    
    return var(settingsPathName) or root('../.satori.json')

def settings():
    ''' returns a dictionary of settings '''
    if os.path.exists(settingsPath()):
        try: 
            with open(settingsPath(), 'r') as f:
                return json.load(f)
        except Exception as e:
            print(e)
    return {}

def getPath(of='data'):
    ''' used to get the data or model path '''
    satoriSattings = settings()
    return satoriSattings.get(
        f'{of} path', 
        satoriSattings.get(
            f'relative {of} Path', 
            root(f'../{of}')))

def dataPath(filename=None):
    ''' data path takes presidence over relative data path if both exist '''
    if filename:
        return os.path.join(getPath(of='data'), filename)
    return getPath(of='data')

def modelPath(filename=None):
    ''' model path takes presidence over relative model path if both exist '''
    if filename:
        return os.path.join(getPath(of='model'), filename)
    return getPath(of='model')

def dataSettings():
    '''
    data settings is the first thing we retrieve when starting up the app
    it needs to hold information about where all the data is it is contained
    within the data folder. Perhaps this could be contained in the .satori.json
    but that was thought of as more of a user defined settings rather than 
    something the engine would continually modify.
    prelimiary outline of .data.json:
    {
        "subscription database": "EUR=X-simpleCleaned.csv"
        "ancillary database": "ancilarydb.parquet"
    }
    '''
    path = dataPath('.data.json')
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(e)
    return {}