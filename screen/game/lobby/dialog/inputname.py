import pygame

from base.dialog.baseinputdialog import BaseInputDialog
from util.globals import *


class InputNameDialog(BaseInputDialog):
    def __init__(self, parent, on_confirm=None):
        super().__init__(parent, on_confirm)
        
        self.title = '이름 입력'
        self.input = 'player'


    def draw(self, surface):
        super().draw(surface)

        """레이아웃 추가 시작"""    
        
        """레이아웃 추가 종료"""

        self.blit_layout(surface)
