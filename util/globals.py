import os

import pygame
from game.model.card import Card
from model.achievement import Achievement

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KEY_NAME = "name"
KEY_DESC = "description"

PREF_ACQUIRED = "acquired"
PREF_TIMIESTAMP = "timestamp"

COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (128, 128, 128)
COLOR_LIGHT_GRAY = (192, 192, 192)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_BLUE = (0, 0, 255)

COLOR_ACHIVEMENT = (15, 169, 88)

COLOR_TRANSPARENT_WHITE = (255, 255, 255, 128)
COLOR_TRANSPARENT_WHITE_25 = (255, 255, 255, 64)
COLOR_TRANSPARENT_RED = (255, 0, 0, 128)

COLOR_BOARD = (8, 64, 21)
COLOR_PLAYER = (40, 120, 58)

CARD_COLOR_NONE = "none"
CARD_COLOR_RED = "red"
CARD_COLOR_YELLOW = "yellow"
CARD_COLOR_GREEN = "green"
CARD_COLOR_BLUE = "blue"

CARD_COLOR_SET = {
    CARD_COLOR_NONE: COLOR_WHITE,
    CARD_COLOR_RED: COLOR_RED,
    CARD_COLOR_YELLOW: COLOR_YELLOW,
    CARD_COLOR_GREEN: COLOR_GREEN,
    CARD_COLOR_BLUE: COLOR_BLUE,
}

COLOR_SET = {
    CARD_COLOR_RED: COLOR_RED,
    CARD_COLOR_YELLOW: COLOR_YELLOW,
    CARD_COLOR_GREEN: COLOR_GREEN,
    CARD_COLOR_BLUE: COLOR_BLUE,
}


MODE_SCREEN = "mode_screen"
MODE_BLIND = "mode_blind"
MODE_MASTER_VOLUME = "mode_master_volume"
MODE_BACKGROUND_VOLUME = "mode_background_volume"
MODE_EFFECT_VOLUME = "mode_effect_volume"
MODE_KEY = "mode_key"
MODE_UNO_KEY = "mode_uno_key"
MODE_DECK_KEY = "mode_deck_key"

MODE_CLEAR = "mode_clear"
MODE_RETURN = "mode_return"

DIMEN_EXTRA_LARGE = 50
DIMEN_LARGE = 40
DIMEN_MEDIUM = 30
DIMEN_SMALL = 20
DIMEN_EXTRA_SMALL = 10

DIMEN_MARGIN_MEDIUM = 20
DIMEN_MARGIN_SMALL = 10
DIMEN_MARGIN_EXTRA_SMALL = 5

CARD_WIDTH = 30
CARD_HEIGHT = 45

DECK_PERCENT = 2
MY_BOARD_CARD_PERCENT = 1.5

UNO_WIDTH = 50
UNO_HEIGHT = 50

ACHIEVE_INFO = {
    Achievement.SINGLE_WIN_1:
        {KEY_NAME: "싱글 플레이어 대전에서 승리", KEY_DESC: "싱글 플레이어 대전에서 승리하여 업적 달성!", },
    Achievement.SINGLE_WIN_10:
        {KEY_NAME: "UNO게임 마스터", KEY_DESC: "싱글 플레이어 대전에서 10번 승리하여 업적 달성!", },
    Achievement.SINGLE_WIN_IN_10_TURN:
        {KEY_NAME: "너무 쉬운데?", KEY_DESC: "싱글 플레이어 대전에서 10턴 안에 승리하여 업적 달성!", },
    Achievement.SINGLE_WIN_NO_SKILL:
        {KEY_NAME: "핸디캡 줘도 이기네ㅋ", KEY_DESC: "기술 카드를 단 한 번도 사용하지 않고 승리하여 업적 달성!", },
    Achievement.STORY_A:
        {KEY_NAME: "스토리모드 A 승리", KEY_DESC: "스토리모드 A 대전에서 승리하여 업적 달성!", },
    Achievement.STORY_B:
        {KEY_NAME: "스토리모드 B 승리", KEY_DESC: "스토리모드 B 대전에서 승리하여 업적 달성!", },
    Achievement.STORY_C:
        {KEY_NAME: "스토리모드 C 승리", KEY_DESC: "스토리모드 C 대전에서 승리하여 업적 달성!", },
    Achievement.STORY_D:
        {KEY_NAME: "스토리모드 D 승리", KEY_DESC: "스토리모드 D 대전에서 승리하여 업적 달성!", },
    Achievement.SINGLE_WIN_UNO:
        {KEY_NAME: "이걸 역전하네?!", KEY_DESC: "다른 플레이어가 UNO를 선언한 뒤에 승리하여 업적 달성!", },
    Achievement.SINGLE_LOSE_UNO:
        {KEY_NAME: "이걸 역전당하네..", KEY_DESC: "내가 UNO를 선언한 뒤에 패배하여 업적 달성!", },
    Achievement.SINGLE_UNO_CNT:
        {KEY_NAME: "순발력 좋은데?", KEY_DESC: "상대보다 UNO 먼저 선언한 횟수", }
}

