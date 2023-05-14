from __future__ import annotations

import pygame.draw

from game.single import SinglePlayGame
from game.model.computer import Computer
from game.model.player import *
from model.screentype import ScreenType
from util.globals import *


class BaseLobbyScreen:
    def __init__(self, screen_controller):

        # 상위 의존성 초기화
        self.screen_controller = screen_controller
        self.screen = screen_controller.screen

        self.event_enabled = True

        # 메뉴 초기화
        self.menu_index = 0
        self.menus = None

        self.menu_enabled = True
        self.input_name_dialog_enabled = False
        self.input_name_text = 'Player'

        self.computer_layout_list = []
        self.computer_select_enabled = False
        self.computer_index = 0
        self.computer_layout_width = 200
        self.computer_height = (self.screen.get_height() - get_small_margin() * 6) // 5
        self.init_player(self.screen)

    def init(self):
        self.menu_enabled = True
        self.input_name_dialog_enabled = False
        self.computer_select_enabled = False
        self.input_name_text = 'Player'

        self.computer_layout_list = []
        self.computer_select_enabled = False
        self.computer_index = 0
        self.init_player(self.screen)

    def toggle_input_name_dialog(self):
        self.input_name_dialog_enabled = not self.input_name_dialog_enabled

    # 화면 그리기
    def draw(self, screen: pygame.Surface):
        screen.fill(COLOR_WHITE)

        self.draw_menu(screen)
        self.draw_player_layout(screen)

        if self.input_name_dialog_enabled:
            self.draw_input_name_dialog(screen)

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

    def draw_input_name_dialog(self, screen: pygame.Surface):
        width, height = 500, 300

        # 배경
        background = pygame.Surface(size=(width, height))
        background.fill(COLOR_WHITE)
        background_rect = get_center_rect(background, screen.get_rect())

        # 제목
        title = get_medium_font().render("이름 입력", True, COLOR_BLACK)

        # 확인
        submit = get_medium_font().render("확인", True, COLOR_BLACK)
        self.submit_rect = get_bottom_center_rect(submit, background_rect, -submit.get_width() // 2,
                                                  -(submit.get_height() + get_small_margin()))

        # 입력 박스
        input_name = get_small_font().render(self.input_name_text, True, COLOR_BLACK)

        input_background = pygame.Surface(
            size=(background_rect.width - 4 * get_medium_margin(), input_name.get_height() + get_small_margin()))
        input_background.fill(COLOR_LIGHT_GRAY)

        screen.blit(background, background_rect)
        pygame.draw.rect(screen, COLOR_BLACK, background_rect, 2)

        screen.blit(title,
                    get_top_center_rect(title, background_rect, x=-title.get_width() // 2, y=get_medium_margin()))
        screen.blit(submit, self.submit_rect)
        screen.blit(input_background, get_center_rect(input_background, background_rect))
        screen.blit(input_name, get_center_rect(input_name, background_rect))

    def draw_player_layout(self, screen):
        pygame.draw.rect(screen, COLOR_GRAY, (
        screen.get_width() - self.computer_layout_width, 0, self.computer_layout_width, screen.get_height()))
        self.draw_player(screen)

    def init_player(self, screen):
        for idx in range(5):
            computer_rect = pygame.Rect(screen.get_width() - self.computer_layout_width + get_small_margin(),
                                        get_small_margin() + (self.computer_height + get_small_margin()) * idx,
                                        self.computer_layout_width - get_small_margin() * 2, self.computer_height
                                        )

            self.computer_layout_list.append(
                {'name': f'Computer{idx}', 'rect': computer_rect, 'enabled': False if idx >= 1 else True})

    def draw_player(self, screen):
        for idx, computer in enumerate(self.computer_layout_list):
            if computer['enabled']:
                layout = pygame.draw.rect(screen, COLOR_PLAYER, computer['rect'])

                # 컴퓨터 이름
                name = get_small_font().render(computer['name'], True, COLOR_BLACK)
                name_rect = get_center_rect(name, layout)

                screen.blit(name, name_rect)

            # 선택된 플레이어 하이라이트
            if self.computer_select_enabled and idx == self.computer_index:
                # 투명 색상 적용
                surface = pygame.Surface(
                    (self.computer_layout_width - get_small_margin() * 2, self.computer_height),
                    pygame.SRCALPHA)
                surface.fill(COLOR_TRANSPARENT_WHITE)
                screen.blit(surface, (screen.get_width() - self.computer_layout_width + get_small_margin(),
                                      get_small_margin() + (self.computer_height + get_small_margin()) * idx))

    # 이벤트 처리
    def run_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.run_key_event(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.run_click_event(event)

    # 키입력 이벤트 처리
    def run_key_event(self, event):
        if self.input_name_dialog_enabled:
            self.run_input_name_dialog_key_event(event)
        elif self.menu_enabled:
            self.run_menu_key_event(event)
        elif self.computer_select_enabled:
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
            self.computer_select_enabled = True

    def run_input_name_dialog_key_event(self, event):
        key = event.key
        if key == pygame.K_ESCAPE:
            return self.toggle_input_name_dialog()

        if key == pygame.K_RETURN:
            self.update_name_and_start_game()

        # 키보드 입력
        elif key == pygame.K_BACKSPACE:
            self.input_name_text = self.input_name_text[:-1]

        elif event.unicode.isalnum():
            self.input_name_text += event.unicode

        else:
            pass
            # TODO: 알파벳 숫자만 입력가능합니다.

    def update_name_and_start_game(self):
        # 이름 설정
        players = [Player(self.input_name_text)]
        # 컴퓨터 플레이어 설정 적용
        for idx, computer in enumerate(self.computer_layout_list):
            if computer['enabled']:
                players.append(Computer(computer['name']))

        # 화면 이동
        self.screen_controller.set_game(SinglePlayGame())
        self.screen_controller.game.set_players(players)
        self.screen_controller.game.start_game()
        self.screen_controller.set_screen(ScreenType.PLAY)


    def run_player_select_key_event(self, event):
        key = event.key
        if key == pygame.K_UP:
            self.computer_index = (self.computer_index - 1) % 5
        elif key == pygame.K_DOWN:
            self.computer_index = (self.computer_index + 1) % 5
        elif key == pygame.K_LEFT:
            self.menu_enabled = True
            self.computer_select_enabled = False
        elif key == pygame.K_RETURN:
            self.toggle_player_enabled()

    def toggle_player_enabled(self):
        if self.computer_index == 0:
            return
        self.computer_layout_list[self.computer_index]['enabled'] = not self.computer_layout_list[self.computer_index][
            'enabled']

    def run_click_event(self, event):
        if self.input_name_dialog_enabled:
            self.run_input_name_dialog_click_event(event)
        else:
            self.run_menu_click_event(event)
            self.run_player_select_click_event(event)

    def run_menu_click_event(self, event):
        pos = pygame.mouse.get_pos()
        for menu in self.menus:
            if menu['rect'].collidepoint(pos):
                menu['action']()

    def run_player_select_click_event(self, event):
        pos = pygame.mouse.get_pos()
        for idx, computer_layout in enumerate(self.computer_layout_list):
            if computer_layout['rect'].collidepoint(pos):
                if idx == 0:
                    return
                computer_layout['enabled'] = not computer_layout['enabled']

    def run_input_name_dialog_click_event(self, event):
        pos = pygame.mouse.get_pos()
        if self.submit_rect.collidepoint(pos):
            self.update_name_and_start_game()

    def disable_event(self):
        self.event_enabled = False

    def enable_event(self):
        self.event_enabled = True

