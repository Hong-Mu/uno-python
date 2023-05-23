import pygame

from base.toast import Toast
from util.globals import COLOR_WHITE


class BaseScreen:
    def __init__(self, screen_controller):
        self.screen_controller = screen_controller
        self.screen = None

        self.event_enabled = True

        self.toast = Toast(self)

    def init(self):
        pass

    def on_destroy(self):
        pass

    def draw(self, screen):
        self.screen = screen
        screen.fill(COLOR_WHITE)


    def run_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.run_key_event(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.run_click_event(event)

    def run_key_event(self, event):
        pass
    def run_click_event(self, event):
        pass

    def disable_event(self):
        self.event_enabled = False

    def enable_event(self):
        self.event_enabled = True
