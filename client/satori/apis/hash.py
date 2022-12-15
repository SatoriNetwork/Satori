# mainly used for generating unique ids for data and model paths since they must be short

import base64
import hashlib

from satori.engine.structs import StreamId


def generatePathId(path: str = None, streamId: StreamId = None):
    hasher = hashlib.sha1((path or streamId.idString()).encode('utf-8'))
    return base64.urlsafe_b64encode(hasher.digest())[:20]
