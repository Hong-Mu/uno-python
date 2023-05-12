import json
import os

import pygame

from util.base import BaseFileUtil
from util.globals import *


class SettingsUtil(BaseFileUtil):
    MAX_VOLUME = 10

    def __init__(self):
        super().__init__()
        self.FILE_PATH = 'uno_setting.json'
        self.data = None
        self.load()

        # 화면
        self.screen_resolution = [(600, 400), (720, 480), (960, 640)]

    def init(self):
        self.data = {
            MODE_SCREEN: 1,
            MODE_BLIND: 0,
            MODE_MASTER_VOLUME: 4,
            MODE_BACKGROUND_VOLUME: 4,
            MODE_EFFECT_VOLUME: 4,
            MODE_UNO_KEY: pygame.K_u,
            MODE_DECK_KEY: pygame.K_d,
        }

    def get_resolution(self):
        return self.screen_resolution[self.get(MODE_SCREEN)]

    def get_background_volume(self):
        return self.get(MODE_BACKGROUND_VOLUME) * self.get(MODE_MASTER_VOLUME) / 100

    def get_effect_volume(self):
        return self.get(MODE_EFFECT_VOLUME) * self.get(MODE_MASTER_VOLUME) / 100


if __name__ == '__main__':
    setting = SettingsUtil()
    print(setting.get_resolution())
    print(setting.get_effect_volume())
    print(setting.get(MODE_MASTER_VOLUME))
