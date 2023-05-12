from __future__ import annotations

import random
from typing import TYPE_CHECKING

from game.model.computer import Computer
from game.model.skill import Skill
from game.story.regiona import GameA
from screen.game.play.section.escapeDialog import EscapeDialog
from screen.game.play.section.gameOverDialog import GameOverDialog
from screen.game.play.section.playersLayout import PlayersLayout
from util.globals import *
from screen.animate.animate import AnimateController
from screen.game.play.section.board import Board
from screen.game.play.section.cardboard import CardBoard
import time

if TYPE_CHECKING:
    from screen.ScreenController import ScreenController


class PlayScreen:

    def __init__(self, screen_controller: ScreenController):

        # 의존성 객체
        self.screen_controller = screen_controller
        self.animate_controller = AnimateController()
        self.game = None
        
        # 레이아웃 모음
        self.players_layout = PlayersLayout(self)
        self.board = Board(self)
        self.card_board = CardBoard(self)

        self.escape_dialog = EscapeDialog(self)
        self.game_over_dialog = GameOverDialog(self)

        # 카드보드 관련 변수 TODO: 나중에 분리
        self.my_cards_selected_index = 0
        self.cards_line_size = 0  # 한 줄 당 카드 개수

        # 게임 관련
        self.stop_timer_enabled = False  # 일시정지 상태
        self.pause_temp_time = None  # 일시정지 임시 시간 저장 변수
        
        self.deck_select_enabled = False  # 덱 선택 가능 상태
        self.card_select_enabled = False  # 카드 선택 가능 상태

        self.select_color_enabled = False

        self.combo_enabled = False

        self.to_computer_play_idx = None

        # 애니메이션 관련
        self.animate_view = None
        
        self.animate_deck_to_player_enabled = False
        self.animate_board_player_to_current_card_enabled = False
        self.animate_current_player_to_current_card_enabled = False

        self.is_animation_running = False

    def pause_game(self):  # 일시정지
        self.stop_timer_enabled = True
        self.pause_temp_time = time.time()

    def continue_game(self):  # 다시 시작
        self.stop_timer_enabled = False

    # 초기화 함수
    def init(self):
        self.escape_dialog.enabled = False
        self.escape_dialog.menu_idx = 0

        self.stop_timer_enabled = False  # 일시정지 상태
        self.pause_temp_time = None  # 일시정지 임시 시간 저장 변수

        self.deck_select_enabled = False  # 덱 선택 가능 상태
        self.card_select_enabled = False  # 카드 선택 가능 상태

        self.select_color_enabled = False

        self.animate_deck_to_player_enabled = False
        self.animate_board_player_to_current_card_enabled = False
        self.animate_current_player_to_current_card_enabled = False

        if self.escape_dialog.enabled:
            self.pause_game()
        else:
            self.continue_game()

    # 다이얼로그 표시 상태 변경
    def toggle_escape_dialog(self):
        self.escape_dialog.enabled = not self.escape_dialog.enabled

        # 일시정지 시간 처리
        if self.escape_dialog.enabled:
            self.pause_game()
        else:
            self.continue_game()

    # 모든 View
    def draw(self, screen):
        screen.fill(COLOR_WHITE)
        self.game = self.screen_controller.game

        if not self.game.is_started:
            return

        # 인덱스 에러 해결을 위한 함수 모음
        self.resolve_error()

        # 화면 섹션 그리기
        self.board.draw(screen)
        self.card_board.draw(screen)
        self.players_layout.draw(screen)

        # 게임 종료
        if self.game.is_game_over():
            self.game_over_dialog.draw(screen, self.game.get_winner())
            return

        # 턴 시작 시 단 1번 동작
        if self.game.is_turn_start:
            self.init_turn()

        # 게임 관련 동작 업데이트
        self.check_time() # 타이머 관련 동작
        self.game.update_uno_enabled()  # 우노 상태 확인

        # 일시정지 다이얼로그
        if self.escape_dialog.enabled:
            self.escape_dialog.draw(screen)
            return

        # 애니메이션
        self.draw_animation(screen)

        if not self.is_animation_running:
            self.run_computer()

    def init_turn(self):
        self.select_color_enabled = False
        self.check_uno_clicked()
        self.game.run_in_turn_start()
        self.game.is_turn_start = False
    def draw_animation(self, screen):
        self.is_animation_running = True
        if self.animate_deck_to_player_enabled:
            self.animate_deck_to_player(screen)
            # 카드 제출 애니메이션
        elif self.animate_board_player_to_current_card_enabled:
            self.animate_board_player_to_current_card(screen)

        elif self.animate_current_player_to_current_card_enabled:
            self.animate_current_player_to_current_card(screen)
        else:
            self.is_animation_running = False


    def animate_deck_to_player(self, screen):
        if self.animate_controller.enabled:
            self.pause_game()
            self.animate_controller.draw(screen)
        else:
            self.animate_deck_to_player_end()

    def animate_deck_to_player_end(self):
        if self.game.can_uno_penalty: # 우노 패널티 결과
            self.game.penalty(self.game.previous_player_index)
            self.game.uno_enabled = False
            self.game.uno_clicked = False
            self.game.can_uno_penalty = False
            self.animate_deck_to_player_enabled = False
            self.continue_game()
            
        elif self.game.skill_plus_cnt > 0: # 기술 카드 부여 결과
            self.game.penalty(self.game.next_player_index)
            print('기술 1장 부여')
            self.game.skill_plus_cnt -= 1
            if self.game.skill_plus_cnt > 0:
                self.on_deck_selected()
            else:
                turn = 0 if self.combo_enabled else 1
                self.game.next_turn(turn)
                self.animate_deck_to_player_enabled = False
                self.continue_game()
        else: # 일반 드로우
            self.game.draw()
            self.game.next_turn()
            self.animate_deck_to_player_enabled = False
            self.continue_game()

    def animate_board_player_to_current_card(self, screen):
        if self.animate_controller.enabled:
            self.pause_game()
            self.animate_controller.draw(screen)
        else:
            self.animate_board_player_to_current_card_end()


    def animate_board_player_to_current_card_end(self):
        self.game.play(self.board_player_to_current_card_idx)
        self.run_card(self.game.current_card)

        self.animate_board_player_to_current_card_enabled = False
        self.continue_game()

    def animate_current_player_to_current_card(self, screen):
        if self.animate_controller.enabled:
            self.pause_game()
            self.animate_controller.draw(screen)
        else:
            self.animate_current_player_to_current_card_end()


    def animate_current_player_to_current_card_end(self):
        self.game.play(self.to_computer_play_idx)
        self.run_card(self.game.current_card)

        self.animate_current_player_to_current_card_enabled = False
        self.continue_game()

    # 카드 실행
    def run_card(self, card: Card):
        if card.value == Skill.REVERSE.value:
            self.game.toggle_turn_direction()
            self.game.next_turn()

        elif card.value == Skill.JUMP.value:
            self.game.skip_turn()

        elif card.value == Skill.PLUS_2.value:
            self.game.skill_plus_cnt = 2
            self.on_deck_selected()

        elif card.value == Skill.PLUS_4.value:
            self.game.skill_plus_cnt = 4
            self.on_deck_selected()
        elif card.value == Skill.OMIT.value:
            self.game.next_turn(0)
        elif card.value == Skill.JUMP_RANDOM.value:
            self.game.skip_turn(random.randint(1, len(self.game.players) - 1))
        elif card.value == Skill.COLOR.value:
            self.select_color_enabled = True
        elif card.value == Skill.COMBO.value:
            self.combo_enabled = True
            self.game.toggle_turn_direction() # 리버스
            self.game.skill_plus_cnt = 2
            self.on_deck_selected()
        else:
            self.game.next_turn()


    def check_time(self):
        if self.stop_timer_enabled:  # 일시정지 상태
            current_time = time.time()
            self.game.turn_start_time = self.game.turn_start_time + (current_time - self.pause_temp_time)
            self.pause_temp_time = current_time

        elif (time.time() - self.game.turn_start_time) > self.game.turn_time:  # 턴 종료
            self.on_deck_selected()

        
        # 나의 턴 확인
        self.card_select_enabled = self.game.board_player_index == self.game.current_player_index

    def check_uno_clicked(self):
        if self.game.uno_enabled:
            if self.game.uno_clicked:
                if self.game.uno_clicked_player_index == self.game.previous_player_index:
                    print('우노 버튼 해당 플레이어 클릭: 패널티 미부여')
                    print(f'{self.game.uno_clicked_player_index} {self.game.previous_player_index}')
                    self.game.uno_enabled = False
                    self.game.uno_clicked = False
                else:
                    print('다른 플레이어로 인한 패널티 부여')
                    self.game.can_uno_penalty = True
                    self.on_deck_selected()
            else:
                print('우노 미선택으로 인한 패널티 부여')
                self.game.can_uno_penalty = True
                self.on_deck_selected()
    
    def check_plus_skill(self):
        if self.game.skill_plus_cnt != 0:
            self.on_deck_selected()

    def run_events(self, events):
        if not self.game.is_started:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.run_key_event(event.key)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.run_click_event(pygame.mouse.get_pos())

    def run_key_event(self, key):
        if self.game.is_game_over():
            self.game_over_dialog.run_key_event(key)

        elif key == pygame.K_ESCAPE:
            self.toggle_escape_dialog()


        if self.escape_dialog.enabled:  # 일시정지 다이얼로그
            self.escape_dialog.run_key_event(key)
        elif self.select_color_enabled and self.game.board_player_index == self.game.current_player_index:
            self.card_board.run_slect_color_key_event(key)
        elif self.card_select_enabled:  #
            self.card_board.run_my_cards_select_key_event(key)
        elif self.players_layout.select_enabled:
            self.players_layout.run_select_key_event(key)

        if self.game.uno_enabled:
            self.board.run_uno_key_event(key)

    # 클릭 이벤트
    def run_click_event(self, pos):

        if self.game.is_game_over():
            self.game_over_dialog.run_click_event(None)

        elif self.escape_dialog.enabled:
            self.escape_dialog.run_click_event(pos)

        elif self.select_color_enabled and self.game.board_player_index == self.game.current_player_index:
            self.card_board.run_select_color_click_event(pos)

        elif self.card_select_enabled:
            self.board.run_deck_click_event(pos)
            self.card_board.run_board_cards_select_click_event(pos)

        elif self.players_layout.select_enabled:
            self.players_layout.run_select_click_event(pos)

        # 우노 버튼 클릭 이벤트
        if self.game.uno_enabled:
            self.board.run_uno_click_event(pos)

    # 카드 선택 분기
    def on_card_selected(self, idx):
        hands = self.game.get_board_player().hands
        card = hands[idx]
        # 유효성 확인
        if self.game.verify_new_card(card):
            self.screen_controller.play_effect()
            self.animate_board_player_to_current_card_enabled = True

            # 제출할 카드 저장
            self.board_player_to_current_card_idx = idx

            # 이동 애니메이션
            start_x, start_y = self.card_board.card_rects[idx].topleft
            end_x, end_y = self.board.current_card_rect.topleft

            surface = get_card(card, 2)
            rect = surface.get_rect()
            rect.topleft = start_x, start_y

            self.animate_controller.start(surface, rect, start_x, start_y, end_x, end_y)

    # 에러 방지를 위한 함수
    def resolve_error(self):
        # 보드 카드 이전 인덱스 초과 시 처리
        if self.my_cards_selected_index >= len(self.game.get_board_player().hands):
            self.my_cards_selected_index -= 1

    # 덱 선택
    def on_deck_selected(self):
        self.screen_controller.play_effect()
        self.animate_deck_to_player_enabled = True

        self.set_animate_view_to_card_back()
        
        # 출발지 지정
        start_x, start_y = self.animate_view_rect.topleft

        # 목적지 지정
        if self.game.can_uno_penalty:
            # 이전 플레이어 목적지 지정
            if self.game.previous_player_index == self.game.board_player_index:
                self.set_board_destination()
            else:
                player_rect = self.players_layout.players[self.game.previous_player_index - 1]
                self.animate_destination_x, self.animate_destination_y = player_rect.topleft
        elif self.game.skill_plus_cnt > 0:
            # 다음 플레이어 목적지 지정
            if self.game.next_player_index == self.game.board_player_index:
                self.set_board_destination()
            else:
                player_rect = self.players_layout.players[self.game.next_player_index - 1]
                self.animate_destination_x, self.animate_destination_y = player_rect.topleft
        else:
            # 현재 플레이어 목적지 지정
            if self.game.current_player_index == self.game.board_player_index:
                self.set_board_destination()
            else:
                player_rect = self.players_layout.players[self.game.current_player_index - 1]
                self.animate_destination_x, self.animate_destination_y = player_rect.topleft

        # 애니메이션 시작
        self.animate_controller.start(
            self.animate_view, 
            self.animate_view_rect, 
            start_x, 
            start_y,
            self.animate_destination_x, self.animate_destination_y
        )

    def set_animate_view_to_card_back(self):
        self.animate_view = get_card_back(MY_BOARD_CARD_PERCENT)
        self.animate_view_rect = get_center_rect(self.animate_view, self.board.background_rect,
                                                 -self.animate_view.get_width() // MY_BOARD_CARD_PERCENT - get_medium_margin())

    # 목적지 지정
    def set_board_destination(self):
        self.animate_destination_x, self.animate_destination_y = self.card_board.next_card_start_x, self.card_board.next_card_start_y
        if self.card_board.next_card_start_x + (
                get_card_width(MY_BOARD_CARD_PERCENT) // 1 + get_extra_small_margin()) + get_card_width(
            MY_BOARD_CARD_PERCENT) >= self.board.background_rect.width:
            self.animate_destination_y -= get_card_height(MY_BOARD_CARD_PERCENT) + get_extra_small_margin()
            self.animate_destination_x = get_small_margin()
        else:
            self.animate_destination_x = self.card_board.next_card_start_x + (
                    get_card_width(MY_BOARD_CARD_PERCENT) // 1 + get_extra_small_margin())

    def run_computer(self):
        if self.game.uno_enabled and not self.game.uno_clicked:
            if time.time() - self.game.turn_start_time >= Computer.UNO_DELAY:
                self.game.uno_clicked = True
                self.game.uno_clicked_player_index = random.randint(1, len(self.game.players) - 1)  # 랜덤 컴퓨터가 우노 버튼 클릭

        if type(self.game.get_current_player()) is Computer:

            # 컴퓨터 딜레이
            if time.time() - self.game.turn_start_time < Computer.DELAY:
                return

            computer = self.game.get_current_player()

            if self.select_color_enabled:
                colors = list(COLOR_SET.keys())
                color = random.choice(colors)
                self.game.current_color = color
                self.game.next_turn()
                return

            self.to_computer_play_idx = computer.to_play(self.game)

            if self.game is GameA:
                self.to_computer_play_idx = self.game.get_combo()

            if self.to_computer_play_idx is not None:
                self.screen_controller.play_effect()
                self.animate_current_player_to_current_card_enabled = True

                # 이동 애니메이션

                player_rect = self.players_layout.players[self.game.current_player_index - 1]

                start_x, start_y = player_rect.topleft
                end_x, end_y = self.board.current_card_rect.topleft

                surface = get_card_back(2)
                rect = surface.get_rect()
                rect.topleft = start_x, start_y

                self.animate_controller.start(surface, rect, start_x, start_y, end_x, end_y)
            else:
                # 낼 카드 없을 떄
                self.on_deck_selected()