from model.screentype import ScreenType
from screen.game.lobby.base.multiplay import BaseMultiPlayLobbyScreen
from screen.game.lobby.dialog.inputname import InputNameDialog


class ClientLobbyScreen(BaseMultiPlayLobbyScreen):
    def __init__(self, screen_controller):
        super().__init__(screen_controller)

        self.client = screen_controller.client

        self.input_name_dialog = InputNameDialog(self)

        self.menus = [
            {'text': '닉네임 설정', 'view': None, 'rect': None, 'action': lambda: (
                self.input_name_dialog.show()
            )},
            {'text': '돌아가기', 'view': None, 'rect': None, 'action': lambda: (
                self.screen_controller.set_screen(ScreenType.HOME)
            )},
        ]
        
    def init(self):
        super().init()

    def on_destroy(self):
        super().on_destroy()
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