from game.model.card import Card
from game.model.player import dict_to_player
from game_socket.socketevent import SocketEvent
from screen.game.play.base.baseplayscreen import BasePlayScreen


class ClientPlayScreen(BasePlayScreen):

    def __init__(self, screen_controller):
        super().__init__(screen_controller)

        self.client = screen_controller.client

    def check_time(self): # 동작 제거
        pass

    def init_turn(self):
        pass

    def run_computer(self): # 동작 제거
        pass

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