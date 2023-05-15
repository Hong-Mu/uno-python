import socket
import requests

from gamesocket.server import GameServer
from model.screentype import ScreenType
from screen.game.lobby.base.multiplay import BaseMultiPlayLobbyScreen
from screen.game.lobby.dialog.inputname import InputNameDialog
from screen.game.lobby.dialog.inputpassword import InputPasswordDialog


class HostLobbyScreen(BaseMultiPlayLobbyScreen):
    def __init__(self, screen_controller):
        super().__init__(screen_controller)

        self.server = screen_controller.server

        self.input_password_dialog = InputPasswordDialog(self)
        self.input_name_dialog = InputNameDialog(self)


        self.menus = [
            {'text': '게임 시작', 'view': None, 'rect': None, 'action': lambda: (

            )},
            {'text': '닉네임 설정', 'view': None, 'rect': None, 'action': lambda: (
                self.input_name_dialog.show()
            )},
            {'text': '비밀번호 설정', 'view': None, 'rect': None, 'action': lambda: (
                self.input_password_dialog.show()
            )},
            {'text': '돌아가기', 'view': None, 'rect': None, 'action': lambda: (
                self.screen_controller.set_screen(ScreenType.HOME)
            )},
            {'text': f'외부IP: {self.get_external_ip()}', 'view': None, 'rect': None, 'action': lambda: (

            )},
            {'text': f'내부IP: {self.get_internal_ip()}', 'view': None, 'rect': None, 'action': lambda: (

            )},
        ]



    def init(self):
        super().init()
        self.server.enabled = True

    def on_destroy(self):
        super().on_destroy()
        self.server.enabled = False


    def draw(self, screen):
        super().draw(screen)
        if self.input_password_dialog.enabled:
            self.input_password_dialog.draw(screen)
        elif self.input_name_dialog.enabled:
            self.input_name_dialog.draw(screen)

    def run_key_event(self, event):
        if self.event_enabled:
            super().run_key_event(event)

        elif self.input_password_dialog.enabled:
            self.input_password_dialog.run_key_event(event)
        elif self.input_name_dialog.enabled:
            self.input_name_dialog.run_key_event(event)

    def run_click_event(self, event):
        if self.event_enabled:
            super().run_click_event(event)

        elif self.input_password_dialog.enabled:
            self.input_password_dialog.run_click_event(event)
        elif self.input_name_dialog.enabled:
            self.input_name_dialog.run_click_event(event)

    def get_internal_ip(self):
        internal_ip = socket.gethostbyname(socket.gethostname())
        return internal_ip

    def get_external_ip(self):
        urls = [
            'https://icanhazip.com',
            'https://ipecho.net/plain',
            'https://ipinfo.io/ip'
            'https://checkip.amazonaws.com',
            'https://ifconfig.co/ip',
        ]
        for url in urls:
            try:
                return requests.get(url).text.strip()
            except:
                pass

