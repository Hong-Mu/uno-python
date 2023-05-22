from base.baseachievementgame import BaseAchievementGame
from base.basegame import BaseGame
from game.model.computer import Computer
from model.region import Region
from util.globals import *


class GameD(BaseGame):
    def __init__(self):
        super().__init__()
        self.turn_cnt = 0

    def init(self):
        super().init()
        self.turn_cnt = 0
        computers = [Computer(f"Computer{i}") for i in range(5)]
        self.players.extend(computers)

        self.deck.set_cards(self.get_deck())
        self.deal()

    def set_winner(self, player):
        super().set_winner(player)
        if player == self.get_board_player():
            self.check_story_cleared(Region.D)
            self.update_achievement(Achievement.STORY_D)


    def get_deck(self):
        color = list(CARD_COLOR_SET.keys())
        cards = []
        for c in color[1:]:
            for v in range(1, 10):
                cards.append(Card(c, v))
        return cards