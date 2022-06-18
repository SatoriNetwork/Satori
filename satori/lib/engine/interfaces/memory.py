import pandas as pd


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
        