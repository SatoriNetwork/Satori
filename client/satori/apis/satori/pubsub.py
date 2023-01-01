# this uses the websocket-client library and represents a both the subscriber
# and the publisher connection in one. It runs the subscriber in it's own thread
# which means the only downside it has is that it cannot change the on_message
# handler, called router, until after a message has been received. This is a
# limitation, but not a serious one.

# the default router should accept the message and hold it in memory until the
# ipfs sync process is complete. Once it is complete it should send each message
# in reserve to the system that saves it to disk and routes it to the engine.
# since the engine will not even be started until after the router is complete,
# and all messages saved to the disk, this should be fine.

import json
import threading


class SatoriPubSubConn(object):
    def __init__(
            self, uid: str, payload: dict, url: str = 'ws://localhost:3000',
            router: 'function' = None, listening: bool = True, *args, **kwargs):
        super(SatoriPubSubConn, self).__init__(*args, **kwargs)
        self.uid = uid
        self.url = url
        self.router = router
        self.ws = self.connect()
        self.listening = listening
        self.ear = threading.Thread(target=self.listen, daemon=True)
        self.ear.start()
        self.payload = payload
        self.checkin()

    def listen(self):
        while True:
            response = self.ws.recv()
            print(response)
            self.router(response)

    def connect(self):
        import websocket
        ws = websocket.WebSocket()
        ws.connect(f'{self.url}?uid={self.uid}')
        assert (ws.connected == True)
        return ws

    def checkin(self):
        self.ws.send('key:' + self.payload)

    def publish(self, topic, data):
        self.ws.send('publish:' + json.dumps({'topic': topic, 'data': data}))

    def notify(self, topic, data):
        self.ws.send('notice:' + json.dumps({'topic': topic, 'data': data}))

    def disconnect(self):
        self.listening = False
        self.notify(topic='connection', data=False)
        self.ws.close()  # server should detect we closed the connection
        assert (self.ws.connected == False)

    def setRouter(self, router: 'function' = None):
        self.router = router

# install latest python3 (>3.7)
# pip3 install websocket-client
# python3 clientws.py
