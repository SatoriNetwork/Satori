import pandas as pd
from satori.lib.engine.structs import SourceStreamTargets

            
class DataDiskApi():
    
    def setAttributes(self, df:pd.DataFrame=None, source:str=None, stream:str=None, location:str=None, append:bool=None, ext:str='parquet'):
        ''' setter for any and all attributes, like __init__ returns self '''

    def incrementals(self, source:str=None, stream:str=None):
        ''' Layer 0 '''

    def append(self, df:pd.DataFrame=None):
        ''' Layer 1
        writes a dataframe to a parquet file.
        must remove multiindex column first.
        must use write_to_dataset rather than write_to_table to support append.
        streamId is the name of file.
        '''

    def compress(self, source:str=None, stream:str=None):
        ''' Layer 1
        assumes columns are always the same...
        this function is used on rare occasion to compress the on disk 
        incrementally saved data to long term storage. The compressed
        table takes up less room than the dataset because the dataset
        is partitioned into many files, allowing us to easily append
        to it. So we normally append observations to the dataset, and
        occasionally, like daily or weekly, run this compress function
        to save it to long term storage. We can still query long term
        storage the same way.
        '''
        
    def savePrediction(self, path:str=None, prediction:str=None):
        ''' Layer 1 - saves prediction to disk '''
            
class ModelDataDiskApi():
    @staticmethod
    def saveModel(model, modelPath:str=None, hyperParameters:list=None, chosenFeatures:list=None):
        ''' saves model using ModelDiskApi'''
    
    @staticmethod
    def loadModel(model, modelPath:str=None, hyperParameters:list=None, chosenFeatures:list=None):
        ''' loads model using ModelDiskApi'''
        
    def gather(
        self, 
        targetColumn:'str|tuple[str]',
        targetsByStreamBySource:dict[str, dict[str, list[str]]]=None,
        targetsByStream:dict[str, list[str]]=None,
        targets:list[str]=None,
        sourceStreamTargets:list=None,
        sourceStreamTargetss:list[SourceStreamTargets]=None,
        source:str=None,
        stream:str=None,
    ):
        ''' Layer 2. 
        retrieves the targets and merges them.
        as a prime example of premature optimization I made 
        this function callable in a myriad of various ways...
        I don't remember why.
        '''

class WalletDiskApi(object):
    
    @staticmethod
    def save(wallet, walletPath:str=None):
        ''' saves wallet to disk '''
    
    @staticmethod
    def load(walletPath:str=None):
        ''' loads wallet from disk'''

class ModelDiskApi(object):
    
    @staticmethod
    def save(model, modelPath:str=None, hyperParameters:list=None, chosenFeatures:list=None):
        ''' saves model to disk '''
    
    @staticmethod
    def load(modelPath:str=None):
        ''' loads model from disk '''
        