import random

from base.basegame import BaseGame
from game.model.computer import Computer
from model.region import Region
from util.globals import *


class GameC(BaseGame):
    def __init__(self):
        super().__init__()


    def init(self):
        super().init()
        computers = [Computer(f"Computer{i}") for i in range(2)]
        self.players.extend(computers)
        self.deal()

    def set_winner(self, player):
        super().set_winner(player)
        if player == self.get_board_player():
            self.check_story_cleared(Region.C)
            self.update_achievement(Achievement.STORY_C)

            self.update_win_count()
            self.check_win_count()

    def run_in_turn_start(self):
        super().run_in_turn_start()

        if self.turn_counter % 5 == 0:
            self.current_color = random.choice(list(COLOR_SET.keys()))
