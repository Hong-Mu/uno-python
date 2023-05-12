import random

from base.basegame import BaseGame
from game.model.card import Card
from game.model.computer import Computer
from game.model.skill import SKILL
from game.story.region import Region
from util.extradata import ExtraData
from util.globals import extraDataUtil, CARD_COLOR_NONE


class GameA(BaseGame):
    def __init__(self):
        super().__init__()

        self.boss = None

    def init(self):
        super().init()

        self.boss = Computer('Computer0')

        self.players.append(self.boss)
        self.computer_deal(7)

    def set_winner(self, player):
        super().set_winner(player)
        if player == self.get_board_player():
            if extraDataUtil.get(ExtraData.STORY_CLEARED.name) > Region.A.value:
                extraDataUtil.set(ExtraData.STORY_CLEARED.name, Region.A.value)

    def computer_deal(self, n):
        example = []
        for _ in range(n):
            card = self.roulette_wheel_selection(self.deck.cards)
            self.deck.cards.remove(card)
            example.append(card)

        self.boss.deal(example)
        self.get_board_player().deal(self.deck.deal(7))

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
            computer.hands.append(Card(CARD_COLOR_NONE, SKILL.COMBO))
            return len(computer.hands) - 1
