# this isn't quite right. this connection object needs to subscribe and publish.
# right now it just listens indefinitely. since the self.ws.recv() is blocking,
# we may need to establish two connections, one for subscribing and one for
# publishing. That would be the simplest solution, puts a burden on the server
# but that's ok for now.


import json
import threading


class SatoriSubConn(object):
    def __init__(
            self, uid: str, payload: dict, url: str = 'ws://localhost:3000',
            router: 'function' = None, listening: bool = True, *args, **kwargs):
        super(SatoriSubConn, self).__init__(*args, **kwargs)
        self.uid = uid
        self.url = url
        self.router = router
        self.ws = self.connect()
        self.listening = listening
        self.ear = threading.Thread(
            target=self.listen, daemon=True)
        self.ear.start()
        self.payload = payload
        self.checkin()

    def listen(self):
        while self.listening == True:
            response = self.ws.recv()
            print(response)
            self.router(response)
        print('not listening')

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


# install latest python3 (>3.7)
# pip3 install websocket-client
# python3 clientws.py
