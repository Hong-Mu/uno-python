from __future__ import annotations
from typing import TYPE_CHECKING

from base.dialog.baseMenuDialog import BaseMenuDialog
from model.screentype import ScreenType

if TYPE_CHECKING:
    pass


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
            {'text': '업적', 'view': None, 'rect': None,
             'action': lambda: (
                 self.screen_controller.set_screen(ScreenType.ACHIEVEMENT),
                 self.screen_controller.set_paused(),
             )},
            {'text': '돌아가기', 'view': None, 'rect': None,
             'action': lambda: (
                self.dismiss()
             )},
            {'text': '종료', 'view': None, 'rect': None, 'action': lambda: (
                self.init(),
                self.parent.game.finish_game(),
                self.screen_controller.set_screen(ScreenType.HOME),
            )
             }
        ]

    def show(self):
        print('show')
        super().show()
        self.parent.pause_game()

    def dismiss(self):
        super().dismiss()
        self.parent.continue_game()