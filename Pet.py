import random
import pygame
from utils import *
import os


class PetState:
    def enter(self, pet):
        pass

    def update(self, pet, world):
        pass

    def exit(self, pet):
        pass


class WanderState(PetState):
    def enter(self, pet):
        pet.animation_name = "walk"
        self.timer = 0

    def update(self, pet, world):
        pet.pos += pet.vel

        if pet.pos.x > SCREEN_WIDTH//2 or pet.pos.x < -SCREEN_WIDTH//2:
            pet.vel.x *= -1

        if self.timer % 60 == 0:
            pet.vel.x = 0
            pet.animation_name = "idle"

        if self.timer % 60 == 30:
            pet.vel.x = random.uniform(-5, 5)
            pet.animation_name = "walk"

        self.timer += 1


class Pet:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)

        self.state = WanderState()
        self.state.enter(self)

    def update(self, world):
        self.state.update(self, world)

    def change_state(self, new_state):
        self.state.exit(self)

        self.state = new_state

        self.state.enter(self)


class PetAnimation:
    def __init__(self, animation_path: str, length: int, pet, file_format='png'):
        self.current_index = 0

        self.images = [pygame.image.load(os.path.join(
            animation_path, f'tile{i:03d}.{file_format}')).convert_alpha() for i in range(0, length, 5)]

        self.pet = pet

        pass

    @property
    def image(self):
        image = self.images[self.current_index]
        return image if self.pet.vel.x > 0 else pygame.transform.flip(image, 1, 0)

    def update(self):
        self.current_index = (self.current_index + 1) % len(self.images)
        self.current_index = (self.current_index + 1) % len(self.images)


class PetSprite(pygame.sprite.DirtySprite):
    def __init__(self, pet: Pet):
        pygame.sprite.Sprite.__init__(self)

        self.pet = pet

        self.animations = {
            "cry": PetAnimation('assets/cry', 120, pet),
            "eat": PetAnimation('assets/eat', 150, pet),
            "sleep": PetAnimation('assets/sleep', 150, pet),
            "walk": PetAnimation('assets/walk', 120, pet),
            "idle": PetAnimation('assets/idle', 1, pet)
        }

    def update(self):
        self.animations[self.pet.animation_name].update()

    @property
    def rect(self):
        rect = self.image.get_rect()
        rect.center = world_to_screen(
            self.pet.pos.x,
            self.pet.pos.y+rect.size[1]//2
        )
        return rect

    @property
    def image(self):
        return self.animations[self.pet.animation_name].image


class ShadowSprite(pygame.sprite.DirtySprite):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet

        self.image = pygame.Surface((80, 25), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (0, 0, 0, 80), self.image.get_rect())
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.centerx = self.pet.pos.x
        self.rect.centery = self.pet.pos.y - 20
