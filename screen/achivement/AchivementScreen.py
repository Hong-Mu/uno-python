import os

from util.achievementsutil import *
from util.fontutil import wrap_text
from util.globals import *
import pygame

KEY_NAME = "name"
KEY_DESC = "description"

SCROLL_UP = 4
SCROLL_DOWN = 5

ITEM_WIDTH, ITEM_HEIGHT = (150, 150)

class AchivementScreen:
    def __init__(self, screen_controller):
        self.screen_controller = screen_controller
        self.achivementsUtil = screen_controller.achivementsUtil
        self.extraDataUtil = screen_controller.extraDataUtil

        self.title_rect = None
        self.scroll_surface = None

        self.scroll_y = 0
        self.scroll_speed = 50
        self.scroll_max = None

        self.info = {
            Achivement.SINGLE_WIN_1:
                {KEY_NAME: "싱글 플레이어 대전에서 승리", KEY_DESC: "싱글 플레이어 대전에서 승리하여 업적 달성!", },
            Achivement.SINGLE_WIN_10:
                {KEY_NAME: "UNO게임 마스터", KEY_DESC: "싱글 플레이어 대전에서 10번 승리하여 업적 달성!", },
            Achivement.SINGLE_WIN_IN_10_TURN:
                {KEY_NAME: "너무 쉬운데?", KEY_DESC: "싱글 플레이어 대전에서 10턴 안에 승리하여 업적 달성!", },
            Achivement.SINGLE_WIN_NO_SKILL:
                {KEY_NAME: "핸디캡 줘도 이기네ㅋ", KEY_DESC: "기술 카드를 단 한 번도 사용하지 않고 승리하여 업적 달성!", },
            Achivement.STORY_A:
                {KEY_NAME: "스토리모드 A 승리", KEY_DESC: "스토리모드 A 대전에서 승리하여 업적 달성!", },
            Achivement.STORY_B:
                {KEY_NAME: "스토리모드 B 승리", KEY_DESC: "스토리모드 B 대전에서 승리하여 업적 달성!", },
            Achivement.STORY_C:
                {KEY_NAME: "스토리모드 C 승리", KEY_DESC: "스토리모드 C 대전에서 승리하여 업적 달성!", },
            Achivement.STORY_D:
                {KEY_NAME: "스토리모드 D 승리", KEY_DESC: "스토리모드 D 대전에서 승리하여 업적 달성!", },
            Achivement.SINGLE_WIN_UNO:
                {KEY_NAME: "이걸 역전하네?!", KEY_DESC: "다른 플레이어가 UNO를 선언한 뒤에 승리하여 업적 달성!", },
            Achivement.SINGLE_LOSE_UNO:
                {KEY_NAME: "이걸 역전당하네..", KEY_DESC: "내가 UNO를 선언한 뒤에 패배하여 업적 달성!", },
            Achivement.SINGLE_UNO_CNT:
                {KEY_NAME: "순발력 좋은데?", KEY_DESC: "상대보다 UNO 먼저 선언한 횟수", }
        }

    def draw(self, screen):
        screen.fill(COLOR_WHITE)

        self.draw_title(screen)
        self.draw_scroll_surface(screen)


    def draw_title(self, screen):
        title = get_large_font().render('업적', True, COLOR_BLACK)
        title_rect = get_rect(title, screen.get_width() // 2, get_medium_margin())
        self.title_rect = screen.blit(title, title_rect)

    def draw_scroll_surface(self, screen):
        self.scroll_surface = pygame.Surface(size=(screen.get_width(), screen.get_height() - self.title_rect.bottom))
        self.scroll_surface.fill(COLOR_WHITE)
        self.draw_achievements(self.scroll_surface)

        screen.blit(self.scroll_surface, (0, self.title_rect.bottom))

    def draw_achievements(self, screen):

        temp_topleft = (0, get_medium_margin())
        for item in self.info.keys():
            self.draw_item(screen, item, (temp_topleft[0], temp_topleft[1] - self.scroll_y))

            temp_topleft = (0, temp_topleft[1] + ITEM_HEIGHT)

        self.scroll_max = temp_topleft[1] - screen.get_height() + get_medium_margin()

    def draw_item(self, screen, achivement, topleft):
        data = self.achivementsUtil.get(achivement.name)

        # 아이콘
        file_name = achivement.value + ('_disabled' if not data[PREF_ACQUIRED] else '')
        resource = f'resource\\achivement\\{file_name}.png'
        item = pygame.image.load(os.path.join(ROOT, resource))
        item = pygame.transform.scale(item, (ITEM_WIDTH, ITEM_HEIGHT))
        screen.blit(item, topleft)

        # 날짜
        if data[PREF_ACQUIRED]:
            date = get_small_font().render(data[PREF_TIMIESTAMP][:11], True, COLOR_BLACK)
            screen.blit(date, ((ITEM_WIDTH - date.get_width()) // 2, topleft[1] + ITEM_HEIGHT - date.get_height()))

        # 제목
        name = get_medium_font().render(self.info[achivement][KEY_NAME], True, COLOR_BLACK)
        screen.blit(name, (topleft[0] + ITEM_WIDTH + get_medium_margin(), topleft[1] + get_extra_small_margin()))

        #  설명
        temp_y = topleft[1] + name.get_height() + get_medium_margin()
        for line in wrap_text('설명: ' + self.info[achivement][KEY_DESC], get_medium_font(), screen.get_width() - ITEM_WIDTH - get_medium_margin()):
            description = get_medium_font().render(line, True, COLOR_BLACK)
            screen.blit(description, (topleft[0] + ITEM_WIDTH + get_medium_margin(), temp_y))
            temp_y += description.get_height()

    def run_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.run_key_event(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.run_scroll_event(event)


    def run_scroll_event(self, event):
        if event.button == SCROLL_UP:  # 위로 스크롤
            if self.scroll_y - self.scroll_speed >= 0:
                self.scroll_y -= self.scroll_speed
        elif event.button == SCROLL_DOWN:  # 아래
            if self.scroll_y + self.scroll_speed <= self.scroll_max:
                self.scroll_y += self.scroll_speed

    def run_key_event(self, event):
        pass

