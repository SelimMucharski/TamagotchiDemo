import pygame
import random
from utils import *


class Effect(pygame.sprite.DirtySprite):
    def __init__(self, x, y, lifetime=1000):
        super().__init__()

        self.pos = pygame.Vector2(x, y)

        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = lifetime

        # losowy ruch do góry
        vel_x = random.uniform(-1, 1)
        vel_y = random.uniform(1.5, 2.5)

        self.vel = pygame.Vector2(vel_x, vel_y)

        self.images: list

        self.animation_frame = 0

    def update(self):
        self.pos += self.vel
        self.animation_frame = (self.animation_frame + 1) % len(self.images)

        # usuń po czasie
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

    @property
    def image(self):
        return self.images[self.animation_frame]

    @property
    def rect(self):
        rect = self.image.get_rect()
        rect.center = world_to_screen(self.pos.x, self.pos.y+rect.size[1]//2)
        return rect


class HeartEffect(Effect):
    def __init__(self, x, y, lifetime=1000):
        super().__init__(x, y, lifetime)

        self.images = [pygame.image.load(
            "assets/heart/16x16.png").convert_alpha()]


class FlyEffect(Effect):
    def __init__(self, x, y, lifetime=1000):
        super().__init__(x, y, lifetime)

        self.images = [pygame.image.load(
            f"assets/fly/tile00{i}.png").convert_alpha() for i in range(3)]


def addHeartToPet(sprites, pet):
    sprites.add(
        HeartEffect(
            pet.pos.x + random.uniform(-10, 10),
            pet.pos.y + random.uniform(-10, 10) + 90
        )
    )


def addFlyToPet(sprites, pet):
    sprites.add(
        FlyEffect(
            pet.pos.x + random.uniform(-10, 10),
            pet.pos.y + random.uniform(-10, 10) + 90,
            2000
        )
    )
