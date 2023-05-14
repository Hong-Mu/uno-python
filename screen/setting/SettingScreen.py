from __future__ import annotations

from model.screentype import ScreenType
from util.globals import *
from typing import TYPE_CHECKING

import pygame
if TYPE_CHECKING:
    from screen.ScreenController import ScreenController


class SettingScreen:
    def __init__(self, controller: ScreenController):

        self.controller = controller
        self.setting = controller.setting

        self.title_rect = None

        self.setting_select_enabled = True
        self.selected_setting_idx = 0
        self.settings = [
            {'text': '해상도', 'rect': None, 'result': None, 'selected_mode': 0, 'mode_rects': [], 'max': 3, 'type': MODE_SCREEN},
            {'text': '색약모드', 'rect': None, 'result': None, 'selected_mode': 0, 'mode_rects': [], 'max': 2, 'type': MODE_BLIND},
            {'text': '전체볼륨', 'rect': None, 'result': None, 'selected_mode': 0, 'mode_rects': [], 'max': 11, 'type': MODE_MASTER_VOLUME},
            {'text': '배경볼륨', 'rect': None, 'result': None, 'selected_mode': 0, 'mode_rects': [], 'max': 11, 'type': MODE_BACKGROUND_VOLUME},
            {'text': '효과음볼륨', 'rect': None, 'result': None, 'selected_mode': 0, 'mode_rects': [], 'max': 11, 'type': MODE_EFFECT_VOLUME},
            {'text': '우노 키 설정', 'rect': None, 'result': None, 'selected_mode': 0, 'mode_rects': [], 'max': 0, 'type': MODE_UNO_KEY},
            {'text': '덱 키 설정', 'rect': None, 'result': None, 'selected_mode': 0, 'mode_rects': [], 'max': 0, 'type': MODE_DECK_KEY},
            {'text': '초기화', 'rect': None, 'result': None, 'selected_mode': 0, 'mode_rects': [], 'max': 0, 'type': MODE_CLEAR},
            {'text': '돌아가기', 'rect': None, 'result': None, 'selected_mode': 0, 'mode_rects': [], 'max': 0, 'type': MODE_RETURN},
        ]
        self.max_text_right = get_medium_font().render('효과음볼륨', True, COLOR_BLACK).get_rect().right + get_medium_margin()

        # 모든 선택 상태
        self.mode_select_enabled = False


    def init(self):
        pass


    def draw(self, screen: pygame.Surface):
        screen.fill(COLOR_WHITE)
        self.draw_title(screen)
        self.draw_contents(screen)

    def draw_title(self, screen: pygame.Surface):
        title = get_large_font().render('설정', True, COLOR_BLACK)
        self.title_rect = get_rect(title, screen.get_width() // 2, get_medium_margin())
        screen.blit(title, self.title_rect)

    def draw_contents(self, screen: pygame.Surface):
        temp_right = 0
        for idx, setting in enumerate(self.settings):
            # 텍스트
            color = COLOR_BLACK if idx == self.selected_setting_idx and self.setting_select_enabled else COLOR_GRAY
            text = get_medium_font().render(setting['text'], True, color)
            text_rect = get_rect(text, text.get_width() // 2 + get_small_margin(), screen.get_height() // 2 + text.get_height() * (idx - len(self.settings) // 2))
            setting['rect'] = text_rect
            screen.blit(text, text_rect)

            # 값
            temp_value = str(self.setting.get(setting['type']))
            if setting['type'] == MODE_SCREEN:
                temp_value = str(self.setting.get_resolution())
            elif setting['type'] == MODE_BLIND:
                temp_value = 'OFF' if temp_value == '0' else 'ON'
            elif setting['type'] == MODE_UNO_KEY or setting['type'] == MODE_DECK_KEY:
                temp_value = chr(int(temp_value))


            if temp_value != 'None':
                value = get_medium_font().render(temp_value, True, COLOR_BLACK)
                value_rect = get_rect(value, screen.get_width() - value.get_width() - get_small_margin(), screen.get_height() // 2 + text.get_height() * (idx - len(self.settings) // 2))
                screen.blit(value, value_rect)

            # 모드 박스
            box_size = 20
            setting['mode_rects'] = []
            for mode in range(setting['max']):

                # 모드 박스
                color = COLOR_BLACK if mode == self.setting.get(setting['type']) else COLOR_GRAY
                mode_rect = pygame.draw.rect(screen, color, (self.max_text_right + box_size * mode * 1.1, text_rect.y + (text_rect.height - box_size) // 2, 20, 20))
                setting['mode_rects'].append(mode_rect)

                # 선택된 모드
                if idx == self.selected_setting_idx and self.mode_select_enabled and mode == setting['selected_mode']:
                    pygame.draw.rect(screen, COLOR_RED, (self.max_text_right + box_size * mode * 1.1, text_rect.y + (text_rect.height - box_size) // 2, 20, 20), 2)

    def run_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.run_key_events(event, event.key)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.run_setting_click_event(pos)
                self.run_mode_click_event(pos)

    def run_key_events(self, event, key):
        if self.setting_select_enabled:
            self.run_select_settings_event(event, key)

        elif self.mode_select_enabled:
            self.run_select_mode_event(key)

    def run_select_settings_event(self, event, key):
        if key == pygame.K_UP:
            self.updateSettingSelectIndex(-1)
        elif key == pygame.K_DOWN:
            self.updateSettingSelectIndex(1)
        elif key == pygame.K_RIGHT:
            if self.get_selected_setting()['max'] != 0:
                self.mode_select_enabled = True
                self.setting_select_enabled = False
        elif key == pygame.K_RETURN:
            if self.get_selected_type() == MODE_RETURN:
                if self.controller.is_paused:
                    self.controller.set_screen(ScreenType.PLAY)
                    self.controller.is_paused = False
                else:
                    self.controller.set_screen(ScreenType.HOME)
            elif self.get_selected_type() == MODE_CLEAR:
                self.setting.clear()
        else:
            if self.get_selected_type() == MODE_UNO_KEY or self.get_selected_type() == MODE_DECK_KEY:
                if event.unicode.isalnum():
                    self.setting.set(self.get_selected_type(), ord(event.unicode))



    def run_select_mode_event(self, key):
        if key == pygame.K_LEFT:
            if self.settings[self.selected_setting_idx]['selected_mode'] == 0:
                self.mode_select_enabled = False
                self.setting_select_enabled = True
            else:
                self.updateModeSelectIndex(self.settings[self.selected_setting_idx], -1)
        elif key == pygame.K_RIGHT:
            self.updateModeSelectIndex(self.settings[self.selected_setting_idx], 1)
        elif key == pygame.K_RETURN:
            self.setting.set(self.get_selected_type(), self.settings[self.selected_setting_idx]['selected_mode'])
            self.mode_select_enabled = False
            self.setting_select_enabled = True

    def run_setting_click_event(self, pos):
        for idx, setting in enumerate(self.settings):
            if setting['rect'].collidepoint(pos):
                self.selected_setting_idx = idx
                if setting['type'] == MODE_CLEAR:
                    self.setting.clear()
                elif setting['type'] == MODE_RETURN:
                    if self.controller.is_paused:
                        self.controller.set_screen(ScreenType.PLAY)
                        self.controller.is_paused = False
                    else:
                        self.controller.set_screen(ScreenType.HOME)

    def run_mode_click_event(self, pos):
        for setting in self.settings:
            if setting['max'] > 0:
                for mode_idx, mode_rect in enumerate(setting['mode_rects']):
                    if mode_rect.collidepoint(pos):
                        self.setting.set(setting['type'], mode_idx)

    def updateSettingSelectIndex(self, direction):
        self.selected_setting_idx = (self.selected_setting_idx + direction) % len(self.settings)

    def updateModeSelectIndex(self, setting, direction):

        setting['selected_mode'] = (setting['selected_mode'] + direction) % setting['max']
        print(setting['selected_mode'])

    def get_selected_setting(self):
        return self.settings[self.selected_setting_idx]
    def get_selected_type(self):
        return self.get_selected_setting()['type']
