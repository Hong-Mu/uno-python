from game.model.computer import Computer
from game.model.player import Player
from game.single import SinglePlayGame
from model.screentype import ScreenType
from screen.game.lobby.base.base import BaseLobbyScreen
from screen.game.lobby.dialog.inputname import InputNameDialog


class LobbyScreen(BaseLobbyScreen):
    def __init__(self, screen_controller):
        super().__init__(screen_controller)

        self.input_name_dialog = InputNameDialog(self, self.play)

        self.menus = [
            {'text': '플레이', 'view': None, 'rect': None, 'action': lambda: (
                self.input_name_dialog.show(),
            )},
            {'text': '스토리 모드 설정', 'view': None, 'rect': None, 'action': lambda: (

            )},
            {'text': '돌아가기', 'view': None, 'rect': None, 'action': lambda: (
                self.screen_controller.set_screen(ScreenType.HOME)
            )},
        ]

    def init(self):
        super().init()

    def init_slot(self):
        super().init_slot()
        for idx in range(5):
            self.player_slots.append({'name': f'Computer{idx}', 'rect': None, 'enabled': False if idx >= 1 else True})

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

    def play(self):
        players = [Player(self.input_name_dialog.input)]

        for idx, computer in enumerate(self.player_slots):
            if computer['enabled']:
                players.append(Computer(computer['name']))

        self.screen_controller.set_game(SinglePlayGame())
        self.screen_controller.game.set_players(players)
        self.screen_controller.game.start_game()
        self.screen_controller.set_screen(ScreenType.PLAY)

