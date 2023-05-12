from __future__ import annotations
from typing import TYPE_CHECKING

import time

import pygame

from game.model.player import Player
from util.globals import *

if TYPE_CHECKING:
    from game.game import UnoGame


class PlayersLayout:
    def __init__(self, play_screen):

        # 의존성 객체
        self.play_screen = play_screen
        self.screen_controller = play_screen.screen_controller
        self.game = None

        self.width = 200
        self.left = 0

        self.player_height = 0

        self.selected_idx = 1
        self.select_enabled = False

        self.players = []

    def draw(self, screen: pygame.Surface):
        self.game = self.play_screen.game

        self.player_height = (screen.get_height() - get_small_margin() * 6) // 5

        self.draw_background(screen)
        self.draw_player(screen, self.game.players)

    def draw_background(self, screen: pygame.Surface):
        pygame.draw.rect(screen, COLOR_GRAY, (screen.get_width() - self.width, 0, self.width, screen.get_height()))

    def draw_player(self, screen: pygame.Surface, players: list[Player]):

        self.left = screen.get_width() - self.width

        self.players = []
        temp_player_layouts = []
        cnt = 0
        for idx, player in enumerate(players):
            # 보드 플레이어 제외
            if idx != self.game.board_player_index:
                # 배경
                player_layout = pygame.draw.rect(screen, COLOR_PLAYER, (self.left + get_small_margin(),
                                                                        get_small_margin() + (
                                                                                self.player_height + get_small_margin()) * cnt,
                                                                        self.width - get_small_margin() * 2,
                                                                        self.player_height))
                temp_player_layouts.append(player_layout)

                # 플레이어 이름
                name = get_small_font().render(player.name, True, COLOR_BLACK)
                name_rect = get_top_center_rect(name, player_layout, x=-name.get_width() // 2)
                screen.blit(name, name_rect)

                # 선택된 플레이어 하이라이트
                if self.select_enabled and idx == self.selected_idx:
                    # 투명 색상 적용
                    surface = pygame.Surface(
                        (self.width - get_small_margin() * 2, self.player_height),
                        pygame.SRCALPHA)
                    surface.fill(COLOR_TRANSPARENT_WHITE)
                    screen.blit(surface, (self.left + get_small_margin(),
                                          get_small_margin() + (self.player_height + get_small_margin()) * cnt))




                # 현재 플레이어 스트로크
                if idx == self.game.current_player_index:
                    pygame.draw.rect(screen, COLOR_RED, (self.left + get_small_margin(),
                                                         get_small_margin() + (
                                                                 self.player_height + get_small_margin()) * cnt,
                                                         self.width - get_small_margin() * 2,
                                                         self.player_height), 2)
                    self.draw_timer(screen, player_layout)

                # 카드
                self.draw_cards(screen, player_layout, player.hands)

                # 스킵된 플레이어 표시
                skipped = self.game.get_skipped_player_indexs()
                for skipped_index in skipped:
                    if idx == skipped_index:
                        surface = pygame.Surface(
                            (self.width - get_small_margin() * 2, self.player_height),
                            pygame.SRCALPHA)
                        surface.fill(COLOR_TRANSPARENT_RED)
                        screen.blit(surface, (self.left + get_small_margin(),
                                              get_small_margin() + (self.player_height + get_small_margin()) * cnt))

                cnt += 1

        self.players = temp_player_layouts

    def draw_timer(self, screen, parent):
        time_text = str(int(self.game.turn_time + 1 - (time.time() - self.game.turn_start_time)))
        timer_text = get_small_font().render(time_text, True, COLOR_RED)
        timer_rect = timer_text.get_rect().topleft = (
        parent.right - timer_text.get_width() - get_small_margin(), parent.top)
        screen.blit(timer_text, timer_rect)

    def draw_cards(self, screen, player_layout, cards):
        for idx, card in enumerate(cards):
            card_layout = pygame.image.load('./resource/card_back.png')
            card_layout = pygame.transform.scale(card_layout, (get_card_width(), get_card_height()))
            card_rect = card_layout.get_rect().topleft = (
                player_layout.left + get_extra_small_margin() + (card_layout.get_width() // 2) * idx,
                player_layout.bottom - card_layout.get_height() - get_extra_small_margin()
            )

            # 카드가 보드 넘어가는 경우 표시하지 않음
            if card_rect[0] + get_card_width() <= player_layout.right:
                screen.blit(card_layout, card_rect)

        # 카드 개수 표시 (45 변수로 설정해야 함)
        txt_card_cnt = get_small_font().render(str(len(cards)), True, COLOR_BLACK)
        txt_card_cnt_rect = txt_card_cnt.get_rect().topleft = (player_layout.left + get_extra_small_margin(),
                                                               player_layout.bottom - get_card_height() - txt_card_cnt.get_height() - get_extra_small_margin())
        screen.blit(txt_card_cnt, txt_card_cnt_rect)


    def run_select_key_event(self, key):
        if key == pygame.K_UP:
            self.selected_idx = (self.selected_idx - 1) % len(self.game.players)
            # 보드 플레이어 제외
            if self.selected_idx == self.game.board_player_index:
                self.selected_idx = (self.selected_idx - 1) % len(self.game.players)
        elif key == pygame.K_DOWN:
            self.selected_idx = (self.selected_idx + 1) % len(self.game.players)
            # 보드 플레이어 제외
            if self.selected_idx == self.game.board_player_index:
                self.selected_idx = (self.selected_idx + 1) % len(self.game.players)
        elif key == pygame.K_RETURN:
            self.on_player_selected(self.selected_idx)

    def run_select_click_event(self, pos):
        for idx, player in enumerate(self.player_layout_list):
            if player.collidepoint(pos):
                # 보드 플레이어 제외
                real_idx = idx
                if idx >= self.game.board_player_index:
                    real_idx += 1
                self.on_player_selected(real_idx)

    def on_player_selected(self, idx):
        print(f"{idx}번 플레이어 선택")