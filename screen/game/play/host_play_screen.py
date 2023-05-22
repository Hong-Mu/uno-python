from screen.game.play.base.baseplayscreen import BasePlayScreen


class HostPlayScreen(BasePlayScreen):

    def __init__(self, screen_controller):
        super().__init__(screen_controller)

    def init_turn(self):
        super().init_turn()
