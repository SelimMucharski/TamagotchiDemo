import pygame
import sys
from PIL import Image, ImageSequence

from VirtualPet import Pet, PetDrawer, State

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def load_gif(filename):
    """Rozbija GIF na listę powierzchni Pygame (Surface)."""
    try:
        pil_image = Image.open(filename)
        frames = []
        for frame in ImageSequence.Iterator(pil_image):
            frame = frame.convert("RGBA")
            pygame_surface = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            # Skalowanie opcjonalne (np. do 300x300)
            pygame_surface = pygame.transform.scale(pygame_surface, (600, 600))
            frames.append(pygame_surface)
        return frames
    except FileNotFoundError:
        # Fallback jeśli nie masz pliku - tworzy kolorowy kwadrat
        surf = pygame.Surface((300, 300))
        surf.fill((200, 200, 200))
        return [surf]

animations = {
    State.IDLE: load_gif("idle.gif"),
    State.EAT: load_gif("eat.gif"),
    State.SLEEP: load_gif("sleep.gif"),
    State.SAD: load_gif("idle.gif")
}


# Inicjalizacja klas
my_pet = Pet()
drawer = PetDrawer(animations)

# ... inicjalizacja ...
pet_rect = pygame.Rect(0, 0, 0, 0)
feed_btn_rect = pygame.Rect(0, 0, 0, 0)

while True:
    dt = clock.tick(60) / 1000 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kliknięcie w stworka
            if pet_rect.collidepoint(event.pos):
                my_pet.touch()
            
            # Kliknięcie w przycisk karmienia
            if feed_btn_rect.collidepoint(event.pos):
                my_pet.feed()

    my_pet.update_stats(dt)

    # Rysowanie tła (można dodać delikatny gradient lub kolor "pokoju")
    screen.fill((255, 253, 230)) # Kremowy żółty
    
    # Rysowanie stworka i pobranie jego pozycji
    pet_rect = drawer.draw(screen, my_pet) 
    
    # Rysowanie interfejsu i pobranie pozycji przycisku
    feed_btn_rect = drawer.draw_ui(screen, my_pet)

    pygame.display.flip()