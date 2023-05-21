import random

from base.baseachievementgame import BaseAchievementGame
from base.basegame import BaseGame
from util.extradata import ExtraData
from util.globals import *


class SinglePlayGame(BaseAchievementGame):
    def __init__(self):
        super().__init__()

    def init(self):
        super().init()
        self.deal()

    def set_winner(self, player):
        super().set_winner(player)

    def run_periodically(self):
        super().run_periodically()

        self.check_uno_count()

