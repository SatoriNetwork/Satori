import json 
from .client import ClientConnection

def establishConnection():
    ''' establishes a connection to the satori server, returns connection object '''
    print(f'establishing a connection...')
    return ClientConnection(
        url='ws://localhost:8000', # mock_server.py
        #url='ws://localhost:4000', # satori server? 
        )

if __name__ == '__main__':
    connection = establishConnection()
    while True:
        connection.send(input('what should the client say to the server? '))