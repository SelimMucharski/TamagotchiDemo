import pygame
import pygame_gui
from utils import *
import utils
from Pet import PetSprite, ShadowSprite, Pet
import Food
from Effects import *
from Settings import SettingsMenu

import threading
from database import DatabaseManager, run_db_loop
import asyncio

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
manager = manager = pygame_gui.UIManager(
    (SCREEN_WIDTH, SCREEN_HEIGHT), "theme.json")

clock = pygame.time.Clock()

utils.db = DatabaseManager(SUPABASE_URL, SUPABASE_KEY)
threading.Thread(target=run_db_loop, args=(utils.db,), daemon=True).start()

all_sprites = pygame.sprite.Group()
foods = pygame.sprite.Group()
pet = Pet(0, 0)
all_sprites.add(ShadowSprite(pet), PetSprite(pet))

menu = SettingsMenu(manager)
background = pygame.transform.scale(pygame.image.load(
    "assets/background/background.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))


health_levels = [pygame.transform.scale(pygame.image.load(
    f"assets/health/tile{i:03d}.png").convert_alpha(), (40, 40)) for i in range(6)]

fly_effect_tmp_variable = 0

run = True
while run:
    time_delta = clock.tick(8) / 1000.0

    try:
        task = utils.db.event_queue.get_nowait()
        print(f"Zadanie z bazy! {task}")
        utils.FOOD_TO_GIVE += 1
        menu.update_info()
    except asyncio.QueueEmpty:
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        manager.process_events(event)

        menu_handled = menu.handle_event(event)

        if not menu_handled and event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if not manager.get_focus_set():
                world_x, world_y = screen_to_word(*pos)

                if utils.ITEM_CHOSEN is not None:
                    food = Food.Food(world_x, world_y,
                                     f'assets/food/tile{utils.ITEM_CHOSEN:03d}.png')
                    all_sprites.add(food)
                    foods.add(food)

                    utils.ITEM_CHOSEN = None
                    utils.FOOD_TO_GIVE -= 1

                    menu.update_info()

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

    hits = pygame.sprite.spritecollide(
        all_sprites.sprites()[1], foods, True)
    for f in hits:
        pet.eat(f)

    screen.blit(background, (0, 0))

    for i in range(utils.MAX_HEALTH):
        if utils.HEALTH_LEVEL >= i + 1:
            level = 5
        elif int(utils.HEALTH_LEVEL) + 1 < i + 1:
            level = 0
        else:
            rest = utils.HEALTH_LEVEL - int(utils.HEALTH_LEVEL)

            level = int(rest * 6)

        screen.blit(health_levels[level],
                    (SCREEN_WIDTH-(utils.MAX_HEALTH - i)*40 - 10, 70))

    if utils.HEALTH_LEVEL < utils.MOOD_TRESHOLD:
        fly_effect_tmp_variable += 1
        addFlyToPet(
            all_sprites, pet) if fly_effect_tmp_variable % 10 == 0 else None

    all_sprites.draw(screen)
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
