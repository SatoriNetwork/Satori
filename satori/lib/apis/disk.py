#!/usr/bin/env python
# coding: utf-8

''' an api for reading and writing to disk '''

import pyarrow.parquet as pq
import numpy as np
import pandas as pd
from satori import config
import os
import pyarrow as pa
from functools import reduce

ext = 'parquet'

def path(stream:str=None, location:str=None):
    ''' Layer 0 get the path of a file '''
    return os.path.join(
            location or config.dataPath(),  
            f'{stream}.{ext}'),

def exists(stream:str=None, location:str=None):
    ''' Layer 0 return True if file exists at path, else False '''
    return os.path.exists(path(stream, location))

def write(df:pd.DataFrame, stream:str=None, location:str=None, append:bool=None):
    ''' Layer 1
    writes a dataframe to a parquet file.
    must remove multiindex column first.
    must use write_to_dataset rather than write_to_table to support append.
    streamId is the name of file.
    '''
    stream = stream or df.columns.levels[0][0]
    append = append or exists(stream, location)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel()
    pq.write_to_dataset((
            pa.Table.from_pandas(df) if append else
            pa.Table.from_pandas(df).replace_schema_metadata(None)),
        path(stream, location))

def read(stream:str=None, location:str=None, df:pd.DataFrame=None, **kwargs):
    ''' Layer 1
    reads a parquet file with filtering, use columns=[targets].
    adds on the stream as first level in multiindex column on dataframe.
    '''
    stream = stream or df.columns.levels[0]
    rdf = pq.read_table(
        path(stream, location),
        **kwargs).to_pandas()
    rdf.columns = pd.MultiIndex.from_product([[stream], rdf.columns])
    return rdf
    
    
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

def gather(targetsByStream:dict[str, list[str]]):
    ''' Layer 2. retrieves the targets and merges them. '''
    return merge([read(key, columns=values) for key, values in targetsByStream.items()])

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