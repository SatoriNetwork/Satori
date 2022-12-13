import json
import pandas as pd
import datetime as dt
from satori import config
from functools import partial


class StreamId:
    ''' unique identifier for a stream '''

    def __init__(
        self,
        stream: str,
        source: str = 'Satori',
        target: str = None,
        publisher: str = None,
    ):
        self.publisher = publisher
        self.stream = stream
        self.target = target
        self.source = source or config.defaultSource()

    def id(self):
        return (self.publisher, self.source, self.stream, self.target)

    def __repr__(self):
        return {
            'publisher': self.publisher,
            'source': self.source,
            'stream': self.stream,
            'target': self.target}

    def __str__(self):
        return f'{self.publisher}:{self.source}:{self.stream}:{self.target}'

    def key(self):
        return self.id()


class SourceStreamMap(dict):

    def __init__(self, content=None, source: str = None, stream: str = None):
        super(SourceStreamMap, self).__init__([
            ((source, stream), content)] if source is not None and stream is not None else [])

    def add(self, source, stream, value=None):
        return self.__setitem__((source, stream), value)


class StreamIdMap():
    def __init__(self, publisher: str = None, source: str = None, stream: str = None, target: str = None, value=None):
        self.d = {(publisher, source, stream, target): value}

    def add(self, publisher, source, stream, target, value=None):
        self.d[(publisher, source, stream, target)] = value

    @staticmethod
    def _condition(x: list[str], publisher: str = None, source: str = None, stream: str = None, target: str = None, default: bool = False):
        return all([
            i is None or i == x[z]
            for i, z in zip([publisher, source, stream, target], range(4))])

    def erase(self, publisher: str = None, source: str = None, stream: str = None, target: str = None):
        condition = partial(
            StreamIdMap._condition,
            publisher=publisher, source=source, stream=stream, target=target)
        erased = []
        for k in self.d.keys():
            if condition(k):
                erased.append(k)
        for k in erased:
            del self.d[k]
        return erased

    def getAll(self, publisher: str = None, source: str = None, stream: str = None, target: str = None):
        condition = partial(
            StreamIdMap._condition,
            publisher=publisher, source=source, stream=stream, target=target)
        return {k: v for k, v in self.d.items() if condition(k)}

    def isFilled(self, publisher: str = None, source: str = None, stream: str = None, target: str = None):
        condition = partial(
            StreamIdMap._condition,
            publisher=publisher, source=source, stream=stream, target=target)
        matches = [
            self.d.get(k) is not None for k in self.d.keys() if condition(k)]
        return len(matches) > 0 and all(matches)

    def getAllAsList(self, publisher: str = None, source: str = None, stream: str = None, target: str = None):
        matches = self.getAll(publisher, source, stream, target)
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
