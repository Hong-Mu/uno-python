from screen.game.lobby.base.base import BaseLobbyScreen


class BaseMultiPlayLobbyScreen(BaseLobbyScreen):
    def __init__(self, screen_controller):
        super().__init__(screen_controller)

    def init(self):
        super().init()

    def draw(self, surface):
        super().draw(surface)