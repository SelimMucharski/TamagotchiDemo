import pygame
from utils import *
from Pet import PetSprite, ShadowSprite, Pet
import Food

from Effects import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello Clean")

clock = pygame.time.Clock()
FPS = 8

all_sprites = pygame.sprite.Group()
foods = pygame.sprite.Group()

pet = Pet(0, 0)

pet_sprite = PetSprite(pet)

shadow = ShadowSprite(pet)

all_sprites.add(shadow)
all_sprites.add(pet_sprite)

HEART_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(HEART_EVENT, 500)

COLLECT_EVENT = pygame.USEREVENT + 2

background_image = pygame.image.load(
    "assets/background/background.png").convert()

background_surface = pygame.transform.scale(
    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


run = True
while run:
    clock.tick(FPS)
    print(clock.get_fps())

    all_sprites.update()

    screen.blit(background_surface, (0, 0))
    all_sprites.draw(screen)

    hits = pygame.sprite.spritecollide(pet_sprite, foods, True)

    pet.update(None)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == HEART_EVENT:
            addHeartToPet(all_sprites, pet)

        if event.type == pygame.MOUSEBUTTONDOWN:
            screen_x, screen_y = pygame.mouse.get_pos()
            x, y = screen_to_word(screen_x, screen_y)
            food_entity = Food.RandomFood(x, y)

            all_sprites.add(food_entity)
            foods.add(food_entity)

        if event.type == pygame.FINGERDOWN:
            if event.x == 0 and event.y == 0:
                continue

            screen_x = (1-event.y) * screen.get_width()
            screen_y = event.x * screen.get_height()

            x, y = screen_to_word(screen_x, screen_y)
            all_sprites.add(Food.RandomFood(x, y))

            print(screen_x, screen_y)
            print(screen_x, screen_y)

    pygame.display.flip()

pygame.quit()
