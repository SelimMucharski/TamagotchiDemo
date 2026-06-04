import pygame
import pygame_gui
from utils import *
from Pet import PetSprite, ShadowSprite, Pet
import Food
from Effects import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Hello Clean")
clock = pygame.time.Clock()


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

        self.buttons = []
        icon_paths = ["assets/gui/plus.png",
                      "assets/gui/plus.png", "assets/gui/plus.png"]

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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
            pos = event.pos if event.type == pygame.MOUSEBUTTONDOWN else (
                event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT)

            if self.toggle_btn.rect.collidepoint(pos):
                self.expanded = not self.expanded
                self.toggle_btn.set_image(
                    self.img_opened if self.expanded else self.img_closed)

                for btn in self.buttons:
                    btn.show() if self.expanded else btn.hide()
                return True

            if self.expanded:
                for i, btn in enumerate(self.buttons):
                    if btn.rect.collidepoint(pos):
                        actions = ["Food", "Save", "Debug"]
                        print(f"Akcja: {actions[i]}")
                        return True
        return False


all_sprites = pygame.sprite.Group()
foods = pygame.sprite.Group()
pet = Pet(0, 0)
all_sprites.add(ShadowSprite(pet), PetSprite(pet))

menu = SettingsMenu(manager)
background = pygame.transform.scale(pygame.image.load(
    "assets/background/background.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

run = True
while run:
    time_delta = clock.tick(8) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        manager.process_events(event)

        menu_handled = menu.handle_event(event)

        if not menu_handled and event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if not manager.get_focus_set():
                world_x, world_y = screen_to_word(*pos)

                print(pos)
                print((world_x, world_y))

                food = Food.RandomFood(world_x, world_y)
                all_sprites.add(food)
                foods.add(food)

        if event.type == pygame.FINGERDOWN:
            if event.x == 0 and event.y == 0:
                continue

            screen_x = (1-event.y) * screen.get_width()
            screen_y = event.x * screen.get_height()

            pygame.event.post(
                pygame.Event(
                    pygame.MOUSEBUTTONDOWN,
                    pos=(screen_x, screen_y)
                )
            )

        if event.type == HEART_EVENT:
            addHeartToPet(all_sprites, pet)
        if event.type == ITEM_ON_GROUND_EVENT:
            pet.go_to(event.pos.x)

    manager.update(time_delta)
    pet.update(None)
    all_sprites.update()

    hits = pygame.sprite.spritecollide(all_sprites.sprites()[1], foods, True)
    for f in hits:
        pet.eat(f)

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
