import asyncio

import socketio

from game_socket.event import SocketEvent


class GameClient:
    def __init__(self):
        self.sio = socketio.Client()
        self.client_task = None
        self.enabled = False
        self.is_running = False


    def start(self, ip='localhost', port=8003, listener=None):
        print('[Client] Started..!')
        self.is_running = True
        self.client_task = asyncio.create_task(self.run(ip, port, listener))

    def stop(self):
        print('[Client] Canceled..!')
        self.is_running = False
        self.sio.disconnect()

    async def run(self, ip='localhost', port=8003, listener=None):
        try:
            self.set_on_message_listener(listener)
            self.sio.connect(f'http://{ip}:{port}')
            # await self.sio.wait()
        except Exception as e:
            print(f'[Client] Run: {e}')

    def set_on_disconnect_listener(self, listener):
        @self.sio.event
        def disconnect():
            print('[Client] connected!')
            listener()

    def set_on_message_listener(self, listener):
        print(listener)

        @self.sio.event
        def connect():
            print('[Client] connected!')
            self.emit(SocketEvent.JOIN, {})



        @self.sio.on('*')
        def catch_all(event, data):
            print(event, data, 'sdfsdf')
            listener(event, data)

    def emit(self, event, data):
        print(f'[Client] [Emit]{event} : {data}')
        self.sio.emit(event, data)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False


if __name__ == '__main__':
    client = GameClient()
    try:
        client.run('localhost', 8003, lambda e, d: (
            print('Listener', e, d)
        ))
        client.emit(SocketEvent.TIME, {'hi': ''})
    except Exception as e:
        print(e)


