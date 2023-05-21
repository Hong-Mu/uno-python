

class SocketEvent:
    JOIN = "join"
    AUTH = "auth"
    SLOT = "slot"

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

    ALL_DATA = "all_data"

    """
    {
        time: 3,
        turn: sid,
        current_card: ?,
        current_color: ?,
        is_reverse: False,
        is_running: True,
        is_turn_start: False
        winner: None,
        players: [
            {
                sid: sdfdsfsdfdsf,
                name: sfsdfsdfdsfdsf,
                is_penalty: False
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



