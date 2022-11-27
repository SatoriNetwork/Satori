import json
from satoriserver.utils import Crypt
import threading


class SatoriPubsubConn(object):
    def __init__(
            self, uid: str, payload: dict, url: str = 'ws://localhost:3000',
            router: function = None, listening: bool = True, *args, **kwargs):
        super(SatoriPubsubConn, self).__init__(*args, **kwargs)
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
        self.ws.send('key:' +
                     Crypt().encrypt(
                         toEncrypt=json.dumps(self.payload),
                         key='thiskeyisfromenv'))

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


#import json
#import time
#from satori.utils import Crypt
#from satori.apis.server.pubsub import SatoriPubsubConn
#
#
# def router(response: str):
#    ''' processes reponse, routes data to the right stream; triggers engine '''
#    pass
#
#
# def run():
#    wait = 30
#    conn = SatoriPubsubConn(
#        uid='pubkey-a',
#        router=router,
#        payload={
#            'publisher': ['stream-a'],
#            'subscriptions': ['stream-b', 'stream-c', 'stream-d']})
#    while True:
#        time.sleep(wait)
#        conn.publish(topic='stream-a', data='data for stream-a')
#        time.sleep(wait)
#    conn.disconnect()
#
#
# run()