def get_rect(view, x, y):
    return view.get_rect(center = (x, y + view.get_height() // 2))

def get_center_rect(view, parent_rect, x = 0, y = 0) -> pygame.Rect:
    if type(parent_rect) is pygame.Rect:
        return view.get_rect(center = (parent_rect.left + parent_rect.width // 2 + x, parent_rect.top + parent_rect.height // 2 + y))
    else:
        return view.get_rect(center = (parent_rect.left + parent_rect.width // 2 + x, parent_rect.top + parent_rect.height // 2 + y))

def get_left_center_rect(view, parent_rect: pygame.Rect, x = 0, y = 0):
    return view.get_rect(topleft = (parent_rect.left + x, parent_rect.height // 2 + y))
def get_top_center_rect(view, parent_rect: pygame.Rect, x = 0, y = 0):
    return view.get_rect(topleft = (parent_rect.centerx + x, parent_rect.top + y))

def get_bottom_center_rect(view, parent_rect: pygame.Rect, x = 0, y = 0):
    return view.get_rect(bottomleft = (parent_rect.centerx + x, parent_rect.bottom + y))

def get_large_font(percent = 1):
    return pygame.font.Font('./resource/font/pretendard_regular.otf', DIMEN_LARGE * percent)

def get_medium_font(percent = 1):
    return pygame.font.Font('./resource/font/pretendard_regular.otf', DIMEN_MEDIUM * percent)

def get_small_font(percent = 1):
    return pygame.font.Font('./resource/font/pretendard_regular.otf', DIMEN_SMALL * percent)

def get_extra_small_font(percent = 1):
    return pygame.font.Font('./resource/font/pretendard_regular.otf', DIMEN_EXTRA_SMALL * percent)


def get_medium_margin(percent = 1):
    return DIMEN_MARGIN_MEDIUM * percent

def get_small_margin(percent = 1):
    return DIMEN_MARGIN_SMALL * percent

def get_extra_small_margin(percent = 1):
    return DIMEN_MARGIN_EXTRA_SMALL * percent


def get_card_width(percent = 1):
    return CARD_WIDTH * percent

def get_card_height(percent = 1):
    return CARD_HEIGHT * percent

def get_uno_width(percent = 1):
    return UNO_WIDTH * percent

def get_uno_height(percent = 1):
    return UNO_HEIGHT * percent

def get_card_back(scale = 1):
    card_back = pygame.image.load('./resource/card_back.png')
    card_back = pygame.transform.scale(card_back, (get_card_width(scale), get_card_height(scale)))
    return card_back

def get_card(card: Card, scale = 1):
    surface = pygame.Surface((get_card_width(scale), get_card_height(scale)))
    surface.fill(CARD_COLOR_SET.get(card.color))

    # 숫자 카드
    if card.value in range(1, 10):
        text = get_small_font().render(str(card.value), True, COLOR_BLACK)
        surface.blit(text, get_center_rect(text, surface.get_rect()))
    # 기술 카드
    else:
        skill = pygame.image.load(f'./resource/{card.value}.png')
        skill = pygame.transform.scale(skill, (get_card_width(scale) // 1.5, get_card_width(scale) // 1.5))
        surface.blit(skill, get_center_rect(skill, surface.get_rect()))
    return surface

def get_skill(value, scale = 1):
    skill = pygame.image.load(f'./resource/{value}.png')
    skill = pygame.transform.scale(skill, (get_card_width(scale) // 1.5, get_card_width(scale) // 1.5))
    return skill