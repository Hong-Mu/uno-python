import asyncio
import json

from game.model.card import Card
from game.model.player import Player

if __name__ == '__main__':
    p1 = Player('name', 'sdfsdf')
    p1.hands = [vars(Card('213', 124))]
    temp = [vars(p1) for _ in range(10)]
    print(temp)
