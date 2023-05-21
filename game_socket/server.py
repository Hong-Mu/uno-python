import asyncio

import pygame
import socketio
from aiohttp import web

from game_socket.socketevent import SocketEvent
from util.globals import COLOR_WHITE


class Pygame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))

        self.server = GameServer()
        self.running = True

    async def run(self):
        cnt = 0
        while self.running:
            cnt += 1
            self.screen.fill(COLOR_WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if cnt == 5:
                self.server.enabled = True

            pygame.display.update()
            self.update_socket()
        pygame.quit()

    def update_socket(self):
        if self.server.enabled:
            if not self.server.is_running:
                self.server.start()
        else:
            if self.server.is_running:
                self.server.stop()



class GameServer:
    def __init__(self):
        self.sio = socketio.AsyncServer()
        self.site = None
        self.runner = None
        self.server_task = None

        self.enabled = False
        self.is_running = False

    def start(self, ip='localhost', port=8003, listener=None):
        print('[Server] start')
        self.is_running = True
        self.server_task = asyncio.create_task(self.run(ip, port, listener))

    def stop(self):
        print('[Server] stop')
        self.is_running = False
        asyncio.create_task(self.site.stop())

    def disconnect(self, sid):
        asyncio.create_task(self.sio.disconnect(sid))

    async def run(self, ip, port, listener):
        self.set_on_message_listener(listener)

        app = web.Application()
        self.sio.attach(app)

        self.runner = web.AppRunner(app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, host=ip, port=port)
        await self.site.start()

    def set_on_message_listener(self, listener):
        @self.sio.on('*')
        async def catch_all(event, sid, data):
            print(event, sid, data)
            await listener(event, sid, data)

    def set_on_connect_listener(self, listener):

        @self.sio.event
        def connect(sid, environ, auth):
            print(f'[Event] {sid} connected!')


    def set_on_disconnect_listener(self, listener):
        @self.sio.event
        def disconnect(sid):
            print(f'[Event] {sid} disconnected!')
            listener(sid)

    async def post(self, event, sid, data):
        await self.sio.emit(event, data, sid)

    def emit(self, event, sid=None, data= None):
        print('[Emit]', event, sid, data)
        asyncio.create_task(self.post(event, sid, data))




async def main():
    game = Pygame()
    pygame_task = asyncio.create_task(game.run())

    await asyncio.gather(pygame_task)


if __name__ == '__main__':
    asyncio.run(main())




