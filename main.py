import pygame
from utils import *
from Pet import PetSprite, ShadowSprite
import Food

from Effects import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello Clean")

clock = pygame.time.Clock()
FPS = 24


all_sprites = pygame.sprite.LayeredDirty()

pet = PetSprite(pygame.Vector2(0, 0))

shadow = ShadowSprite(pet)

all_sprites.add(pet)
all_sprites.add(shadow)

HEART_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(HEART_EVENT, 500)

background_image = pygame.image.load(
    "assets/background/background.png").convert()
background_surface = pygame.transform.scale(
    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


run = True
while run:
    all_sprites.clear(screen, background_surface)

    clock.tick(FPS)
    print(clock.get_fps())

    all_sprites.update()

    rects = all_sprites.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == HEART_EVENT:
            addHeartToPet(all_sprites, pet)

        if event.type == pygame.MOUSEBUTTONDOWN:
            screen_x, screen_y = pygame.mouse.get_pos()
            x, y = screen_to_word(screen_x, screen_y)
            all_sprites.add(Food.RandomFood(x, y))

        if event.type == pygame.FINGERDOWN:
            if event.x == 0 and event.y == 0:
                continue

            screen_x = (1-event.y) * screen.get_width()
            screen_y = event.x * screen.get_height()

            x, y = screen_to_word(screen_x, screen_y)
            all_sprites.add(Food.RandomFood(x, y))

            print(screen_x, screen_y)

    pygame.display.update(rects)

pygame.quit()
