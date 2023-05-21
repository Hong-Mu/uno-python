import socket
import requests

from game.model.player import Player
from game_socket.event import SocketEvent
from game_socket.server import GameServer
from model.screentype import ScreenType
from screen.game.lobby.base.multiplay import BaseMultiPlayLobbyScreen
from screen.game.lobby.dialog.inputname import InputNameDialog
from screen.game.lobby.dialog.inputpassword import InputPasswordDialog


class HostLobbyScreen(BaseMultiPlayLobbyScreen):
    def __init__(self, screen_controller):
        super().__init__(screen_controller)

        self.server = screen_controller.server

        self.input_password_dialog = InputPasswordDialog(self)
        self.input_name_dialog = InputNameDialog(self, on_confirm=lambda : (
            self.send_slot_and_palyers(None),
            self.input_name_dialog.dismiss()
        ))

        self.client_players = []

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
        self.client_players = []
        self.init_slot()

    def on_destroy(self):
        super().on_destroy()
        for player in self.client_players:
            self.server.disconnect(player.sid)
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

    def on_client_disconnected(self, sid):
        for idx, player in enumerate(self.client_players):
            if player.sid == sid:
                self.client_players.pop(idx)
                self.player_slots[idx]['name'] = f'Slot{idx}'

    def on_client_message(self, event, sid, data):
        if event == SocketEvent.JOIN:
            self.handle_join_event(sid, data)
        elif event == SocketEvent.AUTH:
            self.handle_auth_event(sid, data)
        elif event == SocketEvent.SLOT:
            self.handle_slot_event(sid, data)
        elif event == SocketEvent.NAME:
            self.handle_name_event(sid, data)

    def handle_join_event(self, sid, data):
        if len(self.input_password_dialog.input.strip()) == 0:
            self.add_player(sid)
        else:
            self.server.emit(SocketEvent.AUTH, sid, {'type': 'request'})

    def add_player(self, sid):
        slot_available = False
        for idx, slot in enumerate(self.player_slots):
            if slot['enabled'] and slot['name'].startswith('Slot'):
                slot_available = True
                player = Player(name=f'Player{idx + 1}', sid=sid)
                self.client_players.append(player)
                self.player_slots[idx]['name'] = player.name
                self.player_slots[idx]['player'] = player
                print('플레이어 추가 완료!', player.name, len(self.client_players))
                self.server.emit(SocketEvent.JOIN, sid, {'result': True})
                break
        if not slot_available:
            self.server.emit(SocketEvent.JOIN, sid, {'result': False, 'message': '접속 가능한 슬롯이 없습니다.'})

    def handle_auth_event(self, sid, data):
        if self.input_password_dialog.input == data['password']:
            self.add_player(sid)
        else:
            self.server.emit(SocketEvent.AUTH, sid, {'result': False, 'message': '비밀번호가 일치하지 않습니다.' })

    def toggle_player_enabled(self, idx):
        super().toggle_player_enabled(idx)
        self.send_slot_and_palyers(None)

    def handle_slot_event(self, sid, data):
        self.send_slot_and_palyers(sid)
    def send_slot_and_palyers(self, sent_sid):
        temp = []
        for idx, slot in enumerate(self.player_slots):
            temp.append({
                'name': slot['name'],
                'rect': None,
                'enabled':  slot['enabled'],
                'host': self.input_name_dialog.input
            })

            if 'player' in slot:
                if slot['player'].sid == sent_sid:
                    self.server.emit(SocketEvent.NAME, sent_sid, data=slot['player'].name)

        self.server.emit(SocketEvent.SLOT, data=str(temp))



    def handle_name_event(self, sid, data):
        for idx, slot in enumerate(self.player_slots):
            if 'player' in self.player_slots[idx]:
                player = self.player_slots[idx]['player']
                if player.sid == sid:
                    player.name = data['name']
                    self.player_slots[idx]['name'] = player.name

        self.send_slot_and_palyers(sid)
