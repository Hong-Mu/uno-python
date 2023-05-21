import asyncio

from game_socket.client import GameClient
from game_socket.server import GameServer
from screen.achievement.AchievementScreen import AchievementScreen
from model.screentype import ScreenType
from screen.game.lobby.client import ClientLobbyScreen
from screen.game.lobby.host import HostLobbyScreen
from screen.game.lobby.singleplay import LobbyScreen
from screen.game.play.client_play_screen import ClientPlayScreen
from screen.game.play.host_play_screen import HostPlayScreen
from screen.game.play.single_play_screen import SinglePlayScreen
from util.settings import SettingsUtil
from util.globals import *
from screen.home.HomeScreen import HomeScreen
from screen.setting.SettingScreen import SettingScreen
from screen.game.story.StoryScreen import StoryScreen

import pygame

class ScreenController:

    screens = {}

    def __init__(self):
        self.init_pygame()

        self.game = None

        self.server = GameServer()
        self.server.set_on_disconnect_listener(self.on_client_disconnected)

        self.client = GameClient()
        self.client.set_on_disconnect_listener(self.on_server_disconnected)

        self.clock = pygame.time.Clock()
        self.fps = 30

        self.screen_type = ScreenType.HOME
        self.running = True

        # 설정 불러오기
        self.setting = SettingsUtil()
        self.screen = pygame.display.set_mode(self.setting.get_resolution())

        self.init_instance()

        self.is_bgm_playing = False
        self.bgm = pygame.mixer.Sound('./resource/sound/bgm.mp3')
        self.effect = pygame.mixer.Sound('./resource/sound/effect.mp3')

        self.is_paused = False  # 설정에서 돌아오기 위한 용도

    def set_game(self, game):
        self.game = game

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
            ScreenType.HOME: HomeScreen(self),
            ScreenType.SETTING: SettingScreen(self),
            ScreenType.PLAY: SinglePlayScreen(self),
            ScreenType.PLAY_HOST: HostPlayScreen(self),
            ScreenType.PLAY_CLIENT: ClientPlayScreen(self),
            ScreenType.LOBBY_SINGLE: LobbyScreen(self),
            ScreenType.LOBBY_SERVER: HostLobbyScreen(self),
            ScreenType.LOBBY_CLIENT: ClientLobbyScreen(self),
            ScreenType.STORY: StoryScreen(self),
            ScreenType.ACHIEVEMENT: AchievementScreen(self),
        }

    # 화면 시작
    async def run(self):
        while self.running:
            await asyncio.sleep(0.01)
            self.dt = self.clock.tick(self.fps)

            self.display_screen()
            self.run_events()
            pygame.display.update()
            self.update_bgm()
            self.update_setting()

            self.update_socket()

        pygame.quit()

    def update_socket(self):
        if self.server.enabled:
            if not self.server.is_running:
                self.server.start(listener=self.on_client_message)
        else:
            if self.server.is_running:
                self.server.stop()

        if self.client.enabled:
            if not self.client.is_running:
                self.get_screen(ScreenType.HOME).connect()
        else:
            if self.client.is_running:
                self.client.stop()

    async def on_client_message(self, event, sid, data): # 클라이언트로부터의 메세지
        print('[on_client_message]', event, sid, data)
        self.get_screen(ScreenType.LOBBY_SERVER).on_client_message(event, sid, data)


    def on_server_message(self, event, data):
        print('[on_server_message]', event, data)
        self.get_screen(ScreenType.HOME).on_server_message(event, data)
        self.get_screen(ScreenType.LOBBY_CLIENT).on_server_message(event, data)



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
        if self.screen_type == ScreenType.PLAY:
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
    def get_screen(self, screen_type):
        return ScreenController.screens.get(screen_type)

    # 현재 화면 설정
    def set_screen(self, screen_type):
        self.screen_type = screen_type
        for key in self.screens.keys():
            if key == screen_type:
                self.get_screen(key).init()
            else:
                self.get_screen(key).on_destroy()


    # 화면 선택
    def display_screen(self):
        self.get_screen(self.screen_type).draw(self.screen)
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
        self.get_screen(self.screen_type).run_events(events)

    def play_effect(self):
        self.effect.play()


    def on_client_disconnected(self, sid):
        self.get_screen(ScreenType.LOBBY_SERVER).on_client_disconnected(sid)


    def on_server_disconnected(self):
        print('on_server_disconnected')
        self.get_screen(ScreenType.LOBBY_CLIENT).on_server_disconnected()
