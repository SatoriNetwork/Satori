''' here's a callback example that seems to have everything we need. '''
import websocket

def on_message(ws, message):
    ''' send message to flask or correct actor '''
    print(message)

def on_error(ws, error):
    ''' send message to flask to re-establish connection '''
    print(error)
    # exit thread

def on_close(ws, close_status_code, close_msg):
    ''' send message to flask to re-establish connection '''
    print("### closed ###")
    # exit thread

def on_open(ws):
    print("Opened connection")
    ws.send('hello')

if __name__ == "__main__":
    websocket.enableTrace(True)
    #ws = websocket.WebSocketApp("wss://api.gemini.com/v1/marketdata/BTCUSD",
    ws = websocket.WebSocketApp('ws://localhost:8000',
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    

    ws.run_forever()