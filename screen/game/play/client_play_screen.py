from screen.game.play.base.baseplayscreen import BasePlayScreen


class ClientPlayScreen(BasePlayScreen):

    def __init__(self, screen_controller):
        super().__init__(screen_controller)

    def check_time(self): # 동작 제거
        pass

    def init_turn(self):
        pass

    def run_computer(self): # 동작 제거
        pass