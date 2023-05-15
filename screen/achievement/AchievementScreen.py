from model.achievement import Achievement
from model.screentype import ScreenType
from util.achievement import *
from util.extradata import ExtraData
from util.singletone import achievementsUtil, extraDataUtil
from util.text import wrap_text
from util.globals import *
import pygame

SCROLL_UP = 4
SCROLL_DOWN = 5

ITEM_WIDTH, ITEM_HEIGHT = (150, 150)

class AchievementScreen:
    def __init__(self, screen_controller):
        self.screen_controller = screen_controller

        self.title_rect = None
        self.return_rect = None
        self.scroll_surface = None

        self.scroll_y = 0
        self.scroll_speed = 50
        self.scroll_max = None

    def init(self):
        pass

    def on_destroy(self):
        pass

    def draw(self, screen):
        screen.fill(COLOR_WHITE)

        self.draw_title(screen)
        self.draw_return(screen)
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
        for item in ACHIEVE_INFO.keys():
            self.draw_item(screen, item, (temp_topleft[0], temp_topleft[1] - self.scroll_y))

            temp_topleft = (0, temp_topleft[1] + ITEM_HEIGHT)

        self.scroll_max = temp_topleft[1] - screen.get_height() + get_medium_margin() + 100

    def draw_return(self, screen):
        text = get_medium_font().render('돌아가기(ESC)', True, COLOR_BLACK)
        self.return_rect = screen.blit(text, (get_medium_margin(), get_medium_margin()))

    def draw_item(self, screen, achievement, topleft):
        data = achievementsUtil.get(achievement)

        # 아이콘
        file_name = achievement.value + ('_disabled' if not data[PREF_ACQUIRED] else '')
        resource = f'resource\\achievement\\{file_name}.png'
        item = pygame.image.load(os.path.join(ROOT, resource))
        item = pygame.transform.scale(item, (ITEM_WIDTH, ITEM_HEIGHT))
        screen.blit(item, topleft)

        # 우노 카운트
        if achievement == Achievement.SINGLE_UNO_CNT:
            date = get_medium_font().render(str(extraDataUtil.get(ExtraData.SINGLE_UNO_CNT)), True, COLOR_ACHIVEMENT)
            screen.blit(date, ((ITEM_WIDTH - date.get_width()) // 2, topleft[1] + (ITEM_HEIGHT - date.get_height()) // 2 + get_small_margin()))

        # 날짜
        if data[PREF_ACQUIRED]:
            date = get_small_font().render(data[PREF_TIMIESTAMP][:11], True, COLOR_BLACK)
            screen.blit(date, ((ITEM_WIDTH - date.get_width()) // 2, topleft[1] + ITEM_HEIGHT - date.get_height()))

        # 제목
        name = get_medium_font().render(ACHIEVE_INFO[achievement][KEY_NAME], True, COLOR_BLACK)
        screen.blit(name, (topleft[0] + ITEM_WIDTH + get_medium_margin(), topleft[1] + get_extra_small_margin()))

        #  설명
        temp_y = topleft[1] + name.get_height() + get_medium_margin()
        for line in wrap_text('설명: ' + ACHIEVE_INFO[achievement][KEY_DESC], get_medium_font(), screen.get_width() - ITEM_WIDTH - get_medium_margin()):
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
                self.run_return_click_event(event)


    def run_scroll_event(self, event):
        if event.button == SCROLL_UP:  # 위로 스크롤
            if self.scroll_y - self.scroll_speed >= 0:
                self.scroll_y -= self.scroll_speed
        elif event.button == SCROLL_DOWN:  # 아래
            if self.scroll_y + self.scroll_speed <= self.scroll_max:
                self.scroll_y += self.scroll_speed

    def run_return_click_event(self, event):
        if self.return_rect.collidepoint(pygame.mouse.get_pos()):
            if self.screen_controller.is_paused:
                self.screen_controller.set_screen(ScreenType.PLAY)
                self.screen_controller.is_paused = False
            else:
                self.screen_controller.set_screen(ScreenType.HOME)

    def run_key_event(self, event):
        key = event.key
        if key == pygame.K_DOWN:
            if self.scroll_y + self.scroll_speed <= self.scroll_max:
                self.scroll_y += self.scroll_speed
        elif key == pygame.K_UP:
            if self.scroll_y - self.scroll_speed >= 0:
                self.scroll_y -= self.scroll_speed
        elif key == pygame.K_ESCAPE:
            if self.screen_controller.is_paused:
                self.screen_controller.set_screen(ScreenType.PLAY)
                self.screen_controller.is_paused = False
            else:
                self.screen_controller.set_screen(ScreenType.HOME)