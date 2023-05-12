from base.basegame import BaseGame
from game.model.card import Card
from game.model.computer import Computer
from game.story.region import Region
from util.extradata import ExtraData
from util.globals import extraDataUtil, CARD_COLOR_SET


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
            if extraDataUtil.get(ExtraData.STORY_CLEARED.name) > Region.D.value:
                extraDataUtil.set(ExtraData.STORY_CLEARED.name, Region.D.value)


    def get_deck(self):
        color = list(CARD_COLOR_SET.keys())
        cards = []
        for c in color[1:]:
            for v in range(1, 10):
                cards.append(Card(c, v))
        return cards