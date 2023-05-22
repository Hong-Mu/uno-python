from game.model.player import player_to_dict
from game_socket.socketevent import SocketEvent
from screen.game.play.base.baseplayscreen import BasePlayScreen


class HostPlayScreen(BasePlayScreen):

    def __init__(self, screen_controller):
        super().__init__(screen_controller)

        self.server = screen_controller.server

    def init(self):
        super().init()

    def init_turn(self):
        super().init_turn()
        self.send_data_to_clients()

    def on_client_disconnected(self, sid):
        pass

    def on_client_message(self, event, sid, data):
        if event == SocketEvent.INPUT_CURRENT_CARD:
            self.handle_input_card(sid, data)
        elif event == SocketEvent.INPUT_DECK:
            self.handle_input_deck(sid, data)
        elif event == SocketEvent.INPUT_UNO:
            self.handle_input_uno(sid, data)

    def handle_input_card(self, sid, data):
        player = self.get_player_by_sid(sid)
        card = player.hands[data['idx']]

        if self.game.verify_new_card(card):
            self.to_computer_play_idx = data['idx']
            self.start_player_to_deck()

    def handle_input_deck(self, sid, data):
        self.on_deck_selected()

    def handle_input_uno(self, sid, data):
        pass

    def send_data_to_clients(self):
        temp_skip_sids = [p.sid for idx, p in enumerate(self.game.players) if idx in self.game.get_skipped_player_indexs()]
        temp = {
            'turn_start_time': self.game.turn_start_time,
            'turn_sid': self.game.get_current_player().sid,

            'current_card': {
                'color': self.game.current_card.color,
                'value': self.game.current_card.value,
            },

            'current_color': self.game.current_color,

            'is_uno':  self.game.uno_clicked,
            'uno_sid': self.game.get_uno_clicked_player().sid if self.game.get_uno_clicked_player() is not None else None,

            'is_reverse': self.game.reverse_direction,

            'skip_sids': temp_skip_sids,

            'is_started': self.game.is_started,
            'players': [player_to_dict(p) for p in self.game.players]
        }

        self.server.emit(SocketEvent.ALL_DATA, data=temp)

    def get_player_by_sid(self, sid):
        return next((p for p in self.game.players if p.sid == sid))

