from screen.achivement.AchivementScreen import AchivementScreen
from util.achievementsutil import AchievementsUtil
from util.extradatautil import ExtraDataUtil
from util.settings import SettingsUtil
from util.globals import *
from screen.home.HomeScreen import HomeScreen
from screen.setting.SettingScreen import SettingScreen

from screen.game.lobby.LobbyScreen import LobbyScreen
from screen.game.play.PlayScreen import PlayScreen
from screen.game.story.StoryScreen import StoryScreen


from game.game import UnoGame
import pygame

class ScreenController:

    screens = {}

    def __init__(self):
        self.init_pygame()

        self.game: UnoGame = UnoGame()

        self.clock = pygame.time.Clock()
        self.fps = 30

        self.screen_type = TYPE_START
        self.running = True

        # 설정 불러오기
        self.setting = SettingsUtil()
        self.screen = pygame.display.set_mode(self.setting.get_resolution())

        # 업적
        self.achivementsUtil = AchievementsUtil()
        self.extraDataUtil = ExtraDataUtil()

        self.init_instance()

        self.is_bgm_playing = False
        self.bgm = pygame.mixer.Sound('./resource/sound/bgm.mp3')
        self.effect = pygame.mixer.Sound('./resource/sound/effect.mp3')

        self.is_paused = False  # 설정에서 돌아오기 위한 용도

    def set_paused(self):
        self.is_paused = True

    def init_pygame(self):
        pygame.init()
        # 아이콘
        pygame.display.set_icon(pygame.image.load("./resource/icon.png"))
        #제목
        pygame.display.set_caption("Uno Game")
        # 기본 마우스
        pygame.mouse.set_visible(False)

    def init_instance(self):
        ScreenController.screens = {
            TYPE_START: HomeScreen(self),
            TYPE_SETTING: SettingScreen(self),
            TYPE_PLAY: PlayScreen(self),
            TYPE_LOBBY: LobbyScreen(self),
            TYPE_STORY: StoryScreen(self),
            TYPE_ACHIVEMENT: AchivementScreen(self),
        }

    # 화면 설정
    def set_screen_type(self, type):
        self.screen_type = type

    # 화면 시작
    def run(self):
        while self.running:
            self.dt = self.clock.tick(self.fps)

            self.display_screen()
            self.run_events()
            pygame.display.update()
            self.update_bgm()
            self.update_setting()

        pygame.quit()

    def update_setting(self):
        if self.screen.get_size() != self.setting.get_resolution():
            self.screen = pygame.display.set_mode(self.setting.get_resolution())

        if self.bgm.get_volume() != self.setting.get_background_volume():
            self.bgm.set_volume(self.setting.get_background_volume())

        if self.effect.get_volume() != self.setting.get_effect_volume():
            self.effect.set_volume(self.setting.get_effect_volume())

        self.update_color_set()

    def update_color_set(self):
        global CARD_COLOR_SET
        global COLOR_SET
        if self.setting.get(MODE_BLIND) == 0:
            CARD_COLOR_SET[CARD_COLOR_NONE] = COLOR_WHITE
            CARD_COLOR_SET[CARD_COLOR_RED] = COLOR_RED
            CARD_COLOR_SET[CARD_COLOR_YELLOW] = COLOR_YELLOW
            CARD_COLOR_SET[CARD_COLOR_GREEN] = COLOR_GREEN
            CARD_COLOR_SET[CARD_COLOR_BLUE] = COLOR_BLUE

            COLOR_SET[CARD_COLOR_RED] = COLOR_RED
            COLOR_SET[CARD_COLOR_YELLOW] = COLOR_YELLOW
            COLOR_SET[CARD_COLOR_GREEN] = COLOR_GREEN
            COLOR_SET[CARD_COLOR_BLUE] = COLOR_BLUE
        else: # 색맹 모드

                CARD_COLOR_SET[CARD_COLOR_NONE] = (204, 121, 167)
                CARD_COLOR_SET[CARD_COLOR_RED] = (239, 159, 0),
                CARD_COLOR_SET[CARD_COLOR_YELLOW] = (240, 228, 66),
                CARD_COLOR_SET[CARD_COLOR_GREEN] = (0, 158, 116),
                CARD_COLOR_SET[CARD_COLOR_BLUE] = (86, 180, 233),

                COLOR_SET[CARD_COLOR_RED] = (239, 159, 0),
                COLOR_SET[CARD_COLOR_YELLOW] = (240, 228, 66),
                COLOR_SET[CARD_COLOR_GREEN] = (0, 158, 116),
                COLOR_SET[CARD_COLOR_BLUE] = (86, 180, 233),



    def update_bgm(self):
        if self.screen_type == TYPE_PLAY:
            if not self.is_bgm_playing:
                self.is_bgm_playing = True
                self.bgm.play(-1)
        else:
            self.bgm.stop()
            self.is_bgm_playing = False


    # 화면 종료
    def stop(self):
        self.running = False

    # 현재 화면 불러옴
    def get_screen(self):
        return ScreenController.screens.get(self.screen_type)

    # 현재 화면 설정
    def set_screen(self, screen_type):
        self.screen_type = screen_type

    # 화면 선택
    def display_screen(self):
        self.get_screen().draw(self.screen)
        self.draw_cursor()

    # 마우스 커서
    def draw_cursor(self):
        cursor = pygame.image.load('./resource/cursor.svg')
        # cursor = pygame.transform.scale(cursor, (35, 40))
        cursor_rect = cursor.get_rect().topleft = pygame.mouse.get_pos()
        self.screen.blit(cursor, cursor_rect)

    # 이벤트 선택
    def run_events(self):
        # 이벤트 목록 
        events = pygame.event.get()

        # 공통 이벤트 처리
        for event in events:
            if event.type == pygame.QUIT: # 종료 이벤트
                self.running = False

        # 화면에 이벤트 전달
        self.get_screen().run_events(events)

    def play_effect(self):
        self.effect.play()