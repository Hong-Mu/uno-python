from __future__ import annotations
from typing import TYPE_CHECKING

from screen.game.play.dialog.multiplaydialog import MultiPlayDialog
from screen.model.screentype import ScreenType
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
                self.screen_controller.set_screen(ScreenType.LOBBY),
                self.screen_controller.screens[ScreenType.LOBBY].init()
            )},
            {'text': '멀티플레이', 'view': None, 'rect': None, 'action': lambda: (
                self.multi_play_dialog.toggle(),
            )},
            {'text': '스토리모드', 'view': None, 'rect': None, 'action': lambda: (
                self.screen_controller.set_screen_type(ScreenType.STORY),
                self.screen_controller.screens[ScreenType.STORY].init()
            )},
            {'text': '업적', 'action': lambda: self.screen_controller.set_screen(ScreenType.ACHIVEMENT), 'view': None, 'rect': None},
            {'text': '설정', 'action': lambda: self.screen_controller.set_screen(ScreenType.SETTING), 'view': None, 'rect': None },
            {'text': '종료', 'action': lambda: self.screen_controller.stop(), 'view': None, 'rect': None },
        ]

        self.multi_play_dialog = MultiPlayDialog(self)

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

        if self.multi_play_dialog.enabled:
            self.multi_play_dialog.draw(screen)


    # 시작 화면 이벤트 처리
    def run_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.process_key_event(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.run_click_event(event)

    def process_key_event(self, event):
        if self.multi_play_dialog.enabled:
            self.multi_play_dialog.run_key_event(event)
        else:
            self.run_menu_key_event(event)

    def run_click_event(self, event):
        if self.multi_play_dialog.enabled:
            self.multi_play_dialog.run_click_event(event)
        else:
            self.run_menu_click_event(event)

    def run_menu_click_event(self, event):
        for menu in self.menu_dict:
            if menu['rect']:
                if menu['rect'].collidepoint(pygame.mouse.get_pos()):
                    menu['action']()

    def run_menu_key_event(self, event):
        self.hide_alert()
        if event.key == pygame.K_UP:
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_dict)
        elif event.key == pygame.K_DOWN:
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_dict)
        elif event.key == pygame.K_RETURN:
            self.menu_dict[self.selected_menu_index]['action']()
        else:
            self.show_alert()

    def show_alert(self):
        self.alert_visibility = True

    def hide_alert(self):
        self.alert_visibility = False

    def draw_title(self, screen):
        self.title = get_large_font().render("Uno Game", True, COLOR_BLACK)
        self.title_rect = get_rect(self.title, screen.get_width() // 2, screen.get_height() // 5)
        screen.blit(self.title, self.title_rect)

    def draw_menu(self, screen, menus):
        for index, menu in enumerate(menus):
            text = get_medium_font().render(menu['text'], True, COLOR_GRAY if  index != self.selected_menu_index else COLOR_BLACK)
            rect = get_rect(text, screen.get_width() // 2, screen.get_height() // 3 + text.get_height() * index)
            self.menu_dict[index].update({'view': text, 'rect': rect})
            screen.blit(text, rect)

    def draw_alert(self, screen: pygame.Surface, text):
        view = get_small_font().render(text, True, COLOR_RED)
        rect = get_rect(view, screen.get_width() // 2, screen.get_height() - view.get_height() - get_medium_margin())
        screen.blit(view, rect)
