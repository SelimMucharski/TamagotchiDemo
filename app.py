import utils
import pygame
import os
import dotenv

import pygame_gui
from database import DatabaseManager, run_db_loop

import threading

from Pet import Pet, ShadowSprite, PetSprite

from Settings import SettingsMenu

import asyncio

from Effects import addFlyToPet, addHeartToPet

dotenv.load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


class App:
    def __init__(self):
        self.screen = None
        self.clock = None
        self.manager = None
        self.pet = None
        self.all_sprites = None
        self.foods = None
        self.menu = None

        self.db = None

    async def init(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (utils.SCREEN_WIDTH, utils.SCREEN_HEIGHT)
        )

        loading_screen = pygame.image.load(
            'assets/loading_screen/loading_screen.png')

        self.screen.blit(pygame.transform.scale(
            loading_screen, (utils.SCREEN_WIDTH, utils.SCREEN_HEIGHT)))

        pygame.display.flip()

        self.manager = pygame_gui.UIManager(
            (utils.SCREEN_WIDTH, utils.SCREEN_HEIGHT),
            "theme.json"
        )

        self.clock = pygame.time.Clock()

        self.db = DatabaseManager(SUPABASE_URL, SUPABASE_KEY)

        threading.Thread(
            target=run_db_loop,
            args=(self.db,),
            daemon=True
        ).start()

        self.all_sprites = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()

        self.pet = Pet(0, 0, self.db)

        self.all_sprites.add(
            ShadowSprite(self.pet),
            PetSprite(self.pet)
        )

        self.menu = SettingsMenu(self.manager, self.db)

        self.health_levels = [pygame.transform.scale(pygame.image.load(
            f"assets/health/tile{i:03d}.png").convert_alpha(), (40, 40)) for i in range(6)]

        self.background = pygame.transform.scale(pygame.image.load(
            "assets/background/background.png").convert(), (utils.SCREEN_WIDTH, utils.SCREEN_HEIGHT))

        pygame.time.set_timer(utils.UPDATE_PET_EVENT, 1000)

        while True:
            try:
                msg = self.db.event_queue.get_nowait()
                if msg["type"] == "ready":
                    break
            except asyncio.QueueEmpty:
                pass

        print("Init zakończony")

    async def run(self):
        run = True
        while run:
            time_delta = self.clock.tick(8) / 1000.0

            try:
                msg = self.db.event_queue.get_nowait()
                if msg['type'] == 'task_done':
                    print('New task done')
            except asyncio.QueueEmpty:
                pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                self.manager.process_events(event)

                menu_handled = self.menu.handle_event(event)

                if not menu_handled and event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos

                    if not self.manager.get_focus_set():
                        world_x, world_y = utils.screen_to_word(*pos)

                        if utils.ITEM_CHOSEN is not None:
                            import Food

                            food = Food.Food(world_x, world_y,
                                             f'assets/food/tile{utils.ITEM_CHOSEN:03d}.png')
                            self.all_sprites.add(food)
                            self.foods.add(food)

                            utils.ITEM_CHOSEN = None

                if event.type == pygame.FINGERDOWN:
                    if event.x == 0 and event.y == 0:
                        continue

                    screen_x = (1-event.y) * self.screen.get_width()
                    screen_y = event.x * self.screen.get_height()

                    pygame.event.post(
                        pygame.Event(
                            pygame.MOUSEBUTTONDOWN,
                            pos=(screen_x, screen_y),
                            button=0
                        )
                    )

                if event.type == utils.HEART_EVENT:
                    addHeartToPet(self.all_sprites, self.pet)
                if event.type == utils.ITEM_ON_GROUND_EVENT:
                    self.pet.go_to(event.pos.x)

                if event.type == utils.UPDATE_PET_EVENT:

                    energy = utils.calculate_energy(self.db)
                    mood = utils.calculateMood(energy)

                    self.db.loop.call_soon_threadsafe(
                        lambda: asyncio.create_task(
                            self.db.update_pet(energy, mood)
                        )
                    )

            self.menu.update_info()

            self.manager.update(time_delta)
            self.pet.update(None)
            self.all_sprites.update()

            hits = pygame.sprite.spritecollide(
                self.all_sprites.sprites()[1], self.foods, True)
            for f in hits:
                self.pet.eat(f)

                self.db.loop.call_soon_threadsafe(
                    lambda: asyncio.create_task(
                        utils.decreaseTasks(self.db)
                    )
                )

            self.screen.blit(self.background, (0, 0))

            health_level = utils.calculate_energy(
                self.db) / 100 * utils.MAX_HEALTH

            for i in range(utils.MAX_HEALTH):
                if health_level >= i + 1:
                    level = 5
                elif int(health_level) + 1 < i + 1:
                    level = 0
                else:
                    rest = health_level - int(health_level)

                    level = int(rest * 6)

                self.screen.blit(self.health_levels[level],
                                 (utils.SCREEN_WIDTH-(utils.MAX_HEALTH - i)*40 - 10, 70))

            # if utils.HEALTH_LEVEL < utils.MOOD_TRESHOLD:
            #     fly_effect_tmp_variable += 1
            #     addFlyToPet(
            #         self.all_sprites, self.pet) if fly_effect_tmp_variable % 10 == 0 else None

            self.all_sprites.draw(self.screen)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

        pygame.quit()
