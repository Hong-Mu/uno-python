from util.globals import *
import time
import pygame

class CardBoard:
    def __init__(self, play_screen):
        self.play_screen = play_screen

        self.game = None
        self.board = play_screen.board

        self.next_card_start_x = get_extra_small_margin()

        self.color_index = 0
        self.select_colors = [
            {'color': COLOR_SET[CARD_COLOR_RED], 'rect': None, 'type': CARD_COLOR_RED},
            {'color': COLOR_SET[CARD_COLOR_BLUE], 'rect': None, 'type': CARD_COLOR_BLUE},
            {'color': COLOR_SET[CARD_COLOR_GREEN], 'rect': None, 'type': CARD_COLOR_GREEN},
            {'color': COLOR_SET[CARD_COLOR_YELLOW], 'rect': None, 'type': CARD_COLOR_YELLOW},
        ]
    
    def draw(self, screen):
        self.game = self.play_screen.game
        background_height = screen.get_height() // 3

        self.card_width = get_card_width(1.5)
        self.card_height = get_card_height(1.5)
        self.background_rect = pygame.Rect(0, screen.get_height() - background_height, self.board.background_rect.right, background_height)


        pygame.draw.rect(screen, COLOR_PLAYER, self.background_rect)

        name = get_small_font().render(self.game.get_board_player().name, True, COLOR_BLACK)
        name_rect = get_top_center_rect(name, self.background_rect, x=-name.get_width() // 2)
        screen.blit(name, name_rect)

        # 남은 시간 표시
        if self.game.board_player_index == self.game.current_player_index:
            self.timer = get_medium_font().render(str(int(self.game.turn_time + 1 - (time.time() - self.game.turn_start_time))), True, COLOR_RED)
            self.timer_rect = (self.background_rect.right - self.timer.get_width() - get_small_margin(), self.background_rect.top)
            screen.blit(self.timer, self.timer_rect)
            pygame.draw.rect(screen, COLOR_RED, self.background_rect, 2)

        self.draw_my_cards(screen, self.game.get_board_player().hands)
        for idx, rect in enumerate(self.card_rects):
            screen.blit(get_card(self.cards[idx], 1.5), rect)

            # 하이라이트
            if self.play_screen.card_select_enabled and not self.play_screen.deck_select_enabled and idx == self.play_screen.my_cards_selected_index:
                pygame.draw.rect(screen, COLOR_BLACK, rect, 5)

        txt_card_cnt = get_medium_font().render(str(len(self.card_rects)), True, COLOR_BLACK)
        screen.blit(txt_card_cnt, self.background_rect)

        skipped = self.game.get_skipped_player_indexs()
        for skipped_index in skipped:
            print(skipped_index)
            if self.game.board_player_index == skipped_index:
                surface = pygame.Surface(self.background_rect.size, pygame.SRCALPHA)
                surface.fill(COLOR_TRANSPARENT_RED)
                screen.blit(surface, self.background_rect.topleft)

        print(self.play_screen.select_color_enabled)
        if self.play_screen.select_color_enabled and self.game.board_player_index == self.game.current_player_index:
            self.draw_select_color(screen)


    def draw_select_color(self, screen: pygame.Surface):
        size = 50

        surface = pygame.Surface(self.background_rect.size, pygame.SRCALPHA)
        surface.fill(COLOR_TRANSPARENT_WHITE)

        surface_rect = screen.blit(surface, self.background_rect.topleft)

        for idx, color in enumerate(self.select_colors):
            rect = pygame.Rect(0, 0, size, size)
            rect.center = surface_rect.center
            rect.left += (idx - 1.5) * size
            color['rect'] = rect
            pygame.draw.rect(screen, COLOR_SET[color['type']], rect)

            if idx == self.color_index:
                pygame.draw.rect(screen, COLOR_BLACK, rect, 2)



    def run_select_color_click_event(self, pos):
        for color in self.select_colors:
            if color['rect'].collidepoint(pos):
                self.play_screen.update_color(color['type'])

    def run_slect_color_key_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.color_index = (self.color_index + 1) % len(self.select_colors)
        elif event.key == pygame.K_LEFT:
            self.color_index = (self.color_index - 1) % len(self.select_colors)
        elif event.key == pygame.K_RETURN:
            self.play_screen.update_color(self.select_colors[self.color_index]['type'])

    # 나의 카드
    def draw_my_cards(self, screen: pygame.Surface, cards):

        # 카드 레이아웃 (충돌 감지 목적)
        self.cards = cards
        self.card_rects: list[pygame.Rect] = []
        temp_card_rects = []


        # 카드 시작 좌표
        start_x = get_extra_small_margin()
        self.next_card_start_y = screen.get_height() - self.card_height - get_extra_small_margin()

        temp_idx = 0
        self.cards_line_size = 0
        for idx, card in enumerate(cards):

            # 카드가 보드 넘어가는 경우 위로 쌓음
            if start_x + (self.card_width + get_extra_small_margin()) * (idx - temp_idx) + self.card_width >= self.board.background_rect.width:
                self.next_card_start_y -= self.card_height + get_extra_small_margin()

                if temp_idx == 0:
                    self.cards_line_size = idx
                
                temp_idx = idx
        

            # 카드 시작 위치
            self.next_card_start_x = start_x + (self.card_width + get_extra_small_margin()) * (idx - temp_idx)

            card_rect = pygame.Rect(self.next_card_start_x, self.next_card_start_y, self.card_width, self.card_height)
            temp_card_rects.append(card_rect)

        self.card_rects = temp_card_rects

    # 카드 선택 키 이벤트
    def run_my_cards_select_key_event(self, event):
        if self.play_screen.is_animation_running:
            return

        if event.key == pygame.K_LEFT:
            if not self.play_screen.deck_select_enabled:
                self.play_screen.my_cards_selected_index = (self.play_screen.my_cards_selected_index - 1) % len(self.game.get_board_player().hands)
        elif event.key == pygame.K_RIGHT:
            if not self.play_screen.deck_select_enabled:
                self.play_screen.my_cards_selected_index = (self.play_screen.my_cards_selected_index + 1) % len(self.game.get_board_player().hands)
        elif event.key == pygame.K_UP:
            if self.cards_line_size != 0 and self.play_screen.my_cards_selected_index + self.cards_line_size < len(self.game.get_board_player().hands):
                self.play_screen.my_cards_selected_index = self.play_screen.my_cards_selected_index + self.cards_line_size
            else: # 덱 선택
                self.play_screen.deck_select_enabled = True
        elif event.key == pygame.K_DOWN:
            # 다시 카드 선택으로 돌아옴
            if self.play_screen.deck_select_enabled:
                self.play_screen.deck_select_enabled = False
            
            elif self.cards_line_size != 0 and self.play_screen.my_cards_selected_index - self.cards_line_size >= 0:
                self.play_screen.my_cards_selected_index = self.play_screen.my_cards_selected_index - self.cards_line_size
        elif event.key == pygame.K_RETURN:

            if self.play_screen.deck_select_enabled:
                self.play_screen.on_deck_selected()
            else:
                self.play_screen.on_card_selected(self.play_screen.my_cards_selected_index)
        elif event.key == self.play_screen.screen_controller.setting.get(MODE_DECK_KEY):
            self.play_screen.on_deck_selected()

    def run_board_cards_select_click_event(self, pos):
        if self.play_screen.is_animation_running:
            return
        for idx, rect in enumerate(self.card_rects):
            if rect.collidepoint(pos):
                self.play_screen.on_card_selected(idx)