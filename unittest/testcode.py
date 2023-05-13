import random
import unittest

from game.game import UnoGame
from game.model.card import Card
from game.story.regionA import RegionA

class RegionATest(unittest.TestCase):
    def test_percent(self):
        game = UnoGame()
        game.start_game("", [])
        game.deck.shuffle()

        region = RegionA(game)

        skill_cnt = 0
        num_cnt = 0
        for i in range(1000):
            if not isinstance(region.roulette_wheel_selection(game.deck.cards).value, int):
                skill_cnt += 1
            else:
                num_cnt += 1

        skill_ratio = skill_cnt / 1000
        print(skill_ratio)
        error = abs(skill_ratio - 0.6) / 0.6
        print(f'오차: {error}')
        print(f'테스트 통과 여부: {error <= 0.05}')

        print(skill_cnt, num_cnt)
        self.assertTrue(error <= 0.5)

if __name__ == '__main__':
    # pyinstaller main.py --onefile --noconsole
    unittest.main()