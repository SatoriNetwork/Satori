#!/usr/bin/env python
# coding: utf-8

''' an api for reading and writing to disk '''

import shutil
import pyarrow.parquet as pq
import pandas as pd
from satori import config
import os
import joblib
import pyarrow as pa
from satori.apis import memory
from satori.apis.hash import generatePathId
from satori.engine.interfaces.data import DataDiskApi
from satori.engine.interfaces.model import ModelDataDiskApi, ModelDiskApi
from satori.engine.interfaces.wallet import WalletDiskApi
from satori.engine.structs import StreamId


def safetify(path: str):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    return path


class WalletApi(WalletDiskApi):

    @staticmethod
    def save(wallet, walletPath: str = None):
        walletPath = walletPath or config.walletPath()
        safetify(walletPath)
        config.put(data=wallet, path=walletPath)

    @staticmethod
    def load(walletPath: str = None):
        walletPath = walletPath or config.walletPath()
        if os.path.exists(walletPath):
            return config.get(walletPath)
        return False


class ModelApi(ModelDiskApi):

    @staticmethod
    def defaultModelPath(streamId: StreamId):
        return config.root(
            '..', 'models',
            streamId.source, streamId.author, streamId.stream,
            streamId.target + '.joblib')

    @staticmethod
    def save(model, modelPath: str = None, hyperParameters: list = None, chosenFeatures: list = None):
        ''' save to joblib file '''
        def appendAttributes(model, hyperParameters: list = None, chosenFeatures: list = None):
            if hyperParameters is not None:
                model.savedHyperParameters = hyperParameters
            if chosenFeatures is not None:
                model.savedChosenFeatures = chosenFeatures
            return model

        modelPath = modelPath or config.modelPath()
        safetify(modelPath)
        model = appendAttributes(model, hyperParameters, chosenFeatures)
        joblib.dump(model, modelPath)

    @staticmethod
    def load(modelPath: str = None):
        modelPath = modelPath or config.modelPath()
        if os.path.exists(modelPath):
            return joblib.load(modelPath)
        return False

    @staticmethod
    def getModelRootSize(modelPath: str = None):
        total = 0
        with os.scandir(modelPath) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += ModelApi.getModelRootSize(entry.path)
        return total

    @staticmethod
    def getModelSize(modelPath: str = None):
        if os.path.isfile(modelPath):
            return os.path.getsize(modelPath)
        elif os.path.isdir(modelPath):
            return ModelApi.getModelRootSize(modelPath)


