from base.baseachievementgame import BaseAchievementGame
from base.basegame import BaseGame
from game.model.computer import Computer
from model.achievement import Achievement
from model.region import Region


class SingleB(BaseAchievementGame):
    def __init__(self):
        super().__init__()
    def init(self):
        super().init()
        computers = [Computer(f"Computer{i}") for i in range(3)]
        self.players.extend(computers)

        cnt = len(self.deck.cards) // len(self.players)
        self.deal(cnt)

    def set_winner(self, player):
        super().set_winner(player)
        if player == self.get_board_player():
            self.check_story_cleared(Region.B)
            self.update_achievement(Achievement.STORY_B)