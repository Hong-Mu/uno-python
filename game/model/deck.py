from game.model.card import Card
from game.model.skill import SKILL
from util.globals import *
import random

class Deck:
    def __init__(self, game):
        self.game = game
        self.cards = []

        self.init_deck()

    def init_deck(self):
        self.create_cards()
        self.shuffle()

    def create_cards(self):
        color = list(CARD_COLOR_SET.keys())
        value = [i for i in range(1,10)] + [item.value for item in SKILL]

        # 무색상 +4 기술 카드
        cards = []
        cards.extend([Card(CARD_COLOR_NONE, SKILL.PLUS_4.value)])
        # 무색상 색상 기술 카드
        cards.extend([Card(CARD_COLOR_NONE, SKILL.COLOR.value)])

        for c in color[1:]:
            for v in value[:14]:
                cards.append(Card(c,v))

        self.cards = cards

    def set_cards(self, cards):
        self.cards = cards

        
    def shuffle(self):
        random.shuffle(self.cards)

    # 카드 분배
    def deal(self, n = 1):
        return [self.draw() for _ in range(n)]

    # 카드 드로우
    def draw(self):
        if len(self.cards) == 0:
            # TODO: 새로 덱을 만들면 정해진 매수를 초과함 -> 이미 제출한 카드를 다시 섞어야 할듯
            self.init_deck()

        return self.cards.pop()