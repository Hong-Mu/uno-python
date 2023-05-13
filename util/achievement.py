import time
from enum import Enum
from datetime import datetime

from base.basefileutil import BaseFileUtil
from model.achievement import Achievement

PREF_ACQUIRED = "acquired"
PREF_TIMIESTAMP = "timestamp"


class AchievementsUtil(BaseFileUtil):
    def __init__(self):
        super().__init__()
        self.FILE_PATH = 'achievements.json'
        self.load()

    def init(self):
        self.data = {}
        for item in Achievement:
            self.data[item.name] = {PREF_ACQUIRED: False, PREF_TIMIESTAMP: None}

    def set_acquired(self, achievement):
        self.data[achievement.name][PREF_ACQUIRED] = True
        self.data[achievement.name][PREF_TIMIESTAMP] = str(datetime.fromtimestamp(time.time()))
        self.save()
        self.load()


if __name__ == '__main__':
    ach = AchievementsUtil()
    print(ach.data)
