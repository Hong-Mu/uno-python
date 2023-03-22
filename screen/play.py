from __future__ import annotations
from typing import TYPE_CHECKING
from util.globals import *
from screen.animate.animate import AnimateController
from screen.section.board import Board
import time

if TYPE_CHECKING:
    from game.game import UnoGame

class PlayScreen:

    def __init__(self, controller):
        self.ctr = controller
        self.game: UnoGame = controller.game
        self.animate_controller = AnimateController()

        self.start_time = time.time() # 게임 시작 시간

        # 턴 시간 (초단위)
        self.turn_time = 5

        self.animate_deck_to_player_enabled = False

        self.init_game()

        self.init_my_cards_layout(self.ctr.screen)
        self.init_board_layout(self.ctr.screen)
        self.init_players_layout(self.ctr.screen)
        self.init_escape_dialog(self.ctr.screen)

        self.board = Board(self).init(self.ctr.screen.get_width() - self.players_layout_width, self.ctr.screen.get_height() - self.my_cards_layout_height)


    # 게임 시작 시 초기화 필요한 변수
    def init_game(self):
        self.turn_start_time = time.time()

    # 나의 카드 레이아웃 초기화
    def init_my_cards_layout(self, screen):
        self.my_cards_layout_height = screen.get_height() // 3

        self.my_cards_select_enabled = False # 카드 선택 가능 상태
        self.my_cards_selected_index = 0
        self.cards_line_size = 0 # 한 줄 당 카드 개수

    # 보드 레이아웃 초기화
    def init_board_layout(self, screen):
        self.deck_select_enabled = False

    # 플레이어 레이아웃 초기화
    def init_players_layout(self, screen):

        self.players_selected_index = 1 # TODO: 유동적으로 수정
        self.players_select_enabled = True # TODO: 플레이어 선택 가능 상태

        self.players_layout_width = 200
        self.player_layout_height = (screen.get_height() - get_small_margin() * 6) // 5

    # 일시정지 다이얼로그 초기화
    def init_escape_dialog(self, screen):
        self.escape_dialog_enabled = False

        self.escape_dialog_width = 500
        self.escape_dialog_height = 300

        self.escape_menu_index = 0 
        self.esacpe_menus = [
            {'text': '설정', 'view': None, 'rect': None, 'action': lambda: self.ctr.set_screen(TYPE_SETTING) }, 
            {'text': '종료', 'view': None, 'rect': None, 'action': lambda: (
                    self.init(),
                    self.ctr.set_screen(TYPE_START) 
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

    # 플레이어 선택 상태 변경
    def toggle_players_select(self):
        self.players_select_enabled = not self.players_select_enabled

    # 모든 View
    def draw(self, screen):
        screen.fill(COLOR_WHITE)
        self.check_time()

        self.board.draw(screen)
        
        self.draw_my_cards_layout(screen, self.game.get_current_player()) # TODO: 추가

        self.draw_players_layout(screen, self.game.players)

        if self.animate_deck_to_player_enabled:
            if self.animate_controller.enabled:
                self.animate_controller.draw(screen)
            else:
                self.game.draw()
                self.animate_deck_to_player_enabled = False

        if self.escape_dialog_enabled:
            self.draw_escpe_dialog_layout(screen)

    def check_time(self):
        if self.escape_dialog_enabled:
            current_time = time.time()
            self.turn_start_time = self.turn_start_time + (current_time - self.pause_temp_time)
            self.pause_temp_time = current_time
            
        elif (time.time() - self.turn_start_time) > self.turn_time:
            self.game.current_player_index = (self.game.current_player_index + 1) % len(self.game.players)
            self.turn_start_time = time.time()
        
        self.check_my_turn()

    def check_my_turn(self):
        self.my_cards_select_enabled = self.game.board_player_index == self.game.current_player_index

    # 일시정지 다이얼로그 레이아웃
    def draw_escpe_dialog_layout(self, screen):
        # background solid
        self.escape_box = pygame.draw.rect(screen, COLOR_WHITE, ((screen.get_width() - self.escape_dialog_width) // 2, (screen.get_height() - self.escape_dialog_height) // 2, self.escape_dialog_width, self.escape_dialog_height))
        # background outline
        pygame.draw.rect(screen, COLOR_BLACK, ((screen.get_width() - self.escape_dialog_width) // 2, (screen.get_height() - self.escape_dialog_height) // 2, self.escape_dialog_width, self.escape_dialog_height), 1)

        title = get_large_font().render("일시정지", True, COLOR_BLACK)
        title_rect = get_rect(title, screen.get_width() // 2, self.escape_box.y + get_medium_margin())
        screen.blit(title, title_rect)

        self.draw_esacpe_menu(screen)
    
    # 일시정지 메뉴
    def draw_esacpe_menu(self, screen):
        for index, menu in enumerate(self.esacpe_menus):
            text = get_medium_font().render(menu['text'], True, COLOR_GRAY if  index != self.escape_menu_index else COLOR_BLACK)
            rect = get_rect(text, screen.get_width() // 2, screen.get_height() // 2 + text.get_height() * index)
            menu.update({'view': text, 'rect': rect})
            screen.blit(text, rect)

    # 나의 카드 레이아웃
    def draw_my_cards_layout(self, screen, player):
        # 배경
        self.my_cards_layout = pygame.draw.rect(screen, COLOR_PLAYER, (0, self.board.background_rect.bottom, self.board.background_rect.right, self.my_cards_layout_height))

        # 나의 카드
        self.draw_my_cards(screen, player.hands)

        # 나의 차례 스트로크
        if self.game.board_player_index == self.game.current_player_index:
            self.draw_my_board_timer(screen)
            pygame.draw.rect(screen, COLOR_RED, (0, self.board.background_rect.bottom, self.board.background_rect.right, self.my_cards_layout_height), 2)

    # 나의 보드 위 타이머 표시
    def draw_my_board_timer(self, screen):
        timer_text = get_medium_font().render(str(int(self.turn_time + 1 - (time.time() - self.turn_start_time))), True, COLOR_RED)
        timer_rect = timer_text.get_rect().topleft = (self.my_cards_layout.right - timer_text.get_width() - get_small_margin(), self.my_cards_layout.top)
        screen.blit(timer_text, timer_rect)

    # 나의 카드
    def draw_my_cards(self, screen, cards):

        # 카드 레이아웃 (충돌 감지 목적)
        self.card_list = []
        temp_card_list = []

        card_percent = 1.5 # 카드 배율
        card_overlap_percent = 1 

        # 카드 시작 좌표
        card_start_x, self.next_card_start_y = get_extra_small_margin(), screen.get_height() - get_card_height() * card_percent - get_extra_small_margin()
        temp_idx = 0

        for idx, card in enumerate(cards):
            card_image = pygame.image.load('./resource/card_back.png')
            card_image = pygame.transform.scale(card_image, (get_card_width() * card_percent, get_card_height() * card_percent))

            # 카드가 보드 넘어가는 경우 위로 쌓음
            if card_start_x + (card_image.get_width() // card_overlap_percent + get_extra_small_margin()) * (idx - temp_idx) + card_image.get_width() >= self.board.background_rect.width:
                self.next_card_start_y -= card_image.get_height() + get_extra_small_margin()

                if temp_idx == 0:
                    self.cards_line_size = idx
                
                temp_idx = idx
        

            # 카드 시작 위치
            self.next_card_start_x = card_start_x + (card_image.get_width() // card_overlap_percent + get_extra_small_margin()) * (idx - temp_idx)

            card_rect = card_image.get_rect().topleft = (self.next_card_start_x, self.next_card_start_y)
            card_layout = screen.blit(card_image, card_rect)
            temp_card_list.append(card_layout)

            # 선택된 카드 하이라이트
            if self.my_cards_select_enabled and not self.deck_select_enabled and idx == self.my_cards_selected_index:
                # 투명 색상 적용
                surface = pygame.Surface((card_layout.width, card_layout.height), pygame.SRCALPHA)
                surface.fill(COLOR_TRANSPARENT_WHITE)
                screen.blit(surface, (card_layout.left, card_layout.top))

        self.card_list = temp_card_list


        # 카드 개수 표시
        txt_card_cnt = get_medium_font().render(str(len(cards)), True, COLOR_BLACK)
        txt_card_cnt_rect = txt_card_cnt.get_rect().topleft = self.my_cards_layout.topleft
        screen.blit(txt_card_cnt, txt_card_cnt_rect)

    # 플레이어 목록 레이아웃
    def draw_players_layout(self, screen, players):
        self.players_layout = pygame.draw.rect(screen, COLOR_GRAY, (screen.get_width() - self.players_layout_width, 0, self.players_layout_width, screen.get_height()))
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
                player_layout = pygame.draw.rect(screen, COLOR_PLAYER, (self.players_layout.left + get_small_margin(), get_small_margin() + (self.player_layout_height + get_small_margin()) * cnt, self.players_layout.width - get_small_margin() * 2, self.player_layout_height))
                temp_player_layout_list.append(player_layout)

                # 선택된 플레이어 하이라이트
                if self.players_select_enabled and idx == self.players_selected_index:
                    # 투명 색상 적용
                    surface = pygame.Surface((self.players_layout.width - get_small_margin() * 2, self.player_layout_height), pygame.SRCALPHA)
                    surface.fill(COLOR_TRANSPARENT_WHITE)
                    screen.blit(surface, (self.players_layout.left + get_small_margin(), get_small_margin() + (self.player_layout_height + get_small_margin()) * cnt))

                # 현재 플레이어 스트로크
                if idx == self.game.current_player_index:
                    pygame.draw.rect(screen, COLOR_RED, (self.players_layout.left + get_small_margin(), get_small_margin() + (self.player_layout_height + get_small_margin()) * cnt, self.players_layout.width - get_small_margin() * 2, self.player_layout_height), 2)
                    self.draw_player_timer(screen, player_layout)

                # 카드
                self.draw_cards(screen, player_layout, player.hands)

                cnt += 1

        self.player_layout_list = temp_player_layout_list

    # 플레이어 상단 타이머 표시
    def draw_player_timer(self, screen, parent):
        timer_text = get_small_font().render(str(int(self.turn_time + 1 - (time.time() - self.turn_start_time))), True, COLOR_RED)
        timer_rect = timer_text.get_rect().topleft = (parent.right - timer_text.get_width() - get_small_margin(), parent.top)
        screen.blit(timer_text, timer_rect)
            
    # 카드
    def draw_cards(self, screen, player_layout, cards):
        for idx, card in enumerate(cards):
            card_layout = pygame.image.load('./resource/card_back.png')
            card_layout = pygame.transform.scale(card_layout, (get_card_width(), get_card_height()))
            card_rect = card_layout.get_rect().topleft = (player_layout.left  + get_extra_small_margin() + (card_layout.get_width() // 2) * idx, player_layout.bottom - card_layout.get_height() - get_extra_small_margin())

            # 카드가 보드 넘어가는 경우 표시하지 않음
            if card_rect[0] + get_card_width() <= player_layout.right:
                screen.blit(card_layout, card_rect)


        # 카드 개수 표시 (45 변수로 설정해야 함)
        txt_card_cnt = get_small_font().render(str(len(cards)), True, COLOR_BLACK)
        txt_card_cnt_rect = txt_card_cnt.get_rect().topleft = (player_layout.left + get_extra_small_margin(), player_layout.bottom - get_card_height() - txt_card_cnt.get_height() - get_extra_small_margin())
        screen.blit(txt_card_cnt, txt_card_cnt_rect)

    # 이벤트 처리 함수
    def process_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.process_key_event(event.key)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.process_click_event(pygame.mouse.get_pos())

    # 키보드 입력 이벤트 처리
    def process_key_event(self, key):
        if key == pygame.K_ESCAPE:
            self.toggle_escape_dialog()

            # 일시정지 시간 처리
            if self.escape_dialog_enabled:
                self.pause_temp_time = time.time() 

        # 일시정지
        if self.escape_dialog_enabled:
            self.run_esacpe_key_event(key)
        
        # 카드 선택
        elif self.my_cards_select_enabled:
            self.run_my_cards_select_key_event(key)

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

    # 카드 선택 키 이벤트
    def run_my_cards_select_key_event(self, key):
        if key == pygame.K_LEFT:
            if not self.deck_select_enabled:
                self.my_cards_selected_index = (self.my_cards_selected_index - 1) % len(self.game.get_board_player().hands)
        elif key == pygame.K_RIGHT:
            if not self.deck_select_enabled:
                self.my_cards_selected_index = (self.my_cards_selected_index + 1) % len(self.game.get_board_player().hands)
        elif key == pygame.K_UP:
            if self.cards_line_size != 0 and self.my_cards_selected_index + self.cards_line_size < len(self.game.get_board_player().hands):
                self.my_cards_selected_index = self.my_cards_selected_index + self.cards_line_size
            else: # 덱 선택
                self.deck_select_enabled = True
        elif key == pygame.K_DOWN:
            # 다시 카드 선택으로 돌아옴
            if self.deck_select_enabled:
                self.deck_select_enabled = False
            
            elif self.cards_line_size != 0 and self.my_cards_selected_index - self.cards_line_size >= 0:
                self.my_cards_selected_index = self.my_cards_selected_index - self.cards_line_size
        elif key == pygame.K_RETURN:
            if self.deck_select_enabled:
                self.on_deck_selected()
            else:
                self.on_card_selected(self.my_cards_selected_index)

    # 클릭 이벤트
    def process_click_event(self, pos):
        if self.escape_dialog_enabled:
            self.run_esacpe_click_event(pos)

        elif self.my_cards_select_enabled:
            self.run_cards_select_click_event(pos)
        
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

    # 카드 선택 클릭 이벤트
    def run_cards_select_click_event(self, pos):
        
        if self.board.deck_rect.collidepoint(pos):
            self.on_deck_selected()

        for idx, card in enumerate(self.card_list):
            if card.collidepoint(pos):
                self.on_card_selected(idx)

    # 플레이어 선택 종류 분기
    def on_player_selected(self, idx):
        print(f"{idx}번 플레이어 선택")

    # 카드 선택 분기
    def on_card_selected(self, idx):
        print(f"{idx}번 카드 선택")

    # 덱 선택
    def on_deck_selected(self):
        self.animate_deck_to_player_enabled = True

        self.animate_view = pygame.image.load('./resource/card_back.png') # TODO: 카드 수정
        self.animate_view = pygame.transform.scale(self.animate_view, (get_card_width() * MY_BOARD_CARD_PERCENT, get_card_height() * MY_BOARD_CARD_PERCENT))

        self.animate_view_rect = get_center_rect(self.animate_view, self.board.background_rect, -self.animate_view.get_width() // MY_BOARD_CARD_PERCENT - get_medium_margin())
        start_x, start_y = self.animate_view_rect.topleft

        self.animate_destination_x, self.animate_destination_y = self.next_card_start_x, self.next_card_start_y
        if self.next_card_start_x + (get_card_width(MY_BOARD_CARD_PERCENT) // 1 + get_extra_small_margin()) + get_card_width(MY_BOARD_CARD_PERCENT) >= self.board.background_rect.width:
            self.animate_destination_y -= get_card_height(MY_BOARD_CARD_PERCENT) + get_extra_small_margin()
            self.animate_destination_x = get_small_margin()
        else:
            self.animate_destination_x = self.next_card_start_x + (get_card_width(MY_BOARD_CARD_PERCENT) // 1 + get_extra_small_margin())
        
        self.animate_controller.init_pos(self.animate_view, self.animate_view_rect, start_x, start_y, self.animate_destination_x, self.animate_destination_y)