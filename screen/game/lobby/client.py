from game.model.player import dict_to_player
from game.multi.client_game import ClientGame
from game.multi.multi import MultiPlayGame
from game_socket.socketevent import SocketEvent
from model.screentype import ScreenType
import ast
from screen.game.lobby.base.multiplay import BaseMultiPlayLobbyScreen
from screen.game.lobby.dialog.inputname import InputNameDialog


class ClientLobbyScreen(BaseMultiPlayLobbyScreen):
    def __init__(self, screen_controller):
        super().__init__(screen_controller)

        self.client = screen_controller.client

        self.input_name_dialog = InputNameDialog(self, on_confirm=lambda: (
            self.send_name_refresh(),
            self.input_name_dialog.dismiss()
        ))

        self.menus = [
            {'text': '닉네임 설정', 'view': None, 'rect': None, 'action': lambda: (
                self.input_name_dialog.show(),
            )},
            {'text': '돌아가기', 'view': None, 'rect': None, 'action': lambda: (
                self.client.disable(),
                self.screen_controller.set_screen(ScreenType.HOME)
            )},
        ]
        
    def init(self):
        super().init()

        self.client.emit(SocketEvent.SLOT, {'type': 'request'})

    def on_destroy(self):
        super().on_destroy()
        print('ClientLobbyScreen: onDestroy')



    def draw(self, screen):
        super().draw(screen)

        if self.input_name_dialog.enabled:
            self.input_name_dialog.draw(screen)


    def run_key_event(self, event):
        if self.event_enabled:
            super().run_key_event(event)

        elif self.input_name_dialog.enabled:
            self.input_name_dialog.run_key_event(event)

    def run_click_event(self, event):
        if self.event_enabled:
            super().run_click_event(event)

        elif self.input_name_dialog.enabled:
            self.input_name_dialog.run_click_event(event)

    def on_server_disconnected(self):
        self.client.disable()
        self.screen_controller.set_screen(ScreenType.HOME)

    def toggle_player_enabled(self, idx): # 선택 비활성화
        pass

    def send_name_refresh(self):
        self.client.emit(SocketEvent.NAME, {'name': self.input_name_dialog.input})

    def on_server_message(self, event, data):
        if event == SocketEvent.SLOT:
            self.handle_slot_event(data)
        elif event == SocketEvent.START:
            self.play([dict_to_player(p) for p in data])

    def handle_slot_event(self, data):
        data = ast.literal_eval(data)

        for idx, slot in enumerate(self.player_slots):
            player = data[idx]

            slot['name'] = player['name']
            slot['enabled'] = player['enabled']

            if player['sid'] == self.client.my_socket_id:
                slot['name'] = player['host']
                self.input_name_dialog.input = player['name']


    def play(self, players):
        players = self.rotate_list_to_id(players, self.client.my_socket_id)

        self.screen_controller.set_game(ClientGame())
        self.screen_controller.game.set_players(players)
        self.screen_controller.game.start_game()
        self.screen_controller.set_screen(ScreenType.PLAY_CLIENT)

    def rotate_list_to_id(self, players, target_id):
        index = next((i for i, player in enumerate(players) if player.sid == target_id), -1)
        rotated_lst = players[index:] + players[:index]
        return rotated_lst