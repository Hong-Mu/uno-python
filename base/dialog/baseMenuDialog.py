from base.dialog.base import BaseDialog
from util.globals import *



class BaseMenuDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.menu_idx = 0
        self.menus = None

    def draw(self, screen):
        super().draw(screen)
        # background
        layout = pygame.draw.rect(screen, COLOR_WHITE, ((screen.get_width() - self.width) // 2, (screen.get_height() - self.height) // 2, self.width, self.height))

        # background outline
        pygame.draw.rect(screen, COLOR_BLACK, ((screen.get_width() - self.width) // 2, (screen.get_height() - self.height) // 2, self.width, self.height), 1)

        # title
        title = get_large_font().render(self.title_name, True, COLOR_BLACK)
        title_rect = get_rect(title, screen.get_width() // 2, layout.y + get_medium_margin())
        screen.blit(title, title_rect)

        self.draw_menu(screen)

    def draw_menu(self, screen: pygame.Surface):
        for idx, menu in enumerate(self.menus):
            color = COLOR_GRAY if idx != self.menu_idx else COLOR_BLACK
            text = get_medium_font().render(menu['text'], True, color)
            rect = get_rect(text, screen.get_width() // 2, (screen.get_height() - (len(self.menus) * text.get_height())) // 2 + text.get_height() * idx)
            menu.update({'view': text, 'rect': rect})
            screen.blit(text, rect)

    def run_key_event(self, event):
        super().run_key_event(event)
        if event.key == pygame.K_UP:
            self.menu_idx = (self.menu_idx - 1) % len(self.menus)
        elif event.key == pygame.K_DOWN:
            self.menu_idx = (self.menu_idx + 1) % len(self.menus)
        elif event.key == pygame.K_RETURN:
            self.menus[self.menu_idx]['action']()

    def run_click_event(self, event):
        super().run_click_event(event)
        for menu in self.menus:
            if menu['rect'] and menu['rect'].collidepoint(pygame.mouse.get_pos()):
                menu['action']()

