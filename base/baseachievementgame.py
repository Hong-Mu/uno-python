import random

from base.basegame import BaseGame
from util.extradata import ExtraData
from util.globals import *


class BaseAchievementGame(BaseGame):
    def __init__(self):
        super().__init__()

    def set_winner(self, player):
        super().set_winner(player)
        if player == self.get_board_player():
            self.update_win_count()
            self.check_win_count()
            self.check_computer_uno_clicked_when_win()
        else:
            self.check_player_uno_clicked_when_lose()

    def run_periodically(self):
        super().run_periodically()
        self.check_uno_count()

