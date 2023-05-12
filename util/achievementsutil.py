import json
import time
from enum import Enum
from datetime import datetime

from util.base import BaseFileUtil

PREF_ACQUIRED = "acquired"
PREF_TIMIESTAMP = "timestamp"


class AchievementsUtil(BaseFileUtil):
    def __init__(self):
        super().__init__()
        self.FILE_PATH = 'achievements.json'
        self.load()

    def init(self):
        self.data = {}
        for item in Achivement:
            self.data[item.name] = {PREF_ACQUIRED: False, PREF_TIMIESTAMP: None}

    def set_acquired(self, achivement):
        self.data[achivement.name][PREF_ACQUIRED] = True
        self.data[achivement.name][PREF_TIMIESTAMP] = str(datetime.fromtimestamp(time.time()))
        self.save()
        self.load()


class Achivement(Enum):
    SINGLE_WIN_1 = "single_win_1"
    SINGLE_WIN_10 = "single_win_10"
    SINGLE_WIN_IN_10_TURN = "single_win_in_10_turn"
    SINGLE_WIN_NO_SKILL = "single_win_no_skill"
    SINGLE_WIN_UNO = "single_win_uno"
    SINGLE_LOSE_UNO = "single_lose_uno"
    SINGLE_UNO_CNT = "single_uno_cnt"
    STORY_A = "story_a"
    STORY_B = "story_b"
    STORY_C = "story_c"
    STORY_D = "story_d"


if __name__ == '__main__':
    ach = AchievementsUtil()
    print(ach.data)
