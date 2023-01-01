# mainly used for generating unique ids for data and model paths since they must be short

import base64
import hashlib

from satori.concepts.structs import StreamId


def generatePathId(path: str = None, streamId: StreamId = None):
    hasher = hashlib.sha1((path or streamId.idString()).encode('utf-8'))
    removals = r'\/:*?"<>|'
    ret = base64.urlsafe_b64encode(hasher.digest())
    for char in removals:
        if char in ret:
            ret = ret.replace(char, '-')
    return ret
