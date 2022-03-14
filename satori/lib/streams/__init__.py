import time
from reactivex import Subject
from reactivex.subject import BehaviorSubject

def buildBuildingStream():
    ''' {name: bool}
    name: modelId
    true: primary model is building
    '''
    return Subject()

def buildPredictionStream():
    ''' {reason: result}
    reasons:
        'primary'   # new primary (data)
        'secondary' # new secondary (data)
        'model'     # new model
    result:
        float   # new primary (data)
        float   # new secondary (data)
        model   # new model
    }
    '''
    return Subject()

# model listens to 
building = buildBuildingStream()
rebuildPrediction = buildPredictionStream()

# model maker listens to 
# new data available stream = Subject()