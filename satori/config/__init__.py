import os
from functools import partial
from .config import root, read, write, get, put, env, var


root = partial(root, os.path.abspath(__file__))
read = partial(read, root=root)
write = partial(write, root=root)
get = partial(get, root=root)
put = partial(put, root=root)
env = partial(env, get=get, root=root)

def manifest(): 
    return config.get('manifest') or {}

def modify(data: dict): 
    ''' modifies the config yaml without erasing comments (unlike put) '''
    
    def extractKey(line: str):
        return line.replace('#', '').strip().split(':')[0]
    
    replacement = []
    for line in read():
        key = extractKey(line)
        if key in data.keys():
            replacement.append(f'{key}: {data[key]}')
        else:
            replacement.append(line)
    write(lines=replacement)

def flaskPort(): 
    return config.get().get('user interface port', '24685')

def nodejsPort(): 
    return config.get().get('streamr light client port', '24686')

def defaultSource(): 
    return get().get('default source of data streams', 'streamr')

def path(of='data'):
    ''' used to get the data or model path '''
    return get().get(f'absolute {of} path', root(f'../{of}'))

def dataPath(filename=None):
    ''' data path takes presidence over relative data path if both exist '''
    if filename:
        return os.path.join(path(of='data'), filename)
    return path(of='data')

def modelPath(filename=None):
    ''' model path takes presidence over relative model path if both exist '''
    if filename:
        return os.path.join(path(of='model'), filename)
    return path(of='model')
