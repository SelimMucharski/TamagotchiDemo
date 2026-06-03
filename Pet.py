import random
import pygame
from utils import *
import os


class PetAnimation:
    def __init__(self, animation_path: str, len: int, file_format='png'):
        self.current_index = 0
        self.len = len
        self.images = [pygame.image.load(os.path.join(
            animation_path, f'tile{i:03d}.{file_format}')).convert_alpha() for i in range(len)]

        pass

    @property
    def image(self):
        return self.images[self.current_index]

    def update(self):
        self.current_index = (self.current_index + 1) % self.len


class PetSprite(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.vel = pygame.Vector2(0, 0)

        self.size = 100

        self.animation = PetAnimation('assets/eat', 150)

    def update(self):
        self.pos += self.vel

        self.animation.update()

    @property
    def rect(self):
        rect = self.image.get_rect()
        rect.center = to_pygame(self.pos.x, self.pos.y+rect.size[1]//2)
        return rect

    @property
    def image(self):
        return pygame.transform.scale(self.animation.image, (self.size, self.size))


class ShadowSprite(pygame.sprite.Sprite):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet

        self.image = pygame.Surface((80, 25), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (0, 0, 0, 80), self.image.get_rect())
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.centerx = self.pet.rect.centerx
        self.rect.centery = self.pet.rect.bottom - 20


class Effect(pygame.sprite.Sprite):
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
        rect.center = to_pygame(self.pos.x, self.pos.y+rect.size[1]//2)
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
