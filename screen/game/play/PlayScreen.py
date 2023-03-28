from __future__ import annotations
from util.globals import *
from screen.animate.animate import AnimateController
from screen.game.play.section.board import Board
from screen.game.play.section.cardboard import CardBoard
import time

class PlayScreen:

    def __init__(self, screen_controller):

        self.game = screen_controller.game

        self.screen_controller = screen_controller
        self.animate_controller = AnimateController()

        self.stop_timer_enabled = False
        self.deck_select_enabled = False
        self.animate_deck_to_player_enabled = False
        self.animate_board_player_to_current_card_enabled = False

        self.init_game()

        self.init_my_cards_layout(self.screen_controller.screen)

        self.init_players_layout(self.screen_controller.screen)
        self.init_escape_dialog(self.screen_controller.screen)

        self.board = Board(self).init(self.screen_controller.screen.get_width() - self.players_layout_width,
                                      self.screen_controller.screen.get_height() - self.my_cards_layout_height)
        self.card_board = CardBoard(self).init(self.board.background_rect.width, self.my_cards_layout_height)

    # 타이머 일시정지
    def pause_timer(self):
        self.stop_timer_enabled = True
        self.pause_temp_time = time.time()

    def continue_timer(self):
        self.stop_timer_enabled = False

    # 게임 시작 시 초기화 필요한 변수
    def init_game(self):
        self.game.turn_start_time = time.time()

    # 나의 카드 레이아웃 초기화
    def init_my_cards_layout(self, screen):
        self.my_cards_layout_height = screen.get_height() // 3

        self.my_cards_select_enabled = False  # 카드 선택 가능 상태
        self.my_cards_selected_index = 0
        self.cards_line_size = 0  # 한 줄 당 카드 개수

    # 플레이어 레이아웃 초기화
    def init_players_layout(self, screen):

        self.players_selected_index = 1  # TODO: 유동적으로 수정
        self.players_select_enabled = False  # TODO: 플레이어 선택 가능 상태

        self.players_layout_width = 200
        self.player_layout_height = (screen.get_height() - get_small_margin() * 6) // 5

    # 일시정지 다이얼로그 초기화
    def init_escape_dialog(self, screen):
        self.escape_dialog_enabled = False

        self.escape_dialog_width = 500
        self.escape_dialog_height = 300

        self.escape_menu_index = 0
        self.esacpe_menus = [
            {'text': '설정', 'view': None, 'rect': None,
             'action': lambda: self.screen_controller.set_screen(TYPE_SETTING)},
            {'text': '종료', 'view': None, 'rect': None, 'action': lambda: (
                self.init(),
                self.screen_controller.set_screen(TYPE_START)
            )
             }
        ]

    # 초기화 함수 (게임 종료 후 다시 들어왔을 때 호출)
    def init(self):
        self.escape_dialog_enabled = False
        self.escape_menu_index = 0

    # 다이얼로그 표시 상태 변경
    def toggle_escape_dialog(self):
        self.escape_dialog_enabled = not self.escape_dialog_enabled

        # 일시정지 시간 처리
        if self.escape_dialog_enabled:
            self.pause_timer()
        else:
            self.continue_timer()

    # 플레이어 선택 상태 변경
    def toggle_players_select(self):
        self.players_select_enabled = not self.players_select_enabled

    # 모든 View
    def draw(self, screen):
        screen.fill(COLOR_WHITE)
        self.check_time()
        if self.game.is_game_over():
            print("게임 종료")
            print(self.game.get_winner().name)

        self.resolve_error()

        self.board.draw(screen, self.game.current_card)

        self.card_board.draw(screen)

        self.draw_players_layout(screen, self.game.players)

        if self.animate_deck_to_player_enabled:
            if self.animate_controller.enabled:
                self.pause_timer()
                self.animate_controller.draw(screen)
            else:
                self.game.draw()  # 애니메이션 종료 후 한장 가져옴
                self.animate_deck_to_player_enabled = False

                # 일시정해 해제
                self.continue_timer()

                # 턴 전환
                self.game.next_turn()


        # 카드 제출 애니메이션
        elif self.animate_board_player_to_current_card_enabled:
            if self.animate_controller.enabled:
                self.pause_timer()
                self.animate_controller.draw(screen)

            # 애니메이션 종료 시 호출
            else:
                # 한 장 제출
                self.game.play(self.board_player_to_current_card_idx)
                self.animate_board_player_to_current_card_enabled = False
                self.continue_timer()

        if self.escape_dialog_enabled:
            self.draw_escpe_dialog_layout(screen)

    def check_time(self):
        if self.stop_timer_enabled:
            current_time = time.time()
            self.game.turn_start_time = self.game.turn_start_time + (current_time - self.pause_temp_time)
            self.pause_temp_time = current_time

        elif (time.time() - self.game.turn_start_time) > self.game.turn_time:
            # 시간 내 미선택 시 카드 드로우
            self.on_deck_selected()

        self.check_my_turn()

    def check_my_turn(self):
        self.my_cards_select_enabled = self.game.board_player_index == self.game.current_player_index

    # 일시정지 다이얼로그 레이아웃
    def draw_escpe_dialog_layout(self, screen):
        # background solid
        self.escape_box = pygame.draw.rect(screen, COLOR_WHITE, (
        (screen.get_width() - self.escape_dialog_width) // 2, (screen.get_height() - self.escape_dialog_height) // 2,
        self.escape_dialog_width, self.escape_dialog_height))
        # background outline
        pygame.draw.rect(screen, COLOR_BLACK, (
        (screen.get_width() - self.escape_dialog_width) // 2, (screen.get_height() - self.escape_dialog_height) // 2,
        self.escape_dialog_width, self.escape_dialog_height), 1)

        title = get_large_font().render("일시정지", True, COLOR_BLACK)
        title_rect = get_rect(title, screen.get_width() // 2, self.escape_box.y + get_medium_margin())
        screen.blit(title, title_rect)

        self.draw_esacpe_menu(screen)

    # 일시정지 메뉴
    def draw_esacpe_menu(self, screen):
        for index, menu in enumerate(self.esacpe_menus):
            text = get_medium_font().render(menu['text'], True,
                                            COLOR_GRAY if index != self.escape_menu_index else COLOR_BLACK)
            rect = get_rect(text, screen.get_width() // 2, screen.get_height() // 2 + text.get_height() * index)
            menu.update({'view': text, 'rect': rect})
            screen.blit(text, rect)

    # 플레이어 목록 레이아웃
    def draw_players_layout(self, screen, players):
        self.players_layout = pygame.draw.rect(screen, COLOR_GRAY, (
        screen.get_width() - self.players_layout_width, 0, self.players_layout_width, screen.get_height()))
        self.draw_player(screen, players)

    # 플레이어
    def draw_player(self, screen, players):

        self.player_layout_list = []
        temp_player_layout_list = []

        cnt = 0
        for idx, player in enumerate(players):
            # 보드 플레이어 제외
            if idx != self.game.board_player_index:
                # 배경
                player_layout = pygame.draw.rect(screen, COLOR_PLAYER, (self.players_layout.left + get_small_margin(),
                                                                        get_small_margin() + (
                                                                                    self.player_layout_height + get_small_margin()) * cnt,
                                                                        self.players_layout.width - get_small_margin() * 2,
                                                                        self.player_layout_height))
                temp_player_layout_list.append(player_layout)

                # 선택된 플레이어 하이라이트
                if self.players_select_enabled and idx == self.players_selected_index:
                    # 투명 색상 적용
                    surface = pygame.Surface(
                        (self.players_layout.width - get_small_margin() * 2, self.player_layout_height),
                        pygame.SRCALPHA)
                    surface.fill(COLOR_TRANSPARENT_WHITE)
                    screen.blit(surface, (self.players_layout.left + get_small_margin(),
                                          get_small_margin() + (self.player_layout_height + get_small_margin()) * cnt))

                # 현재 플레이어 스트로크
                if idx == self.game.current_player_index:
                    pygame.draw.rect(screen, COLOR_RED, (self.players_layout.left + get_small_margin(),
                                                         get_small_margin() + (
                                                                     self.player_layout_height + get_small_margin()) * cnt,
                                                         self.players_layout.width - get_small_margin() * 2,
                                                         self.player_layout_height), 2)
                    self.draw_player_timer(screen, player_layout)

                # 카드
                self.draw_cards(screen, player_layout, player.hands)

                cnt += 1

        self.player_layout_list = temp_player_layout_list

    # 플레이어 상단 타이머 표시
    def draw_player_timer(self, screen, parent):
        timer_text = get_small_font().render(
            str(int(self.game.turn_time + 1 - (time.time() - self.game.turn_start_time))), True, COLOR_RED)
        timer_rect = timer_text.get_rect().topleft = (
        parent.right - timer_text.get_width() - get_small_margin(), parent.top)
        screen.blit(timer_text, timer_rect)

    # 카드
    def draw_cards(self, screen, player_layout, cards):
        for idx, card in enumerate(cards):
            card_layout = pygame.image.load('./resource/card_back.png')
            card_layout = pygame.transform.scale(card_layout, (get_card_width(), get_card_height()))
            card_rect = card_layout.get_rect().topleft = (
            player_layout.left + get_extra_small_margin() + (card_layout.get_width() // 2) * idx,
            player_layout.bottom - card_layout.get_height() - get_extra_small_margin())

            # 카드가 보드 넘어가는 경우 표시하지 않음
            if card_rect[0] + get_card_width() <= player_layout.right:
                screen.blit(card_layout, card_rect)

        # 카드 개수 표시 (45 변수로 설정해야 함)
        txt_card_cnt = get_small_font().render(str(len(cards)), True, COLOR_BLACK)
        txt_card_cnt_rect = txt_card_cnt.get_rect().topleft = (player_layout.left + get_extra_small_margin(),
                                                               player_layout.bottom - get_card_height() - txt_card_cnt.get_height() - get_extra_small_margin())
        screen.blit(txt_card_cnt, txt_card_cnt_rect)

    # 이벤트 처리 함수
    def run_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.process_key_event(event.key)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.process_click_event(pygame.mouse.get_pos())

    # 키보드 입력 이벤트 처리
    def process_key_event(self, key):

        if key == pygame.K_ESCAPE:
            self.toggle_escape_dialog()

        # 일시정지
        if self.escape_dialog_enabled:
            self.run_esacpe_key_event(key)

        # 카드 선택
        elif self.my_cards_select_enabled:
            self.card_board.run_my_cards_select_key_event(key)

        # 플레이어 선택
        elif self.players_select_enabled:
            self.run_players_select_key_event(key)

    # 일시정지 메뉴 키 이벤트
    def run_esacpe_key_event(self, key):
        if key == pygame.K_UP:
            self.escape_menu_index = (self.escape_menu_index - 1) % len(self.esacpe_menus)
        elif key == pygame.K_DOWN:
            self.escape_menu_index = (self.escape_menu_index + 1) % len(self.esacpe_menus)
        elif key == pygame.K_RETURN:
            self.esacpe_menus[self.escape_menu_index]['action']()

    # 플레이어 선택 키 이벤트
    def run_players_select_key_event(self, key):
        if key == pygame.K_UP:
            self.players_selected_index = (self.players_selected_index - 1) % len(self.game.players)
            # 보드 플레이어 제와
            if self.players_selected_index == self.game.board_player_index:
                self.players_selected_index = (self.players_selected_index - 1) % len(self.game.players)
        elif key == pygame.K_DOWN:
            self.players_selected_index = (self.players_selected_index + 1) % len(self.game.players)
            # 보드 플레이어 제외
            if self.players_selected_index == self.game.board_player_index:
                self.players_selected_index = (self.players_selected_index + 1) % len(self.game.players)
        elif key == pygame.K_RETURN:
            self.on_player_selected(self.players_selected_index)

    # 클릭 이벤트
    def process_click_event(self, pos):

        # 로비 화면 이벤트
        if self.lobby.enabled:
            self.lobby.run_click_event(pos)
            return

        if self.escape_dialog_enabled:
            self.run_esacpe_click_event(pos)

        elif self.my_cards_select_enabled:
            self.board.run_deck_click_event(pos)
            self.card_board.run_board_cards_select_click_event(pos)

        elif self.players_select_enabled:
            self.run_players_select_click_event(pos)

    # 일시정지 메뉴 클릭 이벤트
    def run_esacpe_click_event(self, pos):
        for menu in self.esacpe_menus:
            if menu['rect'] and menu['rect'].collidepoint(pos):
                menu['action']()

    # 플레이어 선택 클릭 이벤트
    def run_players_select_click_event(self, pos):
        for idx, player in enumerate(self.player_layout_list):
            if player.collidepoint(pos):
                # 보드 플레이어 제외
                real_idx = idx
                if idx >= self.game.board_player_index:
                    real_idx += 1
                self.on_player_selected(real_idx)

    # 플레이어 선택 종류 분기
    def on_player_selected(self, idx):
        print(f"{idx}번 플레이어 선택")

    # 카드 선택 분기
    def on_card_selected(self, idx):

        hands = self.game.get_board_player().hands
        card = hands[idx]
        # 유효성 확인
        if self.game.verify_new_card(card):
            self.animate_board_player_to_current_card_enabled = True

            # 제출할 카드 저장
            self.board_player_to_current_card_idx = idx

            # 이동 애니메이션
            start_x, start_y = self.card_board.card_rects[idx].topleft
            end_x, end_y = self.board.current_card_rect.topleft

            surface = get_card(card, 2)
            rect = surface.get_rect()
            rect.topleft = start_x, start_y

            self.animate_controller.init_pos(surface, rect, start_x, start_y, end_x, end_y)

    # 에러 방지를 위한 함수
    def resolve_error(self):
        # 보드 카드 이전 인덱스 초과 시 처리
        if self.my_cards_selected_index >= len(self.game.get_board_player().hands):
            self.my_cards_selected_index -= 1

    # 덱 선택
    def on_deck_selected(self):
        self.animate_deck_to_player_enabled = True

        self.animate_view = pygame.image.load('./resource/card_back.png')  # TODO: 카드 수정
        self.animate_view = pygame.transform.scale(self.animate_view, (
        get_card_width() * MY_BOARD_CARD_PERCENT, get_card_height() * MY_BOARD_CARD_PERCENT))

        self.animate_view_rect = get_center_rect(self.animate_view, self.board.background_rect,
                                                 -self.animate_view.get_width() // MY_BOARD_CARD_PERCENT - get_medium_margin())
        start_x, start_y = self.animate_view_rect.topleft

        self.animate_destination_x, self.animate_destination_y = self.card_board.next_card_start_x, self.card_board.next_card_start_y
        if self.card_board.next_card_start_x + (
                get_card_width(MY_BOARD_CARD_PERCENT) // 1 + get_extra_small_margin()) + get_card_width(
                MY_BOARD_CARD_PERCENT) >= self.board.background_rect.width:
            self.animate_destination_y -= get_card_height(MY_BOARD_CARD_PERCENT) + get_extra_small_margin()
            self.animate_destination_x = get_small_margin()
        else:
            self.animate_destination_x = self.card_board.next_card_start_x + (
                        get_card_width(MY_BOARD_CARD_PERCENT) // 1 + get_extra_small_margin())

        self.animate_controller.init_pos(self.animate_view, self.animate_view_rect, start_x, start_y,
                                         self.animate_destination_x, self.animate_destination_y)