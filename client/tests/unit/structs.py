from satori.engine.structs import StreamId, StreamIdMap


def testStreamIdMap():
    x0 = StreamId(author='a', source='b', stream='c', target=None)
    x1 = StreamId(author='a', source='b', stream='c', target='d')
    x2 = StreamId(author='a', source='b', stream='c', target='e')
    x3 = StreamId(author='a', source='z', stream='z', target='e')
    x4 = StreamId(author='a', source='z', stream='c', target='e')
    x = StreamIdMap(x0, 0)
    x.addAll([x1, x2, x3, x4], [1, 2, 3, 4])
    assert x.getAll(x1.new(clearTarget=True), greedy=True) == {
        x0: 0, x1: 1, x2: 2}
    assert x.getAll(x1.new(clearTarget=True), greedy=False) == {x0: 0, }
    assert x.getAll(x2.new(clearSource=True), greedy=True) == {x2: 2, x4: 4}
    assert x.isFilled(x1.new(clearTarget=True), greedy=True) == True
    assert x.isFilled(x1.new(clearTarget=True), greedy=False) == True
    assert x.isFilled(x2.new(clearSource=True), greedy=True) == True
    assert x.isFilled(x2.new(author='z'), greedy=True) == False
    assert x.erase(x2.new(author='z'), greedy=True) == []
    assert x.erase(x2.new(clearSource=True), greedy=True) == [x2, x4]
    assert x.getAll(x2.new(clearSource=True), greedy=True) == {}
