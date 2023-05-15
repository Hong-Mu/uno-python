from __future__ import annotations
from typing import TYPE_CHECKING

from base.basescreen import BaseScreen
from gamesocket.event import SocketEvent
from screen.home.dialog.inputaddress import InputAddressDialog
from screen.home.dialog.multiplaydialog import MultiPlayDialog
from model.screentype import ScreenType
from util.globals import *
import pygame

if TYPE_CHECKING:
    from screen.ScreenController import ScreenController


class HomeScreen(BaseScreen):
    def __init__(self, screen_controller):
        super().__init__(screen_controller)
        self.client = screen_controller.client

        self.dialogs = []

        self.multi_play_dialog = MultiPlayDialog(self)

        self.input_address_dialog = InputAddressDialog(self, on_confirm=self.connect)

        self.dialogs.extend([
            self.multi_play_dialog,
            self.input_address_dialog
        ])

        self.alert_enabled = False

        # 초기 설정
        self.selected_menu_index = 0
        self.menu_dict = [
            {'text': '싱글플레이', 'view': None, 'rect': None, 'action': lambda: (
                self.screen_controller.set_screen(ScreenType.LOBBY_SINGLE),
            )},
            {'text': '멀티플레이', 'view': None, 'rect': None, 'action': lambda: (
                self.multi_play_dialog.show(),
            )},
            {'text': '스토리모드', 'view': None, 'rect': None, 'action': lambda: (
                self.screen_controller.set_screen(ScreenType.STORY),
            )},
            {'text': '업적', 'action': lambda: self.screen_controller.set_screen(ScreenType.ACHIEVEMENT), 'view': None, 'rect': None},
            {'text': '설정', 'action': lambda: self.screen_controller.set_screen(ScreenType.SETTING), 'view': None, 'rect': None },
            {'text': '종료', 'action': lambda: self.screen_controller.stop(), 'view': None, 'rect': None },
        ]

    def init(self):
        super().init()
        self.multi_play_dialog.init()

    # 시작 화면
    def draw(self, screen):
        super().draw(screen)

        self.draw_title(screen)
        self.draw_menu(screen, self.menu_dict)

        if self.alert_enabled:
            self.draw_alert(screen, "상/하 방향키와 엔터로 메뉴를 선택할 수 있습니다.")

        if self.multi_play_dialog.enabled:
            self.multi_play_dialog.draw(screen)

        if self.input_address_dialog.enabled:
            self.input_address_dialog.draw(screen)

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

    def run_key_event(self, event):
        if self.event_enabled:
            self.run_menu_key_event(event)

        elif self.multi_play_dialog.enabled:
            self.multi_play_dialog.run_key_event(event)

        elif self.input_address_dialog.enabled:
            self.input_address_dialog.run_key_event(event)


    def run_click_event(self, event):
        if self.event_enabled:
            self.run_menu_click_event(event)

        elif self.multi_play_dialog.enabled:
            self.multi_play_dialog.run_click_event(event)

        elif self.input_address_dialog.enabled:
            self.input_address_dialog.run_click_event(event)

    def run_menu_click_event(self, event):
        for menu in self.menu_dict:
            if menu['rect']:
                if menu['rect'].collidepoint(pygame.mouse.get_pos()):
                    menu['action']()

    def run_menu_key_event(self, event):
        self.alert_enabled = False
        if event.key == pygame.K_UP:
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_dict)
        elif event.key == pygame.K_DOWN:
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_dict)
        elif event.key == pygame.K_RETURN:
            self.menu_dict[self.selected_menu_index]['action']()
        else:
            self.alert_enabled = True

    def disable_event(self):
        super().disable_event()
        for dialog in self.dialogs:
            dialog.enabled = False

    def connect(self):
        try:
            self.client.connect(ip=self.input_address_dialog.input, listener=self.screen_controller.on_server_message)
            self.client.emit(SocketEvent.JOIN, {'passwrod': 0})
        except Exception as e:
            print(e)
