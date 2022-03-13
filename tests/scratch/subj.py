import time
from reactivex import Subject

class Hello(object):
    def __init__(self):
        self.count = 0
        self.events = Subject()
    
    def doit(self):
        self.events.on_next({'source': 'hellow world', 'data': 'clicked', 'count':self.count})
        
import time
from reactivex.subject import BehaviorSubject

class Hello2(object):
    def __init__(self):
        self.count = 0
        self.events = Subject()
    
    def doit(self):
        self.count +=1
        self.events.on_next({'source': 'hellow world', 'data': 'clicked', 'count':self.count})

if __name__ == '__main__':
    h = Hello2()
    h.events.subscribe(lambda x: print(f'cliked: {x["count"]}'))
    time.sleep(1)
    h.doit()
    h.doit()
    time.sleep(1)
    h.doit()
    h.doit()
    exit();
