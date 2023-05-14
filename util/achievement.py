import time
from enum import Enum
from datetime import datetime

from base.basefileutil import BaseFileUtil
from model.achievement import Achievement
from util.globals import PREF_ACQUIRED, PREF_TIMIESTAMP


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

    def get(self, achievement):
        return self.data.get(achievement.name)

    def set(self, key, value):
        super().set(key.name, value)


if __name__ == '__main__':
    ach = AchievementsUtil()
    print(ach.data)
