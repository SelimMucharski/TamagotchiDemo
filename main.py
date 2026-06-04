import pygame
import pygame_gui
from utils import *
from Pet import PetSprite, ShadowSprite, Pet
import Food
from Effects import *
from Settings import SettingsMenu

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
manager = manager = pygame_gui.UIManager(
    (SCREEN_WIDTH, SCREEN_HEIGHT), "theme.json")

clock = pygame.time.Clock()

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

                if menu.ITEM_CHOSEN is not None:
                    food = Food.Food(world_x, world_y,
                                     f'assets/food/tile{menu.ITEM_CHOSEN:03d}.png')
                    all_sprites.add(food)
                    foods.add(food)

                    menu.ITEM_CHOSEN = None

        if event.type == pygame.FINGERDOWN:
            if event.x == 0 and event.y == 0:
                continue

            screen_x = (1-event.y) * screen.get_width()
            screen_y = event.x * screen.get_height()

            pygame.event.post(
                pygame.Event(
                    pygame.MOUSEBUTTONDOWN,
                    pos=(screen_x, screen_y),
                    button=0
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
