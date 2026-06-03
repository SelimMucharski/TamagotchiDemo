import pygame
from utils import *
from Pet import PetSprite, ShadowSprite
from Background import Background
import Food

from Effects import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello Clean")

clock = pygame.time.Clock()
FPS = 60


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
#    print(clock.get_fps())
    screen.fill("cyan")

    all_sprites.update()

    all_sprites.draw(screen)

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

            print(screen_x,screen_y)

    pygame.display.flip()

pygame.quit()
