from model.screentype import ScreenType
from screen.game.lobby.base.base import BaseLobbyScreen



class LobbyScreen(BaseLobbyScreen):
    def __init__(self, screen_controller):
        super().__init__(screen_controller)

        self.menus = [
            {'text': '플레이', 'view': None, 'rect': None, 'action': self.toggle_input_name_dialog},
            {'text': '돌아가기', 'view': None, 'rect': None, 'action': lambda: (
                self.screen_controller.set_screen(ScreenType.HOME)
            )},
        ]

    def init(self):
        super().init()

    def draw(self, surface):
        super().draw(surface)

