from screen.game.lobby.base.base import BaseLobbyScreen


class BaseMultiPlayLobbyScreen(BaseLobbyScreen):
    def __init__(self, screen_controller):
        super().__init__(screen_controller)

    def init(self):
        super().init()
        self.init_slot()

    def init_slot(self):
        super().init_slot()
        self.player_slots = []
        for idx in range(5):
            self.player_slots.append({'name': f'Slot{idx}', 'rect': None, 'enabled': False if idx >= 1 else True, 'player': None})

    def draw(self, surface):
        super().draw(surface)