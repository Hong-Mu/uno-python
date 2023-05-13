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


class ExtraData(Enum):
    SINGLE_WIN_CNT = 0
    SINGLE_UNO_CNT = 1
    STORY_CLEARED = 2
