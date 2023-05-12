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
    SINGLE_WIN_CNT = "single_win_cnt"
    SINGLE_UNO_CNT = "single_uno_cnt"
    STORY_CLEARED = "story_cleared"
