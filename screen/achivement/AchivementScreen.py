import os

from util.achievementsutil import *
from util.globals import *
import pygame

KEY_NAME = "name"
KEY_DESC = "description"

ITEM_WIDTH, ITEM_HEIGHT = (100, 100)

class AchivementScreen:
    def __init__(self, screen_controller):
        self.screen_controller = screen_controller
        self.achivemenstUtil = screen_controller.achivemenstUtil

        self.title_rect = None

        self.data = {
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
        self.draw_achievements(screen)
        
        
    def draw_title(self, screen):
        title = get_large_font().render('업적', True, COLOR_BLACK)
        title_rect = get_rect(title, screen.get_width() // 2, get_medium_margin())
        self.title_rect = screen.blit(title, title_rect)

    def draw_achievements(self, screen):

        temp_topleft = (0, self.title_rect.bottom + get_medium_margin())
        for item in self.data.keys():
            self.draw_item(screen, item, temp_topleft)

            if temp_topleft[0] + ITEM_WIDTH * 2 < screen.get_width():
                temp_topleft = (temp_topleft[0] + ITEM_WIDTH, temp_topleft[1])
            else:
                temp_topleft = (0, temp_topleft[1] + ITEM_HEIGHT)





    def draw_item(self, screen, achivement, topleft):

        data = self.achivemenstUtil.get(achivement.name)
        print(data)
        file_name = achivement.value + ('_disabled' if not data[PREF_ACQUIRED] else '')

        resource = f'resource\\achivement\\{file_name}.png'
        item = pygame.image.load(os.path.join(ROOT, resource))
        item = pygame.transform.scale(item, (ITEM_WIDTH, ITEM_HEIGHT))
        screen.blit(item, topleft)

    def run_events(self, events):
        pass
