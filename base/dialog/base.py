import pygame

from util.globals import *


class BaseDialog:
    def __init__(self, parent):
        self.parent = parent
        self.screen_controller = parent.screen_controller

        self.screen = None

        self.enabled = False

        self.layout = None
        self.layout_rect = None

        self.width = 500
        self.height = 300

        self.background_color = COLOR_WHITE
        self.border_color = COLOR_BLACK

        self.border_size = 2

        self.title = ""
        self.title_color = COLOR_BLACK
        self.title_rect = None

    def init(self):
        self.dismiss()

    def draw(self, screen):
        self.screen = screen

        layout = pygame.Surface(size=self.get_size())
        layout.fill(self.background_color)


        self.draw_border(layout)
        self.draw_title(layout)

        self.layout = layout
        self.layout_rect = layout.get_rect()


    def draw_border(self, layout):
        border = pygame.draw.rect(layout, self.border_color, layout.get_rect(), self.border_size)

    def draw_title(self, layout):
        title = get_medium_font().render(self.title, True, self.title_color)
        self.title_rect = layout.blit(title, title.get_rect(midtop=(layout.get_width() // 2, get_medium_margin())))


    def blit_layout(self, surface):
        surface.blit(self.layout, get_center_rect(self.layout, surface.get_rect()))

    def run_key_event(self, event):
        key = event.key
        if key == pygame.K_ESCAPE:
            self.dismiss()

    def run_click_event(self, event):
        pass

    def show(self):
        self.parent.disable_event()
        self.enabled = True
        print(self.enabled)

    def dismiss(self):
        self.parent.enable_event()
        self.enabled = False

    def get_size(self):
        return self.width, self.height

    def get_pos(self):
        x, y = pygame.mouse.get_pos()
        return x - (self.screen.get_width() - self.width) // 2, y - (self.screen.get_height() - self.height) // 2

