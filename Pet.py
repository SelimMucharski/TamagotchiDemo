import random
import pygame
from utils import *
import os


class PetAnimation:
    def __init__(self, animation_path: str, length: int, pet, file_format='png'):
        self.current_index = 0
<<<<<<< HEAD
        self.images = [pygame.image.load(os.path.join(
            animation_path, f'tile{i:03d}.{file_format}')).convert_alpha() for i in range(0, length, 5)]

        self.len = len(self.images)
=======

        self.images = [pygame.image.load(os.path.join(
            animation_path, f'tile{i:03d}.{file_format}')).convert_alpha() for i in range(0, length, 5)]
>>>>>>> 5f49a13 (Reduced number of frames in pet animation)

        self.pet = pet

        pass

    @property
    def image(self):
        image = self.images[self.current_index]
        return image if self.pet.vel.x > 0 else pygame.transform.flip(image, 1, 0)

    def update(self):
        self.current_index = (self.current_index + 1) % len(self.images)


class PetSprite(pygame.sprite.DirtySprite):
    def __init__(self, pos: pygame.Vector2):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.vel = pygame.Vector2(3, 0)

        self.size = 100

        self.animation = PetAnimation('assets/walk', 120, pet=self)
        self.dirty = 1

        self.visible = 1
        self.blendmode = 0

        self.source_rect = None

    def update(self):
        self.pos += self.vel

        if self.pos.x < -SCREEN_WIDTH//2 or self.pos.x > SCREEN_WIDTH//2:
            self.vel.x *= -1

        self.dirty = 1

        self.animation.update()

    @property
    def rect(self):
        rect = self.image.get_rect()
        rect.center = world_to_screen(self.pos.x, self.pos.y+rect.size[1]//2)
        return rect

    @property
    def image(self):
        return pygame.transform.scale(self.animation.image, (self.size, self.size))


class ShadowSprite(pygame.sprite.DirtySprite):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet

        self.image = pygame.Surface((80, 25), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (0, 0, 0, 80), self.image.get_rect())
        self.rect = self.image.get_rect()
        self.dirty = 1

        self.visible = 1
        self.blendmode = 0

    def update(self):
        self.rect.centerx = self.pet.rect.centerx
        self.rect.centery = self.pet.rect.bottom - 20

        self.dirty = 1
