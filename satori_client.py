import websocket
import _thread
import time
import rel
import json


connectAndJoinedToChannel = False

def on_message(ws, message):
    print("RECEIVED_SOCKET_MESSAGE: ", message)

    messageJson = json.loads(message)
    payload = messageJson["payload"]
    global connectAndJoinedToChannel
    if connectAndJoinedToChannel == False:
        if payload["status"] == "ok":
            connectAndJoinedToChannel = True
            createAndPublishObservation("98juoieruerer")


    event = messageJson["event"]
    if event == "published_observation":
        print("PUBLISHED_OBSERVATION: ", payload)





def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    sendJoinRequest("stream:3344-5566")



def createAndPublishObservation(value):
    # [:wallet_id, :stream_id, :target_id, :value]
    streamId = 3344
    targetId = 5566

    observation = {
      "wallet_id": 1122,
      "stream_id": streamId,
      "target_id": targetId,
      "value": value
    }

    # joined channel :  stream:3344-5566
    topic = "stream:" + str(streamId) + "-" + str(targetId)
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





if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:4000/socket/websocket",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()