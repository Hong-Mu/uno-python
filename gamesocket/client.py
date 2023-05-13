import socketio

from gamesocket.event import SocketEvent


class GameClient:
    def __init__(self):
        self.ip = None
        self.port = None

        self.sio = None
        self.app = None

        self.handlers = None

    def init(self, ip, port):
        self.ip = ip
        self.port = port

        self.sio = socketio.Client()

        self.sio.connect(f'http://{ip}:{port}')

        for event in SocketEvent:
            self.sio.on(event.value, self.event_handler)

    def event_handler(self, sid, data):
        print(sid)
        print(data)

    def emit(self, event, data):
        print(f'[Client] {event.value} : {data}')
        self.sio.emit(event.value, data)


if __name__ == '__main__':
    client = GameClient()
    client.init('127.0.0.1', 8002)

    client.emit(SocketEvent.TIME, {'hi': ''})
