from functools import reduce
import pandas as pd

def merge(dfs:list[pd.DataFrame]):
    ''' Layer 1
    combines multiple mutlicolumned dataframes.
    to support disparate frequencies, 
    outter join fills in missing values with previous value.
    '''
    for df in dfs:
        df.index = pd.to_datetime(df.index)
    return reduce(
        lambda left, right: pd.merge(
            left, 
            right, 
            how='outer',
            left_index=True,
            right_index=True).fillna(method='ffill'),
        #.fillna(method='bfill'),
        # don't bfill here, in many cases its fine to bfill, but not in all.
        # maybe we will bfill in model. always bfill After ffill.
        dfs)


def appdendInsert(merged:pd.DataFrame, incremental:pd.DataFrame):
    ''' Layer 2
    after datasets merged one cannot merely append a dataframe. 
    we must insert the incremental at the correct location.
    this function is more of a helper function after we gather,
    to be used by models, it doesn't talk to disk directly.
    incremental is should be a multicolumn, one row DataFrame. 
    '''
    if incremental.index.values[0] in merged.index.values:
        merged.loc[incremental.index, [x for x in incremental.columns]] = incremental
    else:
        merged = merged.append(incremental).sort_index()
    return merged.fillna(method='ffill')