from __future__ import annotations
from typing import TYPE_CHECKING

import pygame
from util.globals import *

if TYPE_CHECKING:
    from screen.game.play.PlayScreen import PlayScreen


class EscapeDialog:
    def __init__(self, play_screen: PlayScreen):
        # 의존성 객체
        self.play_screen = play_screen
        self.screen_controller = play_screen.screen_controller

        # 다이얼로그 관련 객체
        self.enabled = False
        self.width = 500
        self.height = 300

        self.menu_idx = 0

        self.menus = [
            {'text': '설정', 'view': None, 'rect': None,
             'action': lambda: (
                 self.screen_controller.set_screen(TYPE_SETTING),
                 self.screen_controller.set_paused(),
             )},
            {'text': '종료', 'view': None, 'rect': None, 'action': lambda: (
                self.play_screen.init(),
                self.screen_controller.set_screen(TYPE_START),
            )
             }
        ]

    def draw(self, screen: pygame.Surface):
        layout = pygame.draw.rect(screen, COLOR_WHITE, (
        (screen.get_width() - self.width) // 2, (screen.get_height() - self.height) // 2, self.width, self.height))
        # background outline
        pygame.draw.rect(screen, COLOR_BLACK,
                         ((screen.get_width() - self.width) // 2, (screen.get_height() - self.height) // 2, self.width, self.height), 1)

        title = get_large_font().render("일시정지", True, COLOR_BLACK)
        title_rect = get_rect(title, screen.get_width() // 2, layout.y + get_medium_margin())
        screen.blit(title, title_rect)

        self.draw_menu(screen)

    def draw_menu(self, screen: pygame.Surface):
        for idx, menu in enumerate(self.menus):
            color = COLOR_GRAY if idx != self.menu_idx else COLOR_BLACK
            text = get_medium_font().render(menu['text'], True, color)
            rect = get_rect(text, screen.get_width() // 2, screen.get_height() // 2 + text.get_height() * idx)
            menu.update({'view': text, 'rect': rect})
            screen.blit(text, rect)

    def run_key_event(self, key):
        if key == pygame.K_UP:
            self.menu_idx = (self.menu_idx - 1) % len(self.menus)
        elif key == pygame.K_DOWN:
            self.menu_idx = (self.menu_idx + 1) % len(self.menus)
        elif key == pygame.K_RETURN:
            self.menus[self.menu_idx]['action']()

    def run_click_event(self, pos):
        for menu in self.menus:
            if menu['rect'] and menu['rect'].collidepoint(pos):
                menu['action']()