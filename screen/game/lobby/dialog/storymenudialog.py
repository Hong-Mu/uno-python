from base.dialog.baseMenuDialog import BaseMenuDialog


class StoryMenuDialog(BaseMenuDialog):

    def __init__(self, parent):
        super().__init__(parent)
        
        self.confirmed_idx = -1

        self.title_name = "스토리 모드 선택"

        self.height = 350
        self.menus = [
            {'text': '스토리A', 'view': None, 'rect': None,
             'action': lambda: (
                self.update_confirmed_idx(0)
             )},
            {'text': '스토리B', 'view': None, 'rect': None,
             'action': lambda: (
                 self.update_confirmed_idx(1)
             )},
            {'text': '스토리C', 'view': None, 'rect': None,
             'action': lambda: (
                 self.update_confirmed_idx(2)
             )},
            {'text': '스토리D', 'view': None, 'rect': None,
             'action': lambda: (
                 self.update_confirmed_idx(3)
             )},
            {'text': '미선택', 'view': None, 'rect': None,
             'action': lambda: (
                 self.update_confirmed_idx(-1)
             )},
            {'text': '돌아가기', 'view': None, 'rect': None,
             'action': lambda: (
                self.dismiss()
             )},
        ]

    def update_confirmed_idx(self, idx=-1):
        self.confirmed_idx = idx

        self.parent.menus[1]['text'] = f"스토리 모드 설정: {[menu['text'] for i, menu in enumerate(self.menus) if i <= 4][idx]}"
        self.dismiss()

