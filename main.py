import pygame
import pygame_gui

from utils import *
from Pet import PetSprite, ShadowSprite, Pet
import Food
from Effects import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

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

background_image = pygame.image.load(
    "assets/background/background.png"
).convert()

background_surface = pygame.transform.scale(
    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
)

menu_expanded = False

settings_image = pygame.image.load("assets/gui/plus.png").convert_alpha()
settings_image = pygame.transform.smoothscale(settings_image, (50, 50))

settings_icon = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((SCREEN_WIDTH - 60, 10), (50, 50)),
    image_surface=settings_image,
    manager=manager
)

menu_buttons = []

for i, text in enumerate(["Food", "Save", "Debug"]):
    btn = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect(
            (SCREEN_WIDTH - 150 - i * 60, 10),
            (50, 50)
        ),
        image_surface=settings_image,
        manager=manager
    )
    btn.hide()
    menu_buttons.append(btn)

GUI_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, 60)


def is_pointer_over_gui(x, y):
    return GUI_RECT.collidepoint(x, y)


def spawn_food(world_x, world_y):
    food_entity = Food.RandomFood(world_x, world_y)
    all_sprites.add(food_entity)
    foods.add(food_entity)


def finger_to_screen(event):
    return (
        event.x * SCREEN_WIDTH,
        event.y * SCREEN_HEIGHT
    )


run = True
while run:
    time_delta = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():

        manager.process_events(event)

        if event.type == pygame.QUIT:
            run = False

        if event.type == HEART_EVENT:
            addHeartToPet(all_sprites, pet)

        if event.type == ITEM_ON_GROUND_EVENT:
            pet.go_to(event.pos.x)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:

            if event.ui_element == menu_buttons[0]:
                print("Food")

            elif event.ui_element == menu_buttons[1]:
                print("Save")

            elif event.ui_element == menu_buttons[2]:
                print("Debug")

        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = event.pos

            # klik w ikonę settings
            if settings_icon.rect.collidepoint(mx, my):
                menu_expanded = not menu_expanded

                if menu_expanded:
                    settings_icon.set_image(pygame.image.load(
                        "assets/gui/cross.png").convert_alpha())
                else:
                    settings_icon.set_image(pygame.image.load(
                        "assets/gui/plus.png").convert_alpha())

                for btn in menu_buttons:
                    if menu_expanded:
                        btn.show()
                    else:
                        btn.hide()

                continue

            if is_pointer_over_gui(mx, my):
                continue

            world_x, world_y = screen_to_word(mx, my)
            spawn_food(world_x, world_y)

        if event.type == pygame.FINGERDOWN:

            mx, my = finger_to_screen(event)

            if settings_icon.rect.collidepoint(mx, my):
                menu_expanded = not menu_expanded

                for btn in menu_buttons:
                    if menu_expanded:
                        btn.show()
                    else:
                        btn.hide()

                continue

            if is_pointer_over_gui(mx, my):
                continue

            world_x, world_y = screen_to_word(mx, my)
            spawn_food(world_x, world_y)

    manager.update(time_delta)

    hits = pygame.sprite.spritecollide(pet_sprite, foods, True)
    for food in hits:
        pet.eat(food)

    pet.update(None)
    all_sprites.update()

    screen.blit(background_surface, (0, 0))
    all_sprites.draw(screen)

    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
