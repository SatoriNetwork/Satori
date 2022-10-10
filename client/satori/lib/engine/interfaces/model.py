import pandas as pd

from satori.lib.engine.structs import SourceStreamTarget


class ModelMemoryApi():
    @staticmethod    
    def appendInsert(df:pd.DataFrame, incremental:pd.DataFrame):
        ''' Layer 2
        after datasets merged one cannot merely append a dataframe. 
        we must insert the incremental at the correct location.
        this function is more of a helper function after we gather,
        to be used by models, it doesn't talk to disk directly.
        incremental is should be a multicolumn, one row DataFrame. 
        '''


            
class ModelDataDiskApi():
    @staticmethod
    def saveModel(model, modelPath:str=None, hyperParameters:list=None, chosenFeatures:list=None):
        ''' saves model using ModelDiskApi'''
    
    @staticmethod
    def loadModel(model):
        ''' loads model using ModelDiskApi'''
        
    def gather(
        self, 
        targetColumn:'str|tuple[str]',
        sourceStreamTargets:list[SourceStreamTarget],
    ):
        ''' Layer 2. 
        retrieves the targets and merges them.
        '''

class ModelDiskApi(object):
    
    @staticmethod
    def save(model, modelPath:str=None, hyperParameters:list=None, chosenFeatures:list=None):
        ''' saves model to disk '''
    
    @staticmethod
    def load(modelPath:str=None):
        ''' loads model from disk '''
                