class Disk(DataDiskApi, ModelDataDiskApi):
    ''' single point of contact for interacting with disk '''

    def __init__(
        self,
        df: pd.DataFrame = None,
        id: StreamId = None,
        loc: str = None,
        ext: str = 'parquet',
        **kwargs,
    ):
        self.memory = memory.Memory
        self.setAttributes(df=df, id=id, loc=loc, ext=ext, **kwargs)

    def setAttributes(
        self,
        df: pd.DataFrame = None,
        id: StreamId = None,
        loc: str = None,
        ext: str = 'parquet',
        **kwargs,
    ):
        self.df = df if df is not None else pd.DataFrame()
        self.id = id or StreamId(
            source=kwargs.get('source'),
            author=kwargs.get('author'),
            stream=kwargs.get('stream'))
        self.loc = loc
        self.ext = ext
        return self

    @staticmethod
    def safetify(path: str):
        return safetify(path)

    @staticmethod
    def defaultModelPath(streamId: StreamId):
        ModelApi.defaultModelPath(streamId)

    @staticmethod
    def saveModel(model, modelPath: str = None, hyperParameters: list = None, chosenFeatures: list = None):
        ModelApi.save(
            model,
            modelPath=modelPath,
            hyperParameters=hyperParameters,
            chosenFeatures=chosenFeatures)

    @staticmethod
    def loadModel(modelPath: str = None):
        return ModelApi.load(modelPath=modelPath)

    @staticmethod
    def saveWallet(wallet, walletPath: str = None):
        WalletApi.save(wallet, walletPath=walletPath)

    @staticmethod
    def loadWallet(walletPath: str = None):
        return WalletApi.load(walletPath=walletPath)

    @staticmethod
    def getModelSize(modelPath: str = None):
        return ModelApi.getModelSize(modelPath)

    def setId(self, id: StreamId = None, source: str = None, author: str = None, stream: str = None):
        self.id = id or StreamId(source=source, author=author, stream=stream)

    def path(self, permanent: bool = False):
        ''' Layer 0 get the path of a file '''
        return safetify(os.path.join(
            self.loc or config.dataPath(),
            # here we can make a path id that holds both the permanent and incremental data.
            generatePathId(self.id),
            'permanent' if permanent else 'incremental',
            self.id.source or config.defaultSource(),  # this should be the dataframe only
            self.id.author,  # this should be the dataframe only
            f'{self.id.stream}.{self.ext}'  # this should be the dataframe only
        ))

    def exists(self, permanent: bool = False,):
        ''' Layer 0 return True if file exists at path, else False '''
        return os.path.exists(self.path(permanent))

    def reduceMulti(self, df: pd.DataFrame):
        ''' Layer 0 '''
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel()  # source
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel()  # author
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel()  # stream
        return df

    def toTable(self, df: pd.DataFrame = None):
        ''' Layer 0 '''
        return pa.Table.from_pandas(self.reduceMulti(df if df is not None else self.df))

    def incrementals(self):
        ''' Layer 0 '''
        return os.listdir(self.path())

    def append(self, df: pd.DataFrame = None):
        ''' Layer 1
        writes a dataframe to a parquet file.
        must remove multiindex column first.
        must use write_to_dataset rather than write_to_table to support append.
        streamId is the name of file.
        '''
        pq.write_to_dataset(self.toTable(df), self.path())

    def write(self, df: pd.DataFrame = None):
        ''' Layer 1
        writes a dataframe to a parquet file.
        must remove multiindex column first.
        streamId is the name of file.
        '''
        pq.write_table(self.toTable(df), self.path(permanent=True))

    def compress(self):
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
        df = self.readBoth()
        if df is not None:
            self.remove(True)
            self.write(df)
            self.remove(False)

    def remove(self, permanent: bool = None):
        ''' Layer 1 when we don't use a stream anymore we'll remove it '''
        if permanent is None:
            self.remove(True)
            self.remove(False)
        elif permanent:
            if self.exists(permanent):
                os.remove(self.path(permanent))
        else:
            shutil.rmtree(self.path(), ignore_errors=True)

    def readBoth(self, **kwargs):
        ''' Layer 1 
        read both the permanent and incremental tables into memory
        merge them into one dataframe
        '''
        return self.merge(
            self.read(permanent=False, **kwargs),
            self.read(permanent=True, **kwargs))

    def merge(self, df: pd.DataFrame, long: pd.DataFrame, ):
        ''' Layer 1 
        meant to merge long term (permanent) written tables 
        with short term (incremental) appended datasets
        for one stream
        '''
        def dropDuplicates(df: pd.DataFrame):
            return df.drop_duplicates(subset=(self.id.source, self.id.author, self.id.stream, 'StreamObservationId'), keep='last').sort_index()

        if df is None and long is None:
            return None
        if df is None:
            return dropDuplicates(long)
        if long is None:
            return dropDuplicates(df)
        df['TempIndex'] = df.index
        long['TempIndex'] = long.index
        df = pd.merge(df, long, how='outer', on=list(df.columns))
        df.index = df['TempIndex']
        df.index.name = None
        df = df.drop('TempIndex', axis=1, level=0)
        return dropDuplicates(df)

    def read(self, permanent: bool = None, **kwargs):
        ''' Layer 1
        reads a parquet file with filtering, use columns=[targets].
        adds on the stream as first level in multiindex column on dataframe.
        Since we compress incremental observations into long term storage we
        really have 2 datasets per stream to look up, thus we specify permanent
        as None in order to pull from both datasets and merge automatically.
        '''
        def conform(**kwargs):
            if 'columns' in kwargs.keys():
                if 'StreamObservationId' not in kwargs.get('columns', []):
                    kwargs['columns'].append('StreamObservationId')
                if '__index_level_0__' not in kwargs.get('columns', []):
                    kwargs['columns'].append('__index_level_0__')
            return kwargs

        source = self.id.source or self.df.columns.levels[0]
        author = self.id.author or self.df.columns.levels[1]
        stream = self.id.stream or self.df.columns.levels[2]
        if permanent is None:
            return self.readBoth(**kwargs)
        if not self.exists(permanent):
            return None
        rdf = pq.read_table(
            self.path(permanent),
            **conform(**kwargs)).to_pandas()
        if '__index_level_0__' in rdf.columns:
            rdf.index = rdf.loc[:, '__index_level_0__']
            rdf.index.name = None
            rdf = rdf.drop('__index_level_0__', axis=1)
        rdf.columns = pd.MultiIndex.from_product(
            [[source], [author], [stream], rdf.columns])
        return rdf.sort_index()

    def savePrediction(self, path: str = None, prediction: str = None):
        ''' Layer 1 - saves prediction to disk '''
        safetify(path)
        with open(path, 'a') as f:
            f.write(prediction)

    def gather(
        self,
        targetColumn: 'str|tuple[str]',
        streamIds: list[StreamId] = None,
    ):
        ''' Layer 2. 
        retrieves the targets and merges them.
        '''
        def dropIf(df: pd.DataFrame, column: tuple):
            if df is not None:
                return df.drop(column, axis=1)

        def filterNone(items: list):
            return [x for x in items if x is not None]

        # if streamIds is not None:
        #    return self.memory.merge(filterNone([
        #        dropIf(self.read(publisher, self.id.source, self.id.stream, columns=targets),
        #               (self.id.source, self.id.stream, 'StreamObservationId'))
        #        for publisher, self.id.source, self.id.stream, targets in StreamId.condense(streamIds)]),
        #        targetColumn=targetColumn)
        # return dropIf(self.read(self.id.source, self.id.stream), (self.id.source, self.id.stream, 'StreamObservationId'))

        if streamIds is not None:
            items = []
            for source, author, stream, targets in StreamId.condense(streamIds):
                self.setId(source=source, author=author, stream=stream)
                items.append(dropIf(
                    df=self.read(columns=targets),
                    column=(source, author, stream, 'StreamObservationId')))
            return self.memory.merge(
                dfs=filterNone(items),
                targetColumn=targetColumn)
        return dropIf(self.read(), (self.id.source, self.id.author, self.id.stream, 'StreamObservationId'))


'''
from satori.lib.apis import disk
x = disk.Api(source='streamrSpoof', stream='simpleEURCleaned') 
df = x.read()
df
x.read(columns=['High'])
exit()

'''
