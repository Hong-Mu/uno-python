import random

from base.basegame import BaseGame
from game.model.computer import Computer


class MultiPlayGame(BaseGame):
    def __init__(self):
        super().__init__()

        self.boss = None

    def init(self):
        super().init()
        self.deal(3)
