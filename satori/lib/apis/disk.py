#!/usr/bin/env python
# coding: utf-8

''' an api for reading and writing to disk '''

import pyarrow.parquet as pq
import pandas as pd
from satori import config
import os
import pyarrow as pa
from satori.lib.apis.memory import merge
from satori.lib.engine.structs import SourceStreamTargets

class Api(object):
    def __init__(self, df:pd.DataFrame, source:str=None, stream:str=None, location:str=None, append:bool=None, ext:str='parquet'):
        self.df = df
        self.source = source
        self.stream = stream
        self.location = location
        self.ext = ext
        
    def path(self):
        ''' Layer 0 get the path of a file '''
        return os.path.join(
                self.location or config.dataPath(),
                self.source or config.defaultSource,  
                f'{self.stream}.{self.ext}'),

    def exists(self):
        ''' Layer 0 return True if file exists at path, else False '''
        return os.path.exists(self.path())

    def write(self, df:pd.DataFrame,  append:bool=None):
        ''' Layer 1
        writes a dataframe to a parquet file.
        must remove multiindex column first.
        must use write_to_dataset rather than write_to_table to support append.
        streamId is the name of file.
        '''
        append = append or self.exists()
        df = df or self.df
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel() # source
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel() # stream
        pq.write_to_dataset((
                pa.Table.from_pandas(df) if append else
                pa.Table.from_pandas(df).replace_schema_metadata(None)),
            self.path())

    def read(self, source:str, stream:str, **kwargs):
        ''' Layer 1
        reads a parquet file with filtering, use columns=[targets].
        adds on the stream as first level in multiindex column on dataframe.
        '''
        source = source or self.source or self.df.columns.levels[0]
        stream = stream or self.stream or self.df.columns.levels[1]
        rdf = pq.read_table(self.path(), **kwargs).to_pandas()
        rdf.columns = pd.MultiIndex.from_product([[source], [stream], rdf.columns])
        return rdf
        
    
    def gather(
        self, 
        targetsByStreamBySource:dict[str, dict[str, list[str]]]=None,
        targetsByStream:dict[str, list[str]]=None,
        targets:list[str]=None,
        sourceStreamTargets:list=None,
        sourceStreamTargetss:list[SourceStreamTargets]=None,
        source:str=None,
        stream:str=None,
    ):
        ''' Layer 2. retrieves the targets and merges them. '''
        if sourceStreamTargetss is not None:
            return merge([
                self.read(source, stream, columns=targets)
                for source, stream, targets in SourceStreamTargets.condense(sourceStreamTargetss)])
        if sourceStreamTargets is not None:
            return merge([
                self.read(source, stream, columns=targets)
                for source, stream, targets in sourceStreamTargets])
        if targets is not None:
            return merge([
                self.read(
                    source or self.source,
                    stream or self.stream,
                    columns=targets)])
        if targetsByStream is not None:
            return merge([
                self.read(
                    source or self.source,
                    stream, columns=targets)
                for stream, targets in targetsByStream.items()])
        if targetsByStreamBySource is not None:
            return merge([
                self.read(source, stream, columns=targets)
                for source, values in targetsByStreamBySource.items()
                for stream, targets in values
                ])