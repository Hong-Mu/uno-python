from __future__ import annotations
from typing import TYPE_CHECKING

from game.model.skill import Skill
from util.globals import *
import time
import pygame

if TYPE_CHECKING:
    from screen.game.play.PlayScreen import PlayScreen
    from game.game import UnoGame
    from screen.ScreenController import ScreenController

class Board:
    def __init__(self, play_screen: PlayScreen):
        self.play_screen = play_screen
        self.game = None

    def draw(self, screen: pygame.Surface):
        self.game = self.play_screen.game
        print("보드")

        current_card = self.game.current_card

        self.background_rect = pygame.Rect((0, 0, screen.get_width() - self.play_screen.players_layout.width, screen.get_height() - screen.get_height() // 3))
        self.color_circle = (self.background_rect.center, self.background_rect.width // 4, 20)

        self.deck = get_card_back(2)
        self.deck_rect = get_center_rect(self.deck, self.background_rect, -self.deck.get_width() // 2 - get_medium_margin())
        self.deck_highlight = pygame.Surface((get_card_width(2), get_card_height(2)), pygame.SRCALPHA)
        self.deck_highlight.fill(COLOR_TRANSPARENT_WHITE)

        # TODO: 삭제
        self.current_card = get_card_back(2)
        self.current_card_rect = get_center_rect(self.current_card, self.background_rect, self.current_card.get_width() // 2 + get_medium_margin())

        pygame.draw.rect(screen, COLOR_BOARD, self.background_rect)
        pygame.draw.circle(screen, CARD_COLOR_SET[self.game.current_color], *self.color_circle)
        screen.blit(self.deck, self.deck_rect)

        if self.play_screen.card_select_enabled and self.play_screen.deck_select_enabled:
            screen.blit(self.deck_highlight, self.deck_rect)

        screen.blit(get_card(current_card, 2), self.current_card_rect)

        self.draw_uno_button(screen)
        self.draw_reverse(screen)

        if self.game.uno_clicked:
            self.draw_uno(screen)

    # 우노 상태
    def draw_uno(self, screen):
        uno = pygame.image.load('./resource/uno_btn.png')
        uno = pygame.transform.scale(self.uno, (get_uno_width(), get_uno_height()))
        uno_rect = uno.get_rect(topright=self.background_rect.topright)
        screen.blit(uno, uno_rect)

        player = self.game.get_uno_clicked_player()
        if player is not None:
            text = get_small_font().render(player.name, True, COLOR_BLACK)
            screen.blit(text, (uno_rect.x - text.get_width(), 0))

    def draw_reverse(self, screen):
        if self.game.reverse_direction:
            surface = get_skill(Skill.REVERSE.value, 2)
            rect = surface.get_rect(bottomright=self.background_rect.bottomright)
            screen.blit(surface, rect)

    def draw_uno_button(self, screen):
        self.uno = pygame.image.load('./resource/uno_btn.png')
        self.uno = pygame.transform.scale(self.uno, (get_uno_width(), get_uno_height()))
        self.uno_rect = get_center_rect(self.uno, self.background_rect, y = self.background_rect.width // 4 - 10)
        screen.blit(self.uno, self.uno_rect)

    def run_deck_click_event(self, pos):
        if self.deck_rect.collidepoint(pos):
            if self.play_screen.animate_board_player_to_current_card_enabled or self.play_screen.animate_deck_to_player_enabled:
                return
            self.play_screen.on_deck_selected()

    def run_uno_click_event(self, pos):
        if self.uno_rect.collidepoint(pos):
            if not self.game.uno_clicked:
                self.game.uno_clicked = True
                self.game.uno_clicked_player_index = self.game.board_player_index

    def run_uno_key_event(self, event):
        if event.key == self.play_screen.screen_controller.setting.get(MODE_UNO_KEY):
            if not self.game.uno_clicked:
                self.game.uno_clicked = True
                self.game.uno_clicked_player_index = self.game.board_player_index