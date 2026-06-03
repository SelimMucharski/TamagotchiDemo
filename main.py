import pygame
from utils import *
from Pet import PetSprite, ShadowSprite
from Background import Background

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Groups")

clock = pygame.time.Clock()
FPS = 24


all_sprites = pygame.sprite.Group()

background = Background()

pet = PetSprite(pygame.Vector2(0, 0))

shadow = ShadowSprite(pet)

all_sprites.add(background)
all_sprites.add(shadow)
all_sprites.add(pet)

run = True
while run:

    clock.tick(FPS)

    screen.fill("cyan")

    all_sprites.update()

    all_sprites.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
