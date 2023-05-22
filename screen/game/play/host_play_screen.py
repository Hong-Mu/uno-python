from game.model.player import player_to_dict
from game_socket.socketevent import SocketEvent
from screen.game.play.base.baseplayscreen import BasePlayScreen
from util.globals import CARD_COLOR_NONE


class HostPlayScreen(BasePlayScreen):

    def __init__(self, screen_controller):
        super().__init__(screen_controller)

        self.server = screen_controller.server

    def init(self):
        super().init()

    def init_turn(self):
        super().init_turn()
        self.send_data_to_clients()

    def run_computer(self):
        super().run_computer()
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
        elif event == SocketEvent.SKILL_COLOR:
            self.handle_skill_color(sid, data)

    def handle_input_card(self, sid, data):
        player = self.get_player_by_sid(sid)
        card = player.hands[data['idx']]

        if self.game.verify_new_card(card):
            self.to_computer_play_idx = data['idx']
            self.start_player_to_deck(data['idx'])

            if card.color == CARD_COLOR_NONE:
                self.server.emit(SocketEvent.SKILL_COLOR, sid, data={  # 색상 선택 요청
                    'type': 'request'
                })

    def handle_input_deck(self, sid, data):
        self.on_deck_selected()

    def handle_input_uno(self, sid, data):
        if self.game.uno_enabled and not self.game.uno_clicked:
            self.game.uno_clicked = True
            self.game.uno_clicked_player_index = self.get_player_idx_by_sid(sid)

    def send_data_to_clients(self):
        temp_skip_sids = [p.sid for idx, p in enumerate(self.game.players) if idx in self.game.get_skipped_player_indexs()]
        temp = {
            'turn_start_time': self.game.turn_start_time,
            'turn_sid': self.game.get_current_player().sid,
            'previous_sid': self.game.get_previous_player().sid,
            'next_sid': self.game.get_next_player().sid,

            'can_uno_penalty': self.game.can_uno_penalty,
            'skill_plus_cnt': self.game.skill_plus_cnt,

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

    def get_player_idx_by_sid(self, sid):
        for idx, p in enumerate(self.game.players):
            if p.sid == sid:
                return idx
        return -1
    def get_player_by_sid(self, sid):
        return next((p for p in self.game.players if p.sid == sid))


    def start_player_to_deck(self, idx):
        super().start_player_to_deck(idx)

        self.server.emit(SocketEvent.ANIM_PLAYER_TO_CURRENT_CARD, data={
            'player': self.game.get_current_player().sid,
            'idx': idx,
        })

    def start_board_player_to_current_card(self, card, idx):
        super().start_board_player_to_current_card(card, idx)

        self.server.emit(SocketEvent.ANIM_PLAYER_TO_CURRENT_CARD, data={
            'player': self.game.get_board_player().sid,
            'idx': idx,
        })

    def on_deck_selected(self):
        super().on_deck_selected()

        self.server.emit(SocketEvent.ANIM_DECK_TO_PLAYER, data={
            'player': self.game.players[self.destination_player_idx].sid,
            'skill_plus_cnt': self.game.skill_plus_cnt
        })

    def handle_skill_color(self, sid, data):
        color = data['color']
        self.game.current_color = color
        self.game.next_turn()

