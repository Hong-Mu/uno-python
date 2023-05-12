from base.basegame import BaseGame
from game.model.computer import Computer
from game.story.region import Region
from util.extradata import ExtraData
from util.globals import extraDataUtil


class GameB(BaseGame):
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
            if extraDataUtil.get(ExtraData.STORY_CLEARED.name) > Region.B.value:
                extraDataUtil.set(ExtraData.STORY_CLEARED.name, Region.B.value)
