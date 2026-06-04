import pygame
from config import *
from utils import *

from Pet import Pet, ShadowSprite
from Food import Food, RandomFood

from Effects import addHeartToPet


class World:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.all_sprites = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()

        self.pet = Pet(0, 0, self)

        shadow = ShadowSprite(self.pet)

        self.all_sprites.add(shadow)
        self.all_sprites.add(self.pet)

        self.HEART_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.HEART_EVENT, 500)

        background_image = pygame.image.load(
            "assets/background/background.png").convert()

        self.background_surface = pygame.transform.scale(
            background_image, (self.screen.get_width(), self.screen.get_height()))

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == self.HEART_EVENT:
                    addHeartToPet(self.all_sprites, self.pet)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    screen_x, screen_y = pygame.mouse.get_pos()
                    x, y = screen_to_word(screen_x, screen_y)
                    food_entity = RandomFood(x, y)
                    self.all_sprites.add(food_entity)
                    self.foods.add(food_entity)

                if event.type == pygame.FINGERDOWN:
                    if event.x == 0 and event.y == 0:
                        continue

                    screen_x = (1-event.y) * self.screen.get_width()
                    screen_y = event.x * self.screen.get_height()
                    x, y = screen_to_word(screen_x, screen_y)
                    self.screen.all_sprites.add(Food.RandomFood(x, y))
                    self.screen.foods.add(food_entity)

                hits = pygame.sprite.spritecollide(
                    self.pet,
                    self.foods,
                    True
                )

                for food in hits:
                    # pet.eat(food)
                    pass

                self.all_sprites.update()

                self.screen.blit(self.background_surface, (0, 0))
                self.all_sprites.draw(self.screen)

            pygame.display.flip()
