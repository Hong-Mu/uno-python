from __future__ import annotations
from typing import TYPE_CHECKING

from game.model.player import Player
from game.model.region import Region
from game.story.regiona import GameA
from game.story.regionb import GameB
from game.story.regionc import GameC
from game.story.regiond import GameD
from screen.model.screentype import ScreenType
from util.extradata import ExtraData

if TYPE_CHECKING:
    from screen.ScreenController import ScreenController

from util.globals import *


class StoryScreen:
    def __init__(self, screen_controller):
        # 상위 의존성 초기화
        self.screen_controller: ScreenController = screen_controller
        self.game = screen_controller.game

        self.is_confirm_enabled = False
        self.is_story_enabled = True

        # 선택할 수 있는 스토리 최대 인덱스
        self.current_position = 0
        self.confirm_idx = 0

        # 스토리 목록
        self.stories = [
            {'type': Region.A, 'game': GameA, 'rect': None, 'action': None, 'hover': None, 'color': COLOR_RED, 'features': ['컴퓨터 플레이어 첫 분배 기술 카드 확률 50% 상승', '컴퓨터 플레이어 기술 카드 콤보 사용(2-3장)']},
            {'type': Region.B, 'game': GameB, 'rect': None, 'action': None, 'hover': None, 'color': COLOR_BLUE, 'features': ['컴퓨터 플레이어 3명', '모든 카드를 같은 수만큼 분배']},
            {'type': Region.C, 'game': GameC, 'rect': None, 'action': None, 'hover': None, 'color': COLOR_GREEN, 'features': ['컴퓨터 플레이어 2명', '매 5턴마다 낼 수 있는 카드 색상 무작위 변경']},
            {'type': Region.D, 'game': GameD, 'rect': None, 'action': None, 'hover': None, 'color': COLOR_YELLOW, 'features': ['컴퓨터 플레이어 5명', '숫자 카드로만 진행']},
        ]

        # 확인 다이얼로그
        self.confirm_yes_rect = None
        self.confirm_no_rect = None

    def init(self):
        self.is_story_enabled = True
        self.is_confirm_enabled = False

    def draw(self, screen: pygame.Surface):
        screen.fill(COLOR_WHITE)
        self.draw_stories(screen)

        if self.is_confirm_enabled:
            self.draw_confirm_dialog(screen)

    def draw_stories(self, screen):
        width = screen.get_width() / (len(self.stories) + 1)
        for idx, story in enumerate(self.stories):
            color = story['color'] if idx <= extraDataUtil.get(ExtraData.STORY_CLEARED.name) else COLOR_GRAY
            story['rect'] = pygame.draw.circle(screen, color, (width * (idx + 1), screen.get_height() // 2), 20, 3)

            # 현재 위치
            if idx == self.current_position:
                # 위치 표시
                pygame.draw.circle(screen, story['color'], (width * (idx + 1), screen.get_height() // 2), 20)

                # 기능 설명
                for feature_idx, feature in enumerate(story['features']):
                    feature_text = get_medium_font().render(feature, True, COLOR_BLACK)
                    feature_text_rect = get_center_rect(feature_text, screen.get_rect(), y=feature_text.get_height() * (feature_idx + 1) - screen.get_height() // 2)
                    screen.blit(feature_text, feature_text_rect)

    def draw_confirm_dialog(self, screen):
        width, height = 500, 200

        # 배경
        background = pygame.Surface(size=(width, height))
        background.fill(COLOR_WHITE)
        background_rect = get_center_rect(background, screen.get_rect())

        # 내용
        title = get_medium_font().render('대전을 시작하시겠습니까?', True, COLOR_BLACK)
        title_rect = get_center_rect(title, background_rect)

        # 아니요
        no = get_medium_font().render('아니요', True, COLOR_BLACK if self.confirm_idx == 1 else COLOR_GRAY)
        self.confirm_no_rect = get_bottom_center_rect(no, background_rect, x=get_extra_small_margin(), y=-get_extra_small_margin())

        # 예
        yes = get_medium_font().render('예', True, COLOR_BLACK if self.confirm_idx == 0 else COLOR_GRAY)
        self.confirm_yes_rect = get_bottom_center_rect(yes, background_rect, x=-(no.get_width() + get_extra_small_margin()), y=-get_extra_small_margin())

        screen.blit(background, background_rect)
        pygame.draw.rect(screen, COLOR_BLACK, background_rect, 2)

        screen.blit(title, title_rect)
        screen.blit(yes, self.confirm_yes_rect)
        screen.blit(no, self.confirm_no_rect)

    def run_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.run_key_event(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.run_click_event(event)

    def run_key_event(self, event):
        key = event.key
        if self.is_story_enabled:
            self.run_story_event(key)

        elif self.is_confirm_enabled:
            self.run_confirm_event(key)

    def run_story_event(self, key):
        if key == pygame.K_RIGHT:
            self.update_current_position(1)
        elif key == pygame.K_LEFT:
            self.update_current_position(-1)
        elif key == pygame.K_RETURN:
            self.toggle_confirm_dialog()

    def toggle_confirm_dialog(self):
        self.is_story_enabled = not self.is_story_enabled
        self.is_confirm_enabled = not self.is_confirm_enabled

    def run_confirm_event(self, key):
        if key == pygame.K_RIGHT:
            self.update_confirm_idx(1)
        elif key == pygame.K_LEFT:
            self.update_confirm_idx(-1)
        elif key == pygame.K_RETURN:
            self.run_confirm_action()

    def run_confirm_action(self):
        if self.confirm_idx == 0:
            self.move_play_screen()
        else:
            self.is_confirm_enabled = False
            self.is_story_enabled = True

    def update_current_position(self, direction):
        self.current_position = (self.current_position + direction) % (extraDataUtil.get(ExtraData.STORY_CLEARED.name) + 1)

    def update_confirm_idx(self, direction):
        self.confirm_idx = (self.confirm_idx + direction) % 2

    def run_click_event(self, event):
        pos = pygame.mouse.get_pos()
        if self.is_story_enabled:
            self.run_story_click_event(pos)
        elif self.is_confirm_enabled:
            self.run_confirm_click_event(pos)


    def run_story_click_event(self, pos):
        for idx, story in enumerate(self.stories):
            if story['rect'].collidepoint(pos):
                if idx <= extraDataUtil.get(ExtraData.STORY_CLEARED.name):
                    self.current_position = idx
                    self.toggle_confirm_dialog()

    def run_confirm_click_event(self, pos):
        if self.confirm_yes_rect.collidepoint(pos):
            self.move_play_screen()

        elif self.confirm_no_rect.collidepoint(pos):
            self.is_confirm_enabled = False
            self.is_story_enabled = True

    def move_play_screen(self):
        self.screen_controller.set_screen_type(ScreenType.PLAY)
        self.screen_controller.set_game(self.get_selected_story()['game']())
        self.screen_controller.game.set_players([Player("You")])
        self.screen_controller.game.start_game()

    def get_selected_story(self):
        return self.stories[self.current_position]

