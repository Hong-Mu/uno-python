class Player:
    def __init__(self, name, sid=None, is_host=False):
        self.name = name
        self.hands = []
        self.sid = sid
        self.is_host = is_host
    
    def deal(self, cards):
        self.hands = cards

    # 카드를 가져옴
    def draw(self, card):
        self.hands.append(card)

    # 카드를 냄
    def play(self, game, idx):
        return self.hands.pop(idx)
