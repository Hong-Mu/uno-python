from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from screen.model.screentype import ScreenType
from util.globals import *

if TYPE_CHECKING:
    from screen.game.play.PlayScreen import PlayScreen


class GameOverDialog:
    def __init__(self, play_screen: PlayScreen):
        # 의존성 객체
        self.play_screen = play_screen
        self.screen_controller = play_screen.screen_controller

        # 다이얼로그 관련 객체
        self.enabled = False
        self.width = 500
        self.height = 300

    def draw(self, screen: pygame.Surface, winner):
        # background
        layout = pygame.draw.rect(screen, COLOR_WHITE, ((screen.get_width() - self.width) // 2, (screen.get_height() - self.height) // 2, self.width, self.height))

        # background outline
        pygame.draw.rect(screen, COLOR_BLACK, ((screen.get_width() - self.width) // 2, (screen.get_height() - self.height) // 2, self.width, self.height), 1)

        # title
        title = get_large_font().render("게임 종료", True, COLOR_BLACK)
        title_rect = get_rect(title, screen.get_width() // 2, layout.y + get_medium_margin())
        screen.blit(title, title_rect)

        name = get_large_font().render(f"승자: {winner.name}", True, COLOR_BLACK)
        name_rect = get_center_rect(name, screen.get_rect())
        screen.blit(name, name_rect)

    def run_key_event(self, event):
        self.play_screen.init(),
        self.screen_controller.set_screen(ScreenType.START)

    def run_click_event(self, event):
        self.play_screen.init(),
        self.screen_controller.set_screen(ScreenType.START)