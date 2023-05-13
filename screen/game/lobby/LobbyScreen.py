from __future__ import annotations

import pygame.draw

from game.single import SinglePlayGame
from game.model.computer import Computer
from game.model.player import *
from screen.model.screentype import ScreenType
from util.globals import *


class LobbyScreen:
    def __init__(self, screen_controller):

        # 상위 의존성 초기화
        self.screen_controller = screen_controller
        self.screen = screen_controller.screen


        # 메뉴 초기화
        self.menu_index = 0
        self.menus = [
            {'text': '플레이', 'view': None, 'rect': None, 'action': self.toggle_input_name_dialog },
            {'text': '돌아가기', 'view': None, 'rect': None, 'action': lambda: (
                self.screen_controller.set_screen_type(ScreenType.START)
            )},
        ]

        self.menu_enabled = True
        self.input_name_dialog_enabled = False
        self.input_name_text = 'Player'

        self.computer_layout_list = []
        self.computer_select_enabled = False
        self.computer_index = 0
        self.computer_layout_width = 200
        self.computer_height = (self.screen.get_height() - get_small_margin() * 6) // 5
        self.init_computer(self.screen)


    def init(self):
        self.menu_enabled = True
        self.input_name_dialog_enabled = False
        self.computer_select_enabled = False
        self.input_name_text = 'Player'

        self.computer_layout_list = []
        self.computer_select_enabled = False
        self.computer_index = 0
        self.init_computer(self.screen)


    def toggle_input_name_dialog(self):
        self.input_name_dialog_enabled = not self.input_name_dialog_enabled
    # 화면 그리기
    def draw(self, screen: pygame.Surface):

        # 선택 메뉴 그리기
        def draw_menu():
            for idx, item in enumerate(self.menus):
                # 플레이 텍스트
                text_play = get_medium_font().render(item['text'], True,
                                                     COLOR_BLACK if self.menu_enabled and idx == self.menu_index else COLOR_GRAY)
                text_play_rect = get_left_center_rect(text_play, screen.get_rect(), y=text_play.get_height() * idx,
                                                      x=get_medium_margin())

                # 기존 객체에 추가
                self.menus[idx]['view'] = text_play
                self.menus[idx]['rect'] = text_play_rect

                screen.blit(text_play, text_play_rect)

        # 함수 호출
        screen.fill(COLOR_WHITE)
        draw_menu()
        self.draw_computer_layout(screen)

        if self.input_name_dialog_enabled:
            self.draw_input_name_dialog(screen)

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
        self.submit_rect = get_bottom_center_rect(submit, background_rect, -submit.get_width() // 2, -(submit.get_height() + get_small_margin()))

        # 입력 박스
        input_name = get_small_font().render(self.input_name_text, True, COLOR_BLACK)

        input_background = pygame.Surface(size = (background_rect.width - 4 * get_medium_margin(), input_name.get_height() + get_small_margin()))
        input_background.fill(COLOR_LIGHT_GRAY)

        screen.blit(background, background_rect)
        pygame.draw.rect(screen, COLOR_BLACK, background_rect, 2)

        screen.blit(title, get_top_center_rect(title, background_rect, x = -title.get_width() // 2, y = get_medium_margin()))
        screen.blit(submit, self.submit_rect)
        screen.blit(input_background, get_center_rect(input_background, background_rect))
        screen.blit(input_name, get_center_rect(input_name, background_rect))

    def draw_computer_layout(self, screen):
        pygame.draw.rect(screen, COLOR_GRAY, (screen.get_width() - self.computer_layout_width, 0, self.computer_layout_width, screen.get_height()))
        self.draw_computer(screen)

    def init_computer(self, screen):
        for idx in range(5):
            computer_rect = pygame.Rect(screen.get_width() - self.computer_layout_width + get_small_margin(),
                             get_small_margin() + (self.computer_height + get_small_margin()) * idx,
                             self.computer_layout_width - get_small_margin() * 2, self.computer_height
                            )

            self.computer_layout_list.append({'name': f'Computer{idx}', 'rect': computer_rect, 'enabled': False if idx >= 1 else True})

    def draw_computer(self, screen):
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
                self.run_key_event(event, event.key)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.run_click_event(event, pygame.mouse.get_pos())

    # 키입력 이벤트 처리
    def run_key_event(self, event, key):
        if self.input_name_dialog_enabled:
            self.run_input_name_dialog_key_event(event, key)
        elif self.menu_enabled:
            self.run_menu_key_event(key)
        elif self.computer_select_enabled:
            self.run_computer_select_key_event(key)

    def run_menu_key_event(self, key):
        if key == pygame.K_UP:
            self.menu_index = (self.menu_index - 1) % len(self.menus)
        elif key == pygame.K_DOWN:
            self.menu_index = (self.menu_index + 1) % len(self.menus)
        elif key == pygame.K_RETURN:
            self.menus[self.menu_index]['action']()

        elif key == pygame.K_RIGHT:
            self.menu_enabled = False
            self.computer_select_enabled = True

    def run_input_name_dialog_key_event(self, event, key):
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
            #TODO: 알파벳 숫자만 입력가능합니다.

    def update_name_and_start_game(self):
        # 이름 설정
        players = [Player(self.input_name_text)]
        # 컴퓨터 플레이어 설정 적용
        for idx, computer in enumerate(self.computer_layout_list):
            if computer['enabled']:
                players.append(Computer(computer['name']))

        # 화면 이동
        self.screen_controller.set_screen_type(ScreenType.PLAY)
        self.screen_controller.set_game(SinglePlayGame())
        self.screen_controller.game.set_players(players)
        self.screen_controller.game.start_game()

    def run_computer_select_key_event(self, key):
        if key == pygame.K_UP:
            self.computer_index = (self.computer_index - 1) % 5
        elif key == pygame.K_DOWN:
            self.computer_index = (self.computer_index + 1) % 5
        elif key == pygame.K_LEFT:
            self.menu_enabled = True
            self.computer_select_enabled = False
        elif key == pygame.K_RETURN:
            self.toggle_computer_enabled()
    def toggle_computer_enabled(self):
        if self.computer_index == 0:
            return
        self.computer_layout_list[self.computer_index]['enabled'] = not self.computer_layout_list[self.computer_index]['enabled']

    def run_click_event(self, event, pos):
        if self.input_name_dialog_enabled:
            self.run_input_name_dialog_click_event(pos)
        else:
            self.run_menu_click_event(pos)
            self.run_computer_select_click_event(pos)


    def run_menu_click_event(self, pos):
        for menu in self.menus:
            if menu['rect'].collidepoint(pos):
                menu['action']()

    def run_computer_select_click_event(self, pos):
        for idx, computer_layout in enumerate(self.computer_layout_list):
            if computer_layout['rect'].collidepoint(pos):
                if idx == 0:
                    return
                computer_layout['enabled'] = not computer_layout['enabled']


    def run_input_name_dialog_click_event(self, pos):
        if self.submit_rect.collidepoint(pos):
            self.update_name_and_start_game()

