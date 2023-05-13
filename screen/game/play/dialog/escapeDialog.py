from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from base.baseMenuDialog import BaseMenuDialog
from screen.model.screentype import ScreenType
from util.globals import *

if TYPE_CHECKING:
    from screen.game.play.PlayScreen import PlayScreen


class EscapeDialog(BaseMenuDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.title_name = "일시정지"
        self.menus = [
            {'text': '설정', 'view': None, 'rect': None,
             'action': lambda: (
                 self.screen_controller.set_screen(ScreenType.SETTING),
                 self.screen_controller.set_paused(),
             )},
            {'text': '돌아가기', 'view': None, 'rect': None,
             'action': lambda: (
                self.toggle()
             )},
            {'text': '종료', 'view': None, 'rect': None, 'action': lambda: (
                self.parent.init(),
                self.parent.game.finish_game(),
                self.screen_controller.set_screen(ScreenType.START),
            )
             }
        ]

    def toggle(self):
        super().toggle()

        if self.enabled:
            self.parent.pause_game()
        else:
            self.parent.continue_game()