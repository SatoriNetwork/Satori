from satori.engine.structs import StreamIdMap


def testStreamIdMap():
    x = StreamIdMap('a', 'b', 'c', 'd', 1)
    x.add('a', 'b', 'c', 'e', 2)
    x.add('a', 'z', 'c', 'e', 3)
    assert x.isFilled('a', 'z', 'c', 'e') == True
    assert x.isFilled('a', 'b', 'c', 'd') == True
    assert x.isFilled('a', 'b', 'c', 'z') == False
    assert x.erase('a', 'b', 'c', 'z') == []
    assert x.isFilled('a', 'z', 'c', 'e') == True
    assert x.erase('a', 'z', 'c', 'e') == [('a', 'z', 'c', 'e')]
    assert x.isFilled('a', 'z', 'c', 'e') == False
    assert x.getAll('a', 'b', 'c', 'd') == {('a', 'b', 'c', 'd'): 1}
    assert x.getAll('a', 'b', 'c') == {
        ('a', 'b', 'c', 'd'): 1, ('a', 'b', 'c', 'e'): 2}
    assert x.getAll('a') == {('a', 'b', 'c', 'd'): 1, ('a', 'b', 'c', 'e'): 2}
    assert x.getAllAsList(
        'a') == [(('a', 'b', 'c', 'd'), 1), (('a', 'b', 'c', 'e'), 2)]
