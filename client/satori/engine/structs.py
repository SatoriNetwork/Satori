import json
import pandas as pd
import datetime as dt
from satori import config
from functools import partial


class StreamId:
    ''' unique identifier for a stream '''

    def __init__(
        self,
        stream: str = None,
        source: str = None,
        target: str = None,
        author: str = None,
    ):
        self.author = author
        self.stream = stream
        self.target = target
        self.source = source  # or config.defaultSource()

    def id(self):
        return (self.author, self.source, self.stream, self.target)

    def __repr__(self):
        return str({
            'author': self.author,
            'source': self.source,
            'stream': self.stream,
            'target': self.target})

    def __str__(self):
        return str(self.__repr__())

    def key(self):
        return self.id()

    def new(
        self,
        author: str = None,
        source: str = None,
        stream: str = None,
        target: str = None,
        clearAuthor: bool = False,
        clearSource: bool = False,
        clearStream: bool = False,
        clearTarget: bool = False,
    ):
        return StreamId(
            author=None if clearAuthor else (author or self.author),
            source=None if clearSource else (source or self.source),
            stream=None if clearStream else (stream or self.stream),
            target=None if clearTarget else (target or self.target))
    # @staticmethod
    # def order(streamIds: list[StreamId]):
    #    ''' orders list such that streams '''
    #    return {(source, stream, targets) for sst in sourceStreamTargetss for source, stream, targets in sst.asTuples()}


class SourceStreamMap(dict):
    def __init__(self, content=None, source: str = None, stream: str = None):
        super(SourceStreamMap, self).__init__([
            ((source, stream), content)] if source is not None and stream is not None else [])

    def add(self, source, stream, value=None):
        return self.__setitem__((source, stream), value)


class StreamIdMap():
    def __init__(self, streamId: StreamId = None, value=None):
        self.d = {streamId: value}

    def __repr__(self):
        return str(self.d)

    def __str__(self):
        return str(self.__repr__())

    def add(self, streamId: StreamId, value=None):
        self.d[streamId] = value

    def addAll(self, streamIds: list[StreamId], values: list[StreamId]):
        for streamId, value in zip(streamIds, values):
            self.add(streamId, value)

    @staticmethod
    def _condition(key: StreamId, streamId: StreamId, default: bool = True):
        return all([
            x == k or (x is None and default)
            for x, k in zip(
                [streamId.author, streamId.source,
                    streamId.stream, streamId.target],
                [key.author, key.source, key.stream, key.target])])

    def erase(self, streamId: StreamId, greedy: bool = True):
        condition = partial(
            StreamIdMap._condition,
            streamId=streamId, default=greedy)
        erased = []
        for k in self.d.keys():
            if condition(k):
                erased.append(k)
        for k in erased:
            del self.d[k]
        return erased

    def getAll(self, streamId: StreamId = None, greedy: bool = True):
        if streamId is None:
            return self.d
        condition = partial(
            StreamIdMap._condition,
            streamId=streamId, default=greedy)
        return {k: v for k, v in self.d.items() if condition(k)}

    def isFilled(self, streamId: StreamId, greedy: bool = True):
        condition = partial(
            StreamIdMap._condition,
            streamId=streamId, default=greedy)
        matches = [
            self.d.get(k) is not None for k in self.d.keys() if condition(k)]
        return len(matches) > 0 and all(matches)

    def getAllAsList(self, streamId: StreamId = None, greedy: bool = True):
        matches = self.getAll(streamId, greedy=greedy)
        return [(k, v) for k, v in matches.items()]


class HyperParameter:

    def __init__(
        self,
        name: str = 'n_estimators',
        value=3,
        limit=1,
        minimum=1,
        maximum=10,
        kind: 'type' = int
    ):
        self.name = name
        self.value = value
        self.test = value
        self.limit = limit
        self.min = minimum
        self.max = maximum
        self.kind = kind


class Observation:

    def __init__(self, data):
        self.data = data
        self.parse(data)

    def parse(self, data):
        ''' {
                'source-id:"streamrSpoof",'
                'stream-id:"simpleEURCleaned",'
                'observation-id': 3675, 
                'observed-time': "2022-02-16 02:52:45.794120", 
                'content': {
                    'High': 0.81856, 
                    'Low': 0.81337, 
                    'Close': 0.81512}}
            note: if observed-time is missing, define it here.
        '''
        j = json.loads(data)
        self.sourceId = j['source-id']
        self.streamId = j['stream-id']
        self.observedTime = j.get('observed-time', str(dt.datetime.utcnow()))
        self.observationId = j['observation-id']
        self.content = j['content']
        if isinstance(self.content, dict):
            self.df = pd.DataFrame(
                {(self.sourceId, self.streamId, target): values for target, values in list(
                    self.content.items()) + [('StreamObservationId', self.observationId)]},
                # columns=pd.MultiIndex.from_tuples([(self.sourceId, self.streamId, self.)]),
                index=[self.observedTime])
        elif not isinstance(self.content, dict):
            self.df = pd.DataFrame(
                {(self.sourceId, self.streamId, self.streamId): [
                    self.content] + [('StreamObservationId', self.observationId)]},
                index=[self.observedTime])

    def key(self):
        return (self.sourceId, self.streamId)
