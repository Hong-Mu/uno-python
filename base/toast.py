import time

import pygame

from model.achievement import Achievement
from util.extradata import ExtraData
from util.globals import *
from util.singletone import achievementsUtil, extraDataUtil
from util.text import wrap_text

ITEM_WIDTH = 65
ITEM_HEIGHT = 65


class Toast:
    def __init__(self, parent):
        # 의존성 객체
        self.parent = parent
        self.screen_controller = parent.screen_controller

        # 다이얼로그 관련 객체
        self.enabled = False
        self.width = 500
        self.height = 50

        self.display_time = 2
        self.start_time = None

        self.text = ''


    def draw(self, screen):
        self.update_time()
        surface = pygame.Surface(size=(self.width, self.height))
        surface.fill(COLOR_WHITE)

        self.draw_background(surface)
        self.draw_text(surface)

        ratio_y = (time.time() - self.start_time) / self.display_time * 10

        ratio_y = ratio_y if ratio_y < 1 else 1

        screen.blit(surface, surface.get_rect(midbottom=(screen.get_width() // 2, screen.get_height() - (ratio_y - 1) * self.height)))

    def draw_background(self, surface):
        background = pygame.draw.rect(surface, COLOR_BLACK, surface.get_rect(), 2)
    def draw_text(self, surface):
        title = get_small_font().render(self.text, True, COLOR_BLACK)
        surface.blit(title, title.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2)))

    def show(self, text):
        self.text = text
        self.start_time = time.time()
        self.enabled = True

    def update_time(self):
        if time.time() - self.start_time >= self.display_time:
            self.enabled = False

    def run_key_event(self, event):
        pass

    def run_click_event(self, event):
        pass
