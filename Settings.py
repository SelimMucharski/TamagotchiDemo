import pygame
import pygame_gui

from utils import *


class SettingsMenu:
    def __init__(self, manager):
        self.manager = manager
        self.expanded = False

        self.img_closed = pygame.transform.smoothscale(
            pygame.image.load("assets/gui/plus.png").convert_alpha(), (50, 50))
        self.img_opened = pygame.transform.smoothscale(
            pygame.image.load("assets/gui/cross.png").convert_alpha(), (50, 50))

        self.toggle_btn = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 60, 10), (50, 50)),
            image_surface=self.img_closed,
            manager=manager
        )

        self.ITEM_CHOSEN = None

        self.ICONS_TO_SELECT = 5

        self.buttons = []
        icon_paths = [
            f"assets/food/tile{i:03d}.png" for i in range(self.ICONS_TO_SELECT)]

        for i, path in enumerate(icon_paths):
            img = pygame.transform.smoothscale(
                pygame.image.load(path).convert_alpha(), (50, 50))
            btn = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(
                    (SCREEN_WIDTH - 150 - i * 60, 10), (50, 50)),
                image_surface=img,
                manager=manager
            )
            btn.hide()  # Ukrywamy na start
            self.buttons.append(btn)

    def close(self):
        self.expanded = False
        self.toggle_btn.set_image(self.img_closed)

        for btn in self.buttons:
            btn.hide()

    def open(self):
        self.expanded = True
        self.toggle_btn.set_image(self.img_opened)

        for btn in self.buttons:
            btn.show()

    def toggle(self):
        self.close() if self.expanded else self.open()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if self.toggle_btn.rect.collidepoint(pos):
                self.toggle()
                return True

            if self.expanded:
                for i, btn in enumerate(self.buttons):
                    if btn.rect.collidepoint(pos):
                        print(f"Food id: {i}")
                        self.ITEM_CHOSEN = i
                        self.close()
                        return True
        return False
