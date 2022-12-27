import json
import pandas as pd
import datetime as dt
# from satori import config
from functools import partial


class StreamId:
    ''' unique identifier for a stream '''

    def __init__(
        self,
        source: str = None,
        author: str = None,
        stream: str = None,
        target: str = None,
    ):
        self.source = source  # or config.defaultSource()
        self.author = author
        self.stream = stream
        self.target = target

    def topic(self, asJson: bool = True):
        '''
        the topic (id) for this stream. 
        this is how the pubsub system identifies the stream.
        '''
        if asJson:
            return json.dumps(self.keyedId(asJson=False))
        return {'source': self.source, 'author': self.author, 'stream': self.stream, 'target': self.target}

    def id(self):
        return (self.source, self.author, self.stream, self.target)

    def idString(self):  # todo: make this .id and the .key a tuple
        return (self.source or '') + (self.author or '') + (self.stream or '') + (self.target or '')

    def __repr__(self):
        return str({
            'source': self.source,
            'author': self.author,
            'stream': self.stream,
            'target': self.target})

    def __str__(self):
        return str(self.__repr__())

    def filled(self):
        ''' all fields are filled '''
        return self.source is not None and self.author is not None and self.stream is not None and self.target is not None

    def potentiallyFilled(self):
        '''
        some streams may not have a target or author. but they all come from a 
        source and have a stream id
        '''
        return self.source is not None and self.stream is not None

    def key(self):
        return self.id()

    def new(
        self,
        source: str = None,
        author: str = None,
        stream: str = None,
        target: str = None,
        clearAuthor: bool = False,
        clearSource: bool = False,
        clearStream: bool = False,
        clearTarget: bool = False,
    ):
        return StreamId(
            source=None if clearSource else (source or self.source),
            author=None if clearAuthor else (author or self.author),
            stream=None if clearStream else (stream or self.stream),
            target=None if clearTarget else (target or self.target))

    @staticmethod
    def fromMap(map: dict = None):
        return StreamId(
            source=(map or {}).get('source'),
            author=(map or {}).get('author'),
            stream=(map or {}).get('stream'),
            target=(map or {}).get('target'))


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

    def keys(self):
        return self.d.keys()

    def streams(self):
        return {k.new(clearTarget=True) for k in self.keys()}

    @staticmethod
    def _condition(key: StreamId, streamId: StreamId, default: bool = True):
        return all([
            x == k or (x is None and default)
            for x, k in zip(
                [streamId.source, streamId.author,
                    streamId.stream, streamId.target],
                [key.source, key.author, key.stream, key.target])])

    def remove(self, streamId: StreamId, greedy: bool = True):
        condition = partial(
            StreamIdMap._condition,
            streamId=streamId, default=greedy)
        removed = []
        for k in self.d.keys():
            if condition(k):
                removed.append(k)
        for k in removed:
            del self.d[k]
        return removed

    def get(self, streamId: StreamId = None, default=None, greedy: bool = False):
        if streamId is None:
            return self.d
        condition = partial(
            StreamIdMap._condition,
            streamId=streamId, default=greedy)
        matches = [
            self.d.get(k) for k in self.d.keys() if condition(k)]
        return matches[0] if len(matches) > 0 else default

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

    def __init__(self, data: dict):
        self.data = data
        self.parse(data)

    def parse(self, data):
        ''' {
                'source:"streamrSpoof",'
                'author:"pubkey",'
                'stream:"simpleEURCleaned",'
                'observation': 3675, 
                'time': "2022-02-16 02:52:45.794120", 
                'content': {
                    'High': 0.81856, 
                    'Low': 0.81337, 
                    'Close': 0.81512}}
            note: if observed-time is missing, define it here.
        '''
        if isinstance(data, str):
            j = json.loads(data)
        elif isinstance(data, dict):
            j = data
        elif isinstance(data, tuple):
            for k, v in data:
                j[k] = v
        else:
            j = data
        self.source = j.get('source', None)
        self.author = j.get('author', None)
        self.stream = j.get('stream', None)
        self.observedTime = j.get('time', str(dt.datetime.utcnow()))
        self.observationId = j.get('observation', None)
        self.content = j.get('content', {})
        self.target = None
        self.value = None
        if isinstance(self.content, dict):
            if len(self.content.keys()) == 1:
                self.target = self.content.keys()[0]
                self.value = self.content.get(self.target)
            self.df = pd.DataFrame(
                {(self.source, self.author, self.stream, target): values for target, values in list(
                    self.content.items()) + (
                        [('StreamObservationId', self.observationId)]
                        if self.observationId is not None else [])},
                index=[self.observedTime])
        elif not isinstance(self.content, dict):
            self.value = self.content
            self.df = pd.DataFrame(
                {(self.source, self.author, self.stream, self.stream): [
                    self.content] + (
                        [('StreamObservationId', self.observationId)]
                        if self.observationId is not None else [])},
                index=[self.observedTime])

    def key(self):
        return StreamId(
            source=self.source,
            author=self.author,
            stream=self.stream,
            target=self.target)
