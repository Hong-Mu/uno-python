import random

from base.basegame import BaseGame
from util.extradata import ExtraData
from util.globals import *
from util.singletone import extraDataUtil, achievementsUtil


class BaseAchievementGame(BaseGame):
    def __init__(self):
        super().__init__()

    def set_winner(self, player):
        super().set_winner(player)
        if player == self.get_board_player():
            self.update_win_count()
            self.check_win_count()
            self.check_computer_uno_clicked_when_win()
            self.check_turn_count()
            self.check_player_skilled()
        else:
            self.check_player_uno_clicked_when_lose()

    def click_uno(self):
        super().click_uno()
        self.update_achievement(Achievement.SINGLE_UNO_CNT)

    def run_periodically(self):
        super().run_periodically()
        self.check_uno_count()

    def update_achievement(self, achievement):
        is_acquired = achievementsUtil.get(achievement)[PREF_ACQUIRED]
        if not is_acquired:
            achievementsUtil.set_acquired(achievement)
            self.notify_achievements.append(achievement)

    def check_computer_uno_clicked_when_win(self):
        if self.is_uno_clicked_by_computer:
            self.update_achievement(Achievement.SINGLE_WIN_UNO)

    def check_player_uno_clicked_when_lose(self):
        if self.is_uno_clicked_by_player:
            self.update_achievement(Achievement.SINGLE_LOSE_UNO)

    def check_win_count(self):
        cnt = extraDataUtil.get(ExtraData.SINGLE_WIN_CNT)

        if cnt >= 1:
            self.update_achievement(Achievement.SINGLE_WIN_1)

        if cnt >= 10:
            self.update_achievement(Achievement.SINGLE_WIN_10)

    def check_uno_count(self):
        cnt = extraDataUtil.get(ExtraData.SINGLE_UNO_CNT)

        if cnt >= 1:
            self.update_achievement(Achievement.SINGLE_UNO_CNT)

    def check_turn_count(self):
        print('승리 턴', self.turn_counter - 1)
        if (self.turn_counter - 1) <= 10:
            self.update_achievement(Achievement.SINGLE_WIN_IN_10_TURN)

    def check_player_skilled(self):
        if not self.is_player_skilled:
            self.update_achievement(Achievement.SINGLE_WIN_NO_SKILL)

    def update_win_count(self):
        cnt = extraDataUtil.get(ExtraData.SINGLE_WIN_CNT)
        extraDataUtil.set(ExtraData.SINGLE_WIN_CNT, cnt + 1)

