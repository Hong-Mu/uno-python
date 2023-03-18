from util.globals import *
from player import Player
class PlayScreen:

    def __init__(self, controller):
        self.ctr = controller

        self.init_my_cards_layout(self.ctr.screen)
        self.init_board_layout(self.ctr.screen)
        self.init_players_layout(self.ctr.screen)
        self.init_escape_dialog(self.ctr.screen)

    # 나의 카드 레이아웃 초기화
    def init_my_cards_layout(self, screen):
        self.my_cards_layout_height = screen.get_height() // 5

    # 보드 레이아웃 초기화
    def init_board_layout(self, screen):
        self.board_layout_height = screen.get_height() - self.my_cards_layout_height

    # 플레이어 레이아웃 초기화
    def init_players_layout(self, screen):
        self.players_layout_width = 200

    # 일시정지 다이얼로그 초기화
    def init_escape_dialog(self, screen):
        self.escape_dialog_enabled = False

        self.escape_dialog_width = 500
        self.escape_dialog_height = 300

        self.escape_menu_index = 0 
        self.esacpe_menus = [
            {'text': '설정', 'view': None, 'rect': None, 'action': lambda: self.ctr.set_screen(TYPE_SETTING) }, 
            {'text': '종료', 'view': None, 'rect': None, 'action': lambda: (
                    self.init(),
                    self.ctr.set_screen(TYPE_START) 
                )
            }
        ]

    # 초기화 함수 (게임 종료 후 다시 들어왔을 때 호출)
    def init(self):
        self.escape_dialog_enabled = False
        self.escape_menu_index = 0

    # 모든 View
    def draw(self, screen):
        screen.fill(COLOR_WHITE)

        self.draw_board_layout(screen)
        self.draw_my_cards_layout(screen)

        # 임시 플레이어 생성
        players = [Player([1, 2, 3]), Player([1, 2, 3]), Player([1, 2, 3]), Player([1, 2, 3]), Player([1, 2, 3])]
        self.draw_players_layout(screen, players)

        if self.escape_dialog_enabled:
            self.draw_escpe_dialog_layout(screen)

    # 이벤트 처리 함수
    def process_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.process_key_event(event.key)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.process_click_event(pygame.mouse.get_pos())

    # 키보드 입력 이벤트 처리
    def process_key_event(self, key):
        if key == pygame.K_ESCAPE:
            self.toggle_escape_dialog()

        if self.escape_dialog_enabled:
            self.run_esacpe_key_event(key)

    # 일시정지 메뉴 키 이벤트
    def run_esacpe_key_event(self, key):
        if key == pygame.K_UP:
            self.escape_menu_index = (self.escape_menu_index - 1) % len(self.esacpe_menus)
        elif key == pygame.K_DOWN:
            self.escape_menu_index = (self.escape_menu_index + 1) % len(self.esacpe_menus)
        elif key == pygame.K_RETURN:
            self.esacpe_menus[self.escape_menu_index]['action']()

    # 클릭 이벤트
    def process_click_event(self, pos):
        if self.escape_dialog_enabled:
            self.run_esacpe_click_event(pos)

    # 일시정지 메뉴 클릭 이벤트
    def run_esacpe_click_event(self, pos):
        for menu in self.esacpe_menus:
            if menu['rect'] and menu['rect'].collidepoint(pos):
                menu['action']()

    # 다이얼로그 표시 상태 변경
    def toggle_escape_dialog(self):
        self.escape_dialog_enabled = not self.escape_dialog_enabled

    # 일시정지 다이얼로그 레이아웃
    def draw_escpe_dialog_layout(self, screen):
        # background solid
        self.escape_box = pygame.draw.rect(screen, COLOR_WHITE, ((screen.get_width() - self.escape_dialog_width) // 2, (screen.get_height() - self.escape_dialog_height) // 2, self.escape_dialog_width, self.escape_dialog_height))
        # background outline
        pygame.draw.rect(screen, COLOR_BLACK, ((screen.get_width() - self.escape_dialog_width) // 2, (screen.get_height() - self.escape_dialog_height) // 2, self.escape_dialog_width, self.escape_dialog_height), 1)

        title = get_large_font().render("일시정지", True, COLOR_BLACK)
        title_rect = get_rect(title, screen.get_width() // 2, self.escape_box.y + get_medium_margin())
        screen.blit(title, title_rect)

        self.draw_esacpe_menu(screen)
    
    # 일시정지 메뉴
    def draw_esacpe_menu(self, screen):
        for index, menu in enumerate(self.esacpe_menus):
            text = get_medium_font().render(menu['text'], True, COLOR_GRAY if  index != self.escape_menu_index else COLOR_BLACK)
            rect = get_rect(text, screen.get_width() // 2, screen.get_height() // 2 + text.get_height() * index)
            menu.update({'view': text, 'rect': rect})
            screen.blit(text, rect)

    # 보드 레이아웃
    def draw_board_layout(self, screen):
        self.board_layout = pygame.draw.rect(screen, COLOR_BOARD, (0, 0, screen.get_width() - self.players_layout_width, self.board_layout_height))

    # 나의 카드 레이아웃
    def draw_my_cards_layout(self, screen):
        self.my_cards_layout = pygame.draw.rect(screen, COLOR_MY_CARDS, (0, self.board_layout.bottom, self.board_layout.right, self.my_cards_layout_height))

    # 플레이어 목록 레이아웃
    def draw_players_layout(self, screen, players):
        self.player_layout = pygame.draw.rect(screen, COLOR_GRAY, (screen.get_width() - self.players_layout_width, 0, self.players_layout_width, screen.get_height()))
        self.draw_player(screen, players)

    # 플레이어
    def draw_player(self, screen, players):
        
        player_height = (screen.get_height() - get_small_margin() * 6) // 5

        self.player_list = []
        for idx, player in enumerate(players):
            temp = pygame.draw.rect(screen, COLOR_WHITE, (self.player_layout.left + get_small_margin(), get_small_margin() + (player_height + get_small_margin()) * idx, self.player_layout.width - get_small_margin() * 2, player_height))