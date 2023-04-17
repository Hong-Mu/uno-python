from game.model.card import Card
from util.globals import *
import random

class Deck:
    def __init__(self):
        self.cards = []

        self.init_deck()

    def init_deck(self):
        self.create_cards()
        self.shuffle()

    def create_cards(self):
        color = list(CARD_COLOR_SET.keys())
        value = [i for i in range(1,10)] + SKILL_SET
        # value = [SKILL_JUMP_RANDOM] * 5 + [SKILL_REVERSE] * 5 + [SKILL_JUMP] * 5

        # 무색상 +4 기술 카드
        cards=[]
        cards.extend([Card(CARD_COLOR_NONE, SKILL_PLUS_4)])
        # 무색상 색상 기술 카드
        cards.extend([Card(CARD_COLOR_NONE, SKILL_COLOR)])

        for c in color[1:]:
            for v in value[:14]:
                cards.append(Card(c,v))
        self.cards = cards
        
    def shuffle(self):
        random.shuffle(self.cards)

    # 카드 분해 TODO: 범위 체크
    def deal(self, n = 1):
        return [self.draw() for _ in range(n)]

    # 카드 드로우
    def draw(self):
        if len(self.cards) == 0:
            # TODO: 새로 덱을 만들면 정해진 매수를 초과함 -> 이미 제출한 카드를 다시 섞어야 할듯
            self.init_deck()

        return self.cards.pop()