import socketio

from gamesocket.event import SocketEvent


class GameClient:
    def __init__(self):
        self.sio = None
        self.enabled = False
        self.is_running = False

    def connect(self, ip='localhost', port=8003, listener=None):
        try:
            self.sio = socketio.Client()
            self.set_on_message_listener(listener)
            self.sio.connect(f'http://{ip}:{port}')
            print('[Client] connected to server..!')
        except Exception as e:
            raise Exception(e)

    def stop(self):
        self.sio.disconnect()
        self.is_running = False

    def set_on_message_listener(self, listener):
        @self.sio.on('*')
        async def catch_all(event, data):
            print(event, data)
            await listener(event, data)

    def emit(self, event, data):
        print(f'[Client] [Emit]{event} : {data}')
        self.sio.emit(event, data)


if __name__ == '__main__':
    client = GameClient()
    try:
        client.connect('localhost', 8003, lambda e, d: (
            print('Listener', e, d)
        ))
        client.emit(SocketEvent.TIME, {'hi': ''})
    except Exception as e:
        print(e)


