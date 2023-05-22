import pygame

from base.dialog.baseinputdialog import BaseInputDialog
from util.globals import *


class InputPasswordDialog(BaseInputDialog):
    def __init__(self, parent, on_confirm=None):
        super().__init__(parent, on_confirm)
        
        self.title = '비밀번호'


    def draw(self, surface):
        super().draw(surface)

        """레이아웃 추가 시작"""    
        
        """레이아웃 추가 종료"""

        self.blit_layout(surface)
