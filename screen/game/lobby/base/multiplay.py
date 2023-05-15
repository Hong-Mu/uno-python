from screen.game.lobby.base.base import BaseLobbyScreen


class BaseMultiPlayLobbyScreen(BaseLobbyScreen):
    def __init__(self, screen_controller):
        super().__init__(screen_controller)

    def init(self):
        super().init()

    def init_slot(self):
        super().init_slot()
        for idx in range(5):
            self.player_slots.append({'name': f'Slot{idx}', 'rect': None, 'enabled': False if idx >= 1 else True})

    def draw(self, surface):
        super().draw(surface)