

class SocketEvent:
    NAME = 'name'
    JOIN = "join"
    AUTH = "auth"
    SLOT = "slot"
    START = "start"

    ANIM_DECK_TO_PLAYER = "anim_deck_to_board_player"
    """
    {
        player: sid
    }
    """

    ANIM_PLAYER_TO_CURRENT_CARD = "anim_player_to_current_card"
    """
    {
        player: sid
    }
    """

    INPUT_CURRENT_CARD = "input_current_card"
    """
    {
        color: ?
        value: ?
    }
    """
    INPUT_DECK = "input_deck"
    INPUT_UNO = "input_uno"

    ALL_DATA = "all_data"

    """
    컴퓨터 프레이어의 경우 임의 sid 생성 및 전달
    {
        game_turn_start_time: 0,
        turn_sid: sid,
        
        current_card: ?,
        current_color: ?,
        
        is_uno: False,
        uno_sid: sid
        
        is_reverse: False,
        is_turn_start: False,
        winner: None,
        
        skip_sids: [],
        players: [
            {
                sid: sdfdsfsdfdsf,
                name: sfsdfsdfdsfdsf,
                cards: [
                    {
                        color: ??
                        value: ??
                    }
                ]
            }
        ],
    }
    """



