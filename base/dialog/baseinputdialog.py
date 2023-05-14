import pygame

from base.dialog.base import BaseDialog
from util.globals import *


class BaseInputDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.input = ''
        self.confirm_rect = None

    def draw(self, surface):
        super().draw(surface)
        self.draw_input_box(self.layout)
        self.draw_confirm(self.layout)

    def draw_input_box(self, layout):
        input = get_small_font().render(self.input, True, COLOR_BLACK)

        background = pygame.Surface(size=(self.layout_rect.w - 4 * get_medium_margin(), input.get_height() + get_small_margin()))
        background.fill(COLOR_LIGHT_GRAY)

        layout.blit(background, background.get_rect(center=(self.layout_rect.w // 2, self.layout_rect.h // 2)))
        layout.blit(input, input.get_rect(center=(self.layout_rect.w // 2, self.layout_rect.h // 2)))

    def draw_confirm(self, layout):
        text = get_medium_font().render('확인', True, COLOR_BLACK)
        self.confirm_rect = layout.blit(text, text.get_rect(midbottom=(self.layout_rect.w // 2, self.layout_rect.h - get_medium_margin())))


    def run_key_event(self, event):
        super().run_key_event(event)

        key = event.key
        if key == pygame.K_RETURN:
            self.dismiss()
        elif key == pygame.K_BACKSPACE:
            self.input = self.input[:-1]
        elif event.unicode.isalnum():
            self.input += event.unicode


    def run_click_event(self, event):
        super().run_click_event(event)
        pos = self.get_pos()
        if self.confirm_rect.collidepoint(pos):
            self.dismiss()


