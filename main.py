import pygame
import sys

# Inicjalizacja
pygame.init()
WIDTH, HEIGHT = 480, 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- 1. Tło ---
# (Zakładamy, że bg_layers jest już wczytane jak wcześniej)
bg_layers = [pygame.transform.scale(pygame.image.load(f'assets/{i}.png').convert_alpha(), (WIDTH, HEIGHT)) 
             for i in [1, 3, 4, 5]]

# --- 2. Spritesheet śpiącego zwierzaka ---
sheet = pygame.image.load('assets/sleep.png').convert_alpha()
FRAME_SIZE = 800 # Rozmiar jednej klatki (kwadratu)
COLS = 5

# Wydzielanie klatek do listy
frames = []
for y in range(0, 24000, FRAME_SIZE*20):
    for x in range(0, 4000, FRAME_SIZE):
        frames.append(sheet.subsurface(pygame.Rect(x, y, FRAME_SIZE, FRAME_SIZE)))

# Ustawienia animacji
current_frame = 0
animation_speed = 5 # Co ile klatek gry zmieniać obrazek
frame_counter = 0

# Skalowanie zwierzątka (np. do 100x100 pikseli)
PET_SIZE = 100
scaled_frames = [pygame.transform.smoothscale(f, (PET_SIZE, PET_SIZE)) for f in frames]

# Pozycja na środku
pet_x = (WIDTH - PET_SIZE) // 2
pet_y = HEIGHT - 100

# Tekst
font = pygame.font.SysFont('arial', 20, bold=True)
text_surf = font.render("Dni w porządku: 5 dni", True, (255, 255, 255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Rysowanie ---
    # Tło
    for layer in bg_layers:
        screen.blit(layer, (0, 0))
    
    # Animacja
    frame_counter += 1
    if frame_counter >= animation_speed:
        current_frame = (current_frame + 1) % len(scaled_frames)
        frame_counter = 0
    
    screen.blit(scaled_frames[current_frame], (pet_x, pet_y))
    
    # Tekst
    screen.blit(text_surf, (WIDTH - 250, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
