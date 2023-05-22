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
                self.screen_controller.set_screen(ScreenType.HOME)
            )},
        ]
        
    def init(self):
        super().init()

        self.client.emit(SocketEvent.SLOT, {'type': 'request'})

    def on_destroy(self):
        super().on_destroy()
        print('ClientLobbyScreen: onDestroy')
        self.client.disable()


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
        self.screen_controller.set_screen(ScreenType.HOME)

    def toggle_player_enabled(self, idx): # 선택 비활성화
        pass

    def send_name_refresh(self):
        self.client.emit(SocketEvent.NAME, {'name': self.input_name_dialog.input})

    def on_server_message(self, event, data):
        if event == SocketEvent.SLOT:
            data = ast.literal_eval(data)
            for idx, slot in enumerate(self.player_slots):
                slot['name'] = data[idx]['name'] if idx != 0 else data[idx]['host']
                slot['enabled'] = data[idx]['enabled']

                if data[idx]['sid'] == self.client.my_socket_id:
                    self.input_name_dialog.input = data[idx]['name']

