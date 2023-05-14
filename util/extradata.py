from enum import Enum

from base.basefileutil import BaseFileUtil


class ExtraDataUtil(BaseFileUtil):
    def __init__(self):
        super().__init__()
        self.FILE_PATH = 'extradata.json'
        self.load()

    def init(self):
        self.data = {}
        for item in ExtraData:
            self.data[item.name] = 0

    def get(self, extra_data):
        return self.data.get(extra_data.name)

    def set(self, key, value):
        super().set(key.name, value)

    def increase(self, key):
        self.set(key, self.get(key) + 1)


class ExtraData(Enum):
    SINGLE_WIN_CNT = 0
    SINGLE_UNO_CNT = 1
    STORY_CLEARED = 2
