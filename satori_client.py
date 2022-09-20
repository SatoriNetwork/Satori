import websocket
import _thread
import time
import rel
import json

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

import threading
import random
import string


# Global Variables
clientConfiguration = None
primarySubscription = None
ws = None
connectAndJoinedToChannel = False


def on_message(ws, message):
    print("RECEIVED_SOCKET_MESSAGE: ", message)

    messageJson = json.loads(message)
    payload = messageJson["payload"]
    global connectAndJoinedToChannel
    if connectAndJoinedToChannel == False:
        if payload["status"] == "ok":
            connectAndJoinedToChannel = True
            # sendHeartbeat()
            thread = threading.Thread(target=publish_every_n_seconds, daemon=True)
            thread.start()


    event = messageJson["event"]
    if event == "published_observation":
        print("PUBLISHED_OBSERVATION: ", payload)





def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    global primarySubscription
    topic = getChannelTopic(primarySubscription.streamId, primarySubscription.targetId)
    sendJoinRequest(topic)




def publish_every_n_seconds(n=7):
    while True:
        predictObservation()
        # print(getRandomString(8))
        time.sleep(n)


def getChannelTopic(streamId,targetId):
    topic = "stream:" + str(streamId) + "-" + str(targetId)
    return topic


def getRandomString(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def predictObservation():
    global primarySubscription
    predictionValue = getRandomString(8)
    createAndPublishObservation(primarySubscription, predictionValue)



def createAndPublishObservation(subscription,value):
    # [:wallet_id, :stream_id, :target_id, :value]
    observation = {
      "wallet_id": clientConfiguration.walletId,
      "stream_id": subscription.streamId,
      "target_id": subscription.targetId,
      "value": value
    }

    
    topic = getChannelTopic(subscription.streamId, subscription.targetId)
    publishObservation(topic,observation) 


def publishObservation(topic, observation):
    msg = {
      "topic": topic,
      "event": "published_observation",
      "payload": observation,
      "ref": 0
    }
    ws.send(json.dumps(msg))    


def sendJoinRequest(topic):
    msg = {
      "topic": topic,
      "event": "phx_join",
      "payload": {},
      "ref": 0
    }
    ws.send(json.dumps(msg))


def sendHeartbeat():
    msg = {
      "topic": "phoenix",
      "event": "heartbeat",
      "payload": {},
      "ref": 0
    }
    ws.send(json.dumps(msg))



#singleton
class ClientConfiguration(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(ClientConfiguration, cls).__new__(cls)
            #initialization
             
        return cls._instance
        


class Subscription:
    def __init__(self,streamId, targetId):
        self.streamId = streamId
        self.targetId = targetId    



def getPrimarySubscription(clientConfiguration):
    transport = AIOHTTPTransport(url="http://localhost:4000/api")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql(
        """
        query {
          primarySubscription(walletId: 1122, deviceId: 7788) {
            id
            deviceId
            streamId
            targetId
          }
        }
    """
    )

    result = client.execute(query)
    result = str(result).replace("'", '"')
    print(result)
    resultJson = json.loads(result)
    primary_subscription = resultJson["primarySubscription"]
    streamId = primary_subscription["streamId"]
    targetId = primary_subscription["targetId"]

    global primarySubscription
    primarySubscription = Subscription(streamId, targetId)

    configureWebSocket()


def configureWebSocket():
    websocket.enableTrace(True)
    global ws
    ws = websocket.WebSocketApp("ws://localhost:4000/socket/websocket",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()     



if __name__ == "__main__":
    clientConfiguration = ClientConfiguration()
    clientConfiguration.walletId = 1122
    clientConfiguration.deviceId = 7788
    getPrimarySubscription(clientConfiguration)






   