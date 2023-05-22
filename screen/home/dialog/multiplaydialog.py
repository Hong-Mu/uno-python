from base.dialog.baseMenuDialog import BaseMenuDialog
from model.screentype import ScreenType


class MultiPlayDialog(BaseMenuDialog):
    def __init__(self, parent):
        # 의존성 객체
        super().__init__(parent)
        
        self.title_name = "멀티플레이"
        self.menus = [
            {'text': '방 만들기', 'view': None, 'rect': None,
             'action': lambda: (
                 self.screen_controller.set_screen(ScreenType.LOBBY_SERVER),
             )},

            {'text': '입장하기', 'view': None, 'rect': None,
             'action': lambda: (
                 self.parent.input_address_dialog.show()
             )},

            {'text': '돌아가기', 'view': None, 'rect': None,
             'action': lambda: (
                self.dismiss()
             )},
        ]

