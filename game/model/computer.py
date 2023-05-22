import random
import uuid

from game.model.player import Player
from util.globals import *


class Computer(Player):

    DELAY = 3  # 컴퓨터 선택 딜레이
    UNO_DELAY = 2  # 플레이어가 2초 이내 우노 미클릭시 우노 버튼 클릭

    def __init__(self, name):
        super().__init__(name, uuid.uuid1().hex)

    def to_play(self, game):
        temp = [card for card in self.hands if game.verify_new_card(card)]
        if len(temp) > 0:
            card = random.choice(temp)
        else:
            return None
        return self.hands.index(card)

    def get_special_cards(self):
        special_cards = []
        for card in self.hands:
            if card.value == "skill_reverse":
                if len(special_cards) == 0:
                    special_cards.append(card)
            elif card.value == "skill_card_2":
                if len(special_cards) == 1:
                    special_cards.append(card)
            elif card.value == "skill_jump_random":
                if len(special_cards) == 2:
                    special_cards.append(card)
            if len(special_cards) == 3:
                break
        return special_cards if len(special_cards) == 3 else []