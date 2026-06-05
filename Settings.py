import pygame
import pygame_gui

from utils import *
import utils


class SettingsMenu:
    def __init__(self, manager):
        self.manager = manager
        self.expanded = False

        self.info = []

        self.food_info_label = pygame_gui.elements.UILabel(
            text=f"Jedzenie: {utils.FOOD_TO_GIVE}",
            relative_rect=pygame.Rect((10, 10), (200, 70)),
            manager=manager
        )

        self.pet_name_info_label = pygame_gui.elements.UILabel(
            text=f"{utils.PET_NAME}",
            relative_rect=pygame.Rect((10, 30), (200, 70)),
            manager=manager
        )

        self.info.append(self.food_info_label)
        self.info.append(self.pet_name_info_label)

        self.img_closed = pygame.transform.smoothscale(
            pygame.image.load("assets/gui/plus.png").convert_alpha(), (50, 50))
        self.img_opened = pygame.transform.smoothscale(
            pygame.image.load("assets/gui/cross.png").convert_alpha(), (50, 50))

        self.toggle_btn = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 60, 10), (50, 50)),
            image_surface=self.img_closed,
            manager=manager
        )

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
            btn.hide()
            self.buttons.append(btn)

    def close(self):
        self.expanded = False
        self.toggle_btn.set_image(self.img_closed)

        for i in self.info:
            i.visible = True
        for btn in self.buttons:
            btn.hide()

    def open(self):
        self.expanded = True
        self.toggle_btn.set_image(self.img_opened)

        for i in self.info:
            i.visible = False

        for btn in self.buttons:
            btn.show()

    def toggle(self):
        self.close() if self.expanded else self.open()

    def update_info(self):
        self.food_info_label.set_text(f"Jedzenie: {utils.FOOD_TO_GIVE}")
        self.pet_name_info_label.set_text(f"{utils.PET_NAME}")

        if utils.FOOD_TO_GIVE <= 0:
            self.toggle_btn.hide()
        else:
            self.toggle_btn.show()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if utils.FOOD_TO_GIVE <= 0:
                return True

            if self.toggle_btn.rect.collidepoint(pos):
                self.toggle()
                return True

            if self.expanded:
                for i, btn in enumerate(self.buttons):
                    if btn.rect.collidepoint(pos):
                        print(f"Food id: {i}")
                        utils.ITEM_CHOSEN = i
                        self.close()
                        return True
        return False
