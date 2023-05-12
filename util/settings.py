import json
import os

import pygame

from util.globals import *


class SettingsUtil:
    file_path = 'uno_setting.json'

    MAX_VOLUME = 10

    def __init__(self):

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

    def clear(self):
        self.init()
        self.save()

    def get_resolution(self):
        return self.screen_resolution[self.get(MODE_SCREEN)]

    def get_background_volume(self):
        return self.get(MODE_BACKGROUND_VOLUME) * self.get(MODE_MASTER_VOLUME) / 100

    def get_effect_volume(self):
        return self.get(MODE_EFFECT_VOLUME) * self.get(MODE_MASTER_VOLUME) / 100

    # 파일 저장 관련 코드
    def get(self, key):
        self.load()
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def save(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def load(self):
        try:
            with open(self.file_path, 'r') as f:
                self.data = json.load(f)
        except IOError:
            self.clear()


if __name__ == '__main__':
    setting = SettingsUtil()
    print(setting.get_resolution())
    print(setting.get_effect_volume())
    print(setting.get(MODE_MASTER_VOLUME))
