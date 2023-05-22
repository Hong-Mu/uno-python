import pygame

from game.model.card import Card
from game.model.player import dict_to_player
from game_socket.socketevent import SocketEvent
from screen.game.play.base.baseplayscreen import BasePlayScreen


class ClientPlayScreen(BasePlayScreen):

    def __init__(self, screen_controller):
        super().__init__(screen_controller)

        self.client = screen_controller.client

    def check_time(self): # 동작 제거
        self.card_select_enabled = self.game.board_player_index == self.game.current_player_index

    def init_turn(self):
        self.select_color_enabled = False

    def run_computer(self):
        pass  # Clear

    def on_card_selected(self, idx):
        hands = self.game.get_board_player().hands
        card = hands[idx]

        self.client.emit(SocketEvent.INPUT_CURRENT_CARD, {
            'idx': idx,
            'color': card.color,
            'value': card.value,
        })

    def on_deck_selected(self):
        self.client.emit(SocketEvent.INPUT_DECK, {})

    def click_uno(self):
        self.client.emit(SocketEvent.INPUT_UNO, {})

    def on_server_message(self, event, data):
        if event == SocketEvent.ALL_DATA:
            self.hanle_data(data)
        else:
            print('불일치')

    def hanle_data(self, data):
        self.game.players = self.rotate_list_to_id([dict_to_player(p) for p in data['players']], self.client.my_socket_id)

        self.game.turn_start_time = data['turn_start_time']

        card = data['current_card']
        self.game.current_card = Card(card['color'], card['value'])
        self.game.current_color = data['current_color']

        self.game.uno_clicked = data['is_uno']

        self.game.reverse_direction = data['is_reverse']
        self.game.is_started = data['is_started']

        self.game.skip_sids = data['skip_sids']

        for idx, p in enumerate(self.game.players):
            if p.sid == data['turn_sid']:
                self.game.current_player_index = idx

            if p.sid == data['uno_sid']:
                self.game.uno_clicked_player_index = idx
    def on_server_disconnected(self):
        pass

    def rotate_list_to_id(self, players, target_id):
        index = next((i for i, player in enumerate(players) if player.sid == target_id), -1)
        rotated_lst = players[index:] + players[:index]
        return rotated_lst