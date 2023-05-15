from __future__ import annotations

import pygame.draw

from game.single import SinglePlayGame
from game.model.computer import Computer
from game.model.player import *
from model.screentype import ScreenType
from util.globals import *


class BaseLobbyScreen:
    def __init__(self, screen_controller):
        self.screen_controller = screen_controller
        self.screen = screen_controller.screen

        self.event_enabled = True

        self.menu_index = 0
        self.menus = None
        self.menu_enabled = True

        self.player_slots = []
        self.slot_select_enabled = False
        self.slot_idx = 0

        self.slot_width = 200
        self.slot_height = None

        self.init_slot()

    def init(self):
        pass

    def init_slot(self):
        pass

    def on_destroy(self):
        pass

    # 화면 그리기
    def draw(self, screen: pygame.Surface):
        screen.fill(COLOR_WHITE)
        self.run_periodiacally(screen)

        self.draw_menu(screen)
        self.draw_slot_layout(screen)

    def run_periodiacally(self, screen):
        self.slot_height = (self.screen.get_height() - get_small_margin() * 6) // 5

    def draw_menu(self, screen):
        for idx, item in enumerate(self.menus):
            # 텍스트
            color = COLOR_BLACK if self.menu_enabled and idx == self.menu_index else COLOR_GRAY
            text = get_medium_font().render(item['text'], True, color)
            text_rect = get_left_center_rect(text, screen.get_rect(), y=text.get_height() * idx - (text.get_height() * len(self.menus)) // 2, x=get_medium_margin())

            # 기존 객체에 추가
            self.menus[idx]['view'] = text
            self.menus[idx]['rect'] = text_rect

            screen.blit(text, text_rect)

    def draw_slot_layout(self, screen):
        background = pygame.draw.rect(screen, COLOR_GRAY, (screen.get_width() - self.slot_width, 0, self.slot_width, screen.get_height()))
        self.draw_player(screen)

    def draw_player(self, screen):
        for idx, slot in enumerate(self.player_slots):
            slot['rect'] = pygame.Rect(screen.get_width() - self.slot_width + get_small_margin(),
                                       get_small_margin() + (self.slot_height + get_small_margin()) * idx,
                                       self.slot_width - get_small_margin() * 2, self.slot_height)
            if slot['enabled']:
                background_rect = pygame.draw.rect(screen, COLOR_PLAYER, slot['rect'])

                name = get_small_font().render(slot['name'], True, COLOR_BLACK)
                screen.blit(name, get_center_rect(name, background_rect))

            # 선택된 플레이어 하이라이트
            if self.slot_select_enabled and idx == self.slot_idx:
                surface = pygame.Surface((self.slot_width - get_small_margin() * 2, self.slot_height),pygame.SRCALPHA)
                surface.fill(COLOR_TRANSPARENT_WHITE)
                screen.blit(surface, (screen.get_width() - self.slot_width + get_small_margin(), get_small_margin() + (self.slot_height + get_small_margin()) * idx))

    # 이벤트 처리
    def run_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.run_key_event(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.run_click_event(event)

    # 키입력 이벤트 처리
    def run_key_event(self, event):
        if self.menu_enabled:
            self.run_menu_key_event(event)

        elif self.slot_select_enabled:
            self.run_player_select_key_event(event)

    def run_menu_key_event(self, event):
        key = event.key
        if key == pygame.K_UP:
            self.menu_index = (self.menu_index - 1) % len(self.menus)
        elif key == pygame.K_DOWN:
            self.menu_index = (self.menu_index + 1) % len(self.menus)
        elif key == pygame.K_RETURN:
            self.menus[self.menu_index]['action']()

        elif key == pygame.K_RIGHT:
            self.menu_enabled = False
            self.slot_select_enabled = True


    def run_player_select_key_event(self, event):
        key = event.key
        if key == pygame.K_UP:
            self.slot_idx = (self.slot_idx - 1) % 5
        elif key == pygame.K_DOWN:
            self.slot_idx = (self.slot_idx + 1) % 5
        elif key == pygame.K_LEFT:
            self.menu_enabled = True
            self.slot_select_enabled = False
        elif key == pygame.K_RETURN:
            self.toggle_player_enabled()

    def toggle_player_enabled(self):
        if self.slot_idx == 0:
            return
        self.player_slots[self.slot_idx]['enabled'] = not self.player_slots[self.slot_idx]['enabled']

    def run_click_event(self, event):
        self.run_menu_click_event(event)
        self.run_slot_click_event(event)

    def run_menu_click_event(self, event):
        pos = pygame.mouse.get_pos()
        for menu in self.menus:
            if menu['rect'].collidepoint(pos):
                menu['action']()

    def run_slot_click_event(self, event):
        pos = pygame.mouse.get_pos()
        for idx, slot in enumerate(self.player_slots):
            if slot['rect'].collidepoint(pos):
                if idx == 0:
                    return
                slot['enabled'] = not slot['enabled']

    def disable_event(self):
        self.event_enabled = False

    def enable_event(self):
        self.event_enabled = True

