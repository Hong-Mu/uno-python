import random

from base.baseachievementgame import BaseAchievementGame
from base.basegame import BaseGame
from game.model.card import Card
from game.model.computer import Computer
from model.achievement import Achievement
from model.skill import Skill
from model.region import Region
from util.extradata import ExtraData
from util.globals import *


class GameA(BaseGame):
    def __init__(self):
        super().__init__()

    def init(self):
        super().init()
        for c in self.players:
            if c.name.startswith('Computer'):
                self.computer_deal(c, 7)
        self.get_board_player().deal(self.deck.deal(7))

    def computer_deal(self, computer, n):
        example = []
        for _ in range(n):
            card = self.roulette_wheel_selection(self.deck.cards)
            self.deck.cards.remove(card)
            example.append(card)

        computer.deal(example)



    def roulette_wheel_selection(self, cards):
        non_int_values = [card for card in cards if not isinstance(card.value, int)]
        int_values = [card for card in cards if isinstance(card.value, int)]

        sample = [0, 0, 1, 1, 1]
        idx = random.randint(0, len(sample) - 1)

        if sample[idx]:
            return random.choice(non_int_values)
        else:
            return random.choice(int_values)

    def get_combo(self, computer):
        temp = computer.get_special_cards()
        if len(temp) > 0:
            for card in temp:
                computer.hands.remove(card)
            computer.hands.append(Card(CARD_COLOR_NONE, Skill.COMBO.value))
            return len(computer.hands) - 1

