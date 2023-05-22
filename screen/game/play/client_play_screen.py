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
        pass

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
            self.handle_data(data)
        elif event == SocketEvent.ANIM_PLAYER_TO_CURRENT_CARD:
            self.handle_player_to_current_card(data)
        elif event == SocketEvent.ANIM_DECK_TO_PLAYER:
            self.handle_deck_to_player(data)
        elif event == SocketEvent.SKILL_COLOR:
            self.handle_skill_color(data)

    def handle_data(self, data):
        self.game.players = self.rotate_list_to_id([dict_to_player(p) for p in data['players']], self.client.my_socket_id)

        self.game.turn_start_time = data['turn_start_time']

        card = data['current_card']
        self.game.current_card = Card(card['color'], card['value'])
        self.game.current_color = data['current_color']

        self.game.uno_clicked = data['is_uno']

        self.game.can_uno_penalty = data['can_uno_penalty']
        self.game.skill_plus_cnt = data['skill_plus_cnt']

        self.game.reverse_direction = data['is_reverse']
        self.game.is_started = data['is_started']

        self.game.skip_sids = data['skip_sids']

        for idx, p in enumerate(self.game.players):
            if p.sid == data['turn_sid']:
                self.game.current_player_index = idx

            if p.sid == data['next_sid']:
                self.game.next_player_index = idx

            if p.sid == data['previous_sid']:
                self.game.previous_player_index = idx

            if p.sid == data['uno_sid']:
                self.game.uno_clicked_player_index = idx

    def on_server_disconnected(self):
        pass

    def rotate_list_to_id(self, players, target_id):
        index = next((i for i, player in enumerate(players) if player.sid == target_id), -1)
        rotated_lst = players[index:] + players[:index]
        return rotated_lst

    def handle_player_to_current_card(self, data):
        player_idx = self.get_player_idx_by_sid(data['player'])

        print(player_idx, self.game.board_player_index)
        if player_idx == self.game.board_player_index:
            card = self.game.get_board_player().hands[data['idx']]
            self.start_board_player_to_current_card(card, data['idx'])
        else:
            self.start_player_to_deck(0)

    def animate_deck_to_player(self, screen):
        if self.animate_controller.enabled:
            self.animate_controller.draw(screen)
        else:
            self.animate_deck_to_player_end()

    def animate_deck_to_player_end(self):
        self.animate_deck_to_player_enabled = False

    def animate_board_player_to_current_card(self, screen):
        if self.animate_controller.enabled:
            self.animate_controller.draw(screen)
        else:
            self.animate_board_player_to_current_card_end()

    def animate_board_player_to_current_card_end(self):
        self.animate_board_player_to_current_card_enabled = False

    def animate_current_player_to_current_card(self, screen):
        if self.animate_controller.enabled:
            self.animate_controller.draw(screen)
        else:
            self.animate_current_player_to_current_card_end()

    def animate_current_player_to_current_card_end(self):
        self.animate_current_player_to_current_card_enabled = False

    def get_player_idx_by_sid(self, sid):
        for idx, p in enumerate(self.game.players):
            if p.sid == sid:
                return idx
        return -1
    def get_player_by_sid(self, sid):
        return next((p for p in self.game.players if p.sid == sid))

    def handle_deck_to_player(self, data):
        sid = data['player']
        self.game.skill_plus_cnt = data['skill_plus_cnt']
        super().on_deck_selected()


    def handle_skill_color(self, data):
        self.select_color_enabled = True
        print('========================색상 선택 활성화====================')


    def update_color(self, color):
        self.select_color_enabled = False
        self.client.emit(SocketEvent.SKILL_COLOR, {
            'type': None,
            'color': color
        })
