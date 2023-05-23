from base.baseachievementgame import BaseAchievementGame
from base.basegame import BaseGame
from game.model.computer import Computer
from model.achievement import Achievement
from model.region import Region


class GameB(BaseGame):
    def __init__(self):
        super().__init__()
    def init(self):
        super().init()
        cnt = len(self.deck.cards) // len(self.players)
        self.deal(cnt)