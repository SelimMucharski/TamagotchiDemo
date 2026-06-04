import pygame
from utils import *
import random


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.pos = pygame.Vector2(x, y)

        self.vel = pygame.Vector2(0, 0)

        self.acc = pygame.Vector2(0, -1)

        self.has_alerted = False

    def update(self):
        self.vel += self.acc
        self.pos += self.vel
        if self.pos.y <= 10:
            self.vel.y = 0
            self.acc.y = 0

            if not self.has_alerted:

                event = pygame.event.Event(
                    ITEM_ON_GROUND_EVENT,
                    pos=self.pos
                )

                pygame.event.post(event)

                self.has_alerted = True


class Food(Item):
    def __init__(self, x, y, texture_path):
        super().__init__(x, y)

        self.image = pygame.image.load(texture_path)

    @property
    def rect(self):
        rect = self.image.get_rect()
        rect.center = world_to_screen(self.pos.x, self.pos.y+rect.size[1]//2)
        return rect


class RandomFood(Food):
    def __init__(self, x, y):
        N_food_textures = 24

        i = random.randint(0, N_food_textures-1)

        texture_path = f'assets/food/tile{i:03d}.png'

        super().__init__(x, y, texture_path)
