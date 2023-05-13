import eventlet
from eventlet import wsgi
import socketio

from gamesocket.event import SocketEvent


class GameServer:
    def __init__(self):
        self.ip = None
        self.port = None

        self.sio = None
        self.app = None

        self.handlers = None
        self.init_event_handlers()

    def init(self, ip, port):
        self.ip = ip
        self.port = port

        self.sio = socketio.Server()
        self.app = socketio.WSGIApp(self.sio)

        self.init_listeners()

        eventlet.wsgi.server(eventlet.listen((ip, port)), self.app)



    def init_listeners(self):
        @self.sio.on('*')
        def catch_all(event, sid, data):
            print(event, sid, data)

    def init_event_handlers(self):
        self.handlers = {
            SocketEvent.TIME.value: 0
        }

if __name__ == '__main__':
    server = GameServer()
    server.init('127.0.0.1', 8002)
