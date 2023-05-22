import random

from base.basegame import BaseGame
from game.model.computer import Computer


class ClientGame(BaseGame):
    def __init__(self):
        super().__init__()

        self.skip_sids = []

    def get_skipped_player_indexs(self):
        return [idx for idx, p in enumerate(self.players) if p.sid in self.skip_sids]

