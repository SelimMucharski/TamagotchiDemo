import pygame
from utils import *
from Pet import PetSprite, ShadowSprite
from Background import Background
import random

from Effects import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello Clean")

clock = pygame.time.Clock()
FPS = 24


def addHeartToPet(sprites, pet):
    sprites.add(
        FlyEffect(
            pet.pos.x + random.uniform(-10, 10),
            pet.pos.y + pet.size + random.uniform(-10, 10) - 10
        )
    )


all_sprites = pygame.sprite.Group()

background = Background()

pet = PetSprite(pygame.Vector2(0, 0))

shadow = ShadowSprite(pet)

all_sprites.add(background)
all_sprites.add(shadow)
all_sprites.add(pet)
all_sprites.remove()

HEART_EVENT = pygame.USEREVENT + 1

pygame.time.set_timer(HEART_EVENT, 500)


run = True
while run:
    clock.tick(FPS)

    screen.fill("cyan")

    all_sprites.update()

    all_sprites.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == HEART_EVENT:
            addHeartToPet(all_sprites, pet)

    pygame.display.flip()

pygame.quit()
