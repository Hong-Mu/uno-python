import copy

from game.model.card import Card


class Player:
    def __init__(self, name, sid=None):
        self.name = name
        self.hands = []
        self.sid = sid
    
    def deal(self, cards):
        self.hands = cards

    # 카드를 가져옴
    def draw(self, card):
        self.hands.append(card)

    # 카드를 냄
    def play(self, game, idx):
        return self.hands.pop(idx)

def player_to_dict(player):
    player_dict = copy.copy(vars(player))
    player_dict["hands"] = [copy.copy(vars(card)) for card in player.hands]
    return player_dict


def dict_to_player(player_dict):
    name = player_dict.get("name")
    sid = player_dict.get("sid")

    player = Player(name, sid)

    hands = player_dict.get("hands", [])
    for card_dict in hands:
        color = card_dict.get("color")
        value = card_dict.get("value")
        card = Card(color, value)
        player.hands.append(card)

    return player
