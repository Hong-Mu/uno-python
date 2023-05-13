import time

import pygame

from model.achievement import Achievement
from util.globals import *
from util.text import wrap_text

ITEM_WIDTH = 70
ITEM_HEIGHT = 70

class AchievementDialog:
    def __init__(self, parent):
        # 의존성 객체
        self.parent = parent
        self.screen_controller = parent.screen_controller

        # 다이얼로그 관련 객체
        self.enabled = True
        self.width = 200
        self.height = 70

        self.achievement = Achievement.SINGLE_WIN_NO_SKILL

        self.display_time = 5
        self.start_time = float('inf')

        self.surface = None
        self.icon_rect = None


    def draw(self, screen):
        self.update_time()
        self.draw_surface(screen)


    def draw_surface(self, screen):
        self.surface = pygame.Surface(size=(self.width, self.height))
        self.surface.fill(COLOR_WHITE)

        self.draw_icon(self.surface)
        self.draw_title(self.surface)
        screen.blit(self.surface, (0, get_small_margin()))

    def draw_icon(self, surface):
        file_name = self.achievement.value
        resource = f'resource\\achievement\\{file_name}.png'
        item = pygame.image.load(os.path.join(ROOT, resource))
        item = pygame.transform.scale(item, (ITEM_WIDTH, ITEM_HEIGHT))
        self.icon_rect = surface.blit(item, (0, 0))

    def draw_title(self, surface):
        temp_y = 0
        for line in wrap_text(ACHIEVE_INFO[self.achievement][KEY_NAME], get_small_font(), self.surface.get_width() - ITEM_WIDTH - get_small_margin()):
            title = get_small_font().render(line, True, COLOR_BLACK)
            surface.blit(title, (ITEM_WIDTH + get_small_margin(), temp_y))
            temp_y += title.get_height()

    def show(self, achievement):
        self.achievement = achievement
        self.start_time = time.time()
        self.enabled = True

    def update_time(self):
        if time.time() - self.start_time >= self.display_time:
            self.enabled = False

    def run_key_event(self, event):
        pass

    def run_click_event(self, event):
        pass