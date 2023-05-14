import random

from base.basegame import BaseGame
from util.extradata import ExtraData
from util.globals import *


class SinglePlayGame(BaseGame):
    def __init__(self):
        super().__init__()

    def init(self):
        super().init()
        self.deal()

    def set_winner(self, player):
        super().set_winner(player)
        if player == self.get_board_player():
            self.update_win_count()
            self.check_win_count()

    def run_periodically(self):
        super().run_periodically()

        self.check_uno_count()

