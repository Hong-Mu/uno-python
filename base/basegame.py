import time

from game.model.deck import Deck
from util.extradata import ExtraDataUtil
from util.globals import *


class BaseGame:
    def __init__(self):
        self.is_started = False

        self.play_type = None
        self.players = []

        self.reverse_direction = False
        self.current_player_index = 0
        self.board_player_index = 0
        self.previous_player_index = 0
        self.next_player_index = 0
        self.turn_counter = None

        self.deck = None
        self.current_card = None
        self.current_color = None

        self.turn_time = 10
        self.uno_count = 2  # TODO 우노 버튼을 클릭해야 할 카드 개수: 기본2
        self.skip_direction = 1

        self.skill_plus_cnt = 0

        self.turn_start_time = None
        self.is_turn_start = False

        self.can_uno_penalty = False
        self.uno_enabled = False
        self.uno_clicked = False
        self.uno_clicked_player_index = None

    def init(self):
        self.is_started = True

        self.reverse_direction = False
        self.current_player_index = 0
        self.board_player_index = 0
        self.next_player_index = 1
        self.previous_player_index = None
        self.turn_counter = 1
        self.skip_direction = 1

        self.skill_plus_cnt = 0

        self.turn_start_time = time.time()
        self.is_turn_start = False

        self.can_uno_penalty = False
        self.uno_enabled = False
        self.uno_clicked = False
        self.uno_clicked_player_index = None


    def start_game(self):
        self.deck = Deck(self)
        self.init()

        self.current_card = self.deck.draw()
        self.current_color = self.current_card.color


    def run_in_turn_start(self):
        pass


    def finish_game(self):
        self.is_started = False
        self.players = []

    # 다음 턴
    def next_turn(self, turn=1):
        self.is_turn_start = True
        # 이전 플레이어 저장
        self.previous_player_index = self.current_player_index
        direction = -turn if self.reverse_direction else turn
        next_direction = -(turn + 1) if self.reverse_direction else (turn + 1)

        self.skip_direction = direction

        self.next_player_index = (self.current_player_index + next_direction) % len(self.players)
        self.current_player_index = (self.current_player_index + direction) % len(self.players)

        self.turn_counter += 1
        self.reset_turn_start_time()

    def set_players(self, players):
        self.players = players

    # 현재 플레이어 반환
    def get_current_player(self):
        return self.players[self.current_player_index]

    def get_board_player(self):
        return self.players[self.board_player_index]

    def get_next_player(self):
        return self.players[self.next_player_index]

    def get_previous_player(self):
        return self.players[self.previous_player_index]

    def draw(self):
        print(f'드로우 {self.current_player_index}')
        self.get_current_player().draw(self.deck.draw())

    # 카드 제출
    def play(self, idx=None):
        self.set_current_card(self.get_current_player().play(self, idx))

    def reset_turn_start_time(self):
        self.turn_start_time = time.time()

    # 다음 턴 스킵 :
    def skip_turn(self, skip=1):
        print('스킵')
        self.next_turn(skip + 1)

    # 스킵된 플레이어 인덱스 리스트를 반환하는 함수
    def get_skipped_player_indexs(self):
        temp = []
        if abs(self.skip_direction) != 1:
            for direction in list(range(1, abs(self.skip_direction))) if self.skip_direction > 0 else list(
                    range(-1, self.skip_direction, -1)):
                temp.append((self.previous_player_index + direction) % len(self.players))

        return temp

    # 턴 이동 방향 변경
    def toggle_turn_direction(self):
        self.reverse_direction = not self.reverse_direction

    # 카드 분배
    def deal(self, n=7):
        for player in self.players:
            player.deal(self.deck.deal(n))

    # 플레이어에게 패널티 카드 n장 부여
    def penalty(self, player_index, n=1):
        for _ in range(n):
            self.players[player_index].draw(self.deck.draw())

    # 현재 카드 변경
    def set_current_card(self, card):
        self.current_card = card
        self.current_color = card.color

    # 카드 검증
    def verify_new_card(self, new_card) -> bool:
        if self.current_card.value == SKILL_COLOR:
            if new_card.color == CARD_COLOR_NONE:
                print('유효성 검사1', new_card.value == SKILL_COLOR)
                return new_card.value == SKILL_COLOR

        # 이전 카드가 미색상 기술 카드이면서 새로운 카드가 미색상 카드가 아닌 경우
        temp = self.current_color == CARD_COLOR_NONE or \
               new_card.color == CARD_COLOR_NONE or \
               self.current_color == new_card.color or \
               self.current_card.value == new_card.value
        print('유효성 검사2', temp)
        return temp

    def update_uno_enabled(self):
        self.uno_enabled = len(self.get_current_player().hands) == self.uno_count

    def is_game_over(self) -> bool:
        for idx, player_hands in enumerate([player.hands for player in self.players]):
            if len(player_hands) == 0:
                self.set_winner(self.players[idx])
                return True
        return False

    def set_winner(self, player):
        self.winner = player

    def get_winner(self):
        return self.winner