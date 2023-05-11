from __future__ import annotations
from typing import TYPE_CHECKING

from util.globals import *
import pygame

if TYPE_CHECKING:
    from screen.ScreenController import ScreenController

class HomeScreen:
    def __init__(self, screen_controller):
        self.screen_controller: ScreenController = screen_controller

        # 초기 설정
        self.selected_menu_index = 0
        self.menu_dict = [
            {'text': '싱글플레이', 'view': None, 'rect': None, 'action': lambda: (
                self.screen_controller.set_screen(TYPE_LOBBY),
                self.screen_controller.screens[TYPE_LOBBY].init()
            )},
            {'text': '스토리모드', 'view': None, 'rect': None, 'action': lambda: (
                self.screen_controller.set_screen_type(TYPE_STORY),
                self.screen_controller.screens[TYPE_STORY].init()
            )},
            {'text': '업적', 'action': lambda: self.screen_controller.set_screen(TYPE_ACHIVEMENT), 'view': None, 'rect': None},
            {'text': '설정', 'action': lambda: self.screen_controller.set_screen(TYPE_SETTING), 'view': None, 'rect': None },
            {'text': '종료', 'action': lambda: self.screen_controller.stop(), 'view': None, 'rect': None },
        ]

        self.alert_visibility = False # 다른 키 입력 알림

        self.draw_title(self.screen_controller.screen)
        self.draw_menu(self.screen_controller.screen, self.menu_dict)


    # 시작 화면
    def draw(self, screen):
        screen.fill(COLOR_WHITE)

        self.draw_title(screen)
        self.draw_menu(screen, self.menu_dict)

        if self.alert_visibility:
            self.draw_alert(screen, "상/하 방향키와 엔터로 메뉴를 선택할 수 있습니다.")


    # 시작 화면 이벤트 처리
    def run_events(self, events):
        for event in events:
            # 마우스 좌표 (x, y)
            pos = pygame.mouse.get_pos()

            if event.type == pygame.KEYDOWN: # 키보드 입력 처리
                self.process_key_event(event.key)

            elif event.type == pygame.MOUSEBUTTONUP: # 마우스 클릭 처리
                for menu in self.menu_dict:
                    if menu['rect']:
                        if menu['rect'].collidepoint(pos):
                            menu['action']()





    def process_key_event(self, key):
        self.hide_alert()
        if key == pygame.K_UP:
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_dict)
        elif key == pygame.K_DOWN:
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_dict)
        elif key == pygame.K_RETURN:
            self.menu_dict[self.selected_menu_index]['action']()
        else:
            self.show_alert()

    def show_alert(self):
        self.alert_visibility = True

    def hide_alert(self):
        self.alert_visibility = False

    def draw_title(self, screen):
        self.title = get_large_font().render("Uno Game", True, COLOR_BLACK)
        self.title_rect = get_rect(self.title, screen.get_width() // 2, screen.get_height() // 3)
        screen.blit(self.title, self.title_rect)

    def draw_menu(self, screen, menus):
        for index, menu in enumerate(menus):
            text = get_medium_font().render(menu['text'], True, COLOR_GRAY if  index != self.selected_menu_index else COLOR_BLACK)
            rect = get_rect(text, screen.get_width() // 2, screen.get_height() // 2 + text.get_height() * index)
            self.menu_dict[index].update({'view': text, 'rect': rect})
            screen.blit(text, rect)

    def draw_alert(self, screen: pygame.Surface, text):
        view = get_small_font().render(text, True, COLOR_RED)
        rect = get_rect(view, screen.get_width() // 2, screen.get_height() - view.get_height() - get_medium_margin())
        screen.blit(view, rect)
