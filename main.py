import pygame
from PIL import Image, ImageSequence
import sys

# --- KONFIGURACJA ---
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
            pygame_surface = pygame.transform.scale(pygame_surface, (300, 300))
            frames.append(pygame_surface)
        return frames
    except FileNotFoundError:
        # Fallback jeśli nie masz pliku - tworzy kolorowy kwadrat
        surf = pygame.Surface((300, 300))
        surf.fill((200, 200, 200))
        return [surf]

# Załaduj animacje (upewnij się, że pliki istnieją lub zmień nazwy)
animations = {
    "IDLE": load_gif("idle.gif"),
    "EAT": load_gif("eat.gif"),
    "SLEEP": load_gif("sleep.gif"), # Twój nowy GIF
    "SAD": load_gif("idle.gif")
}

class Pet:
    def __init__(self):
        # ZMIANA: Zaczynamy od spania
        self.state = "SLEEP"
        self.hunger = 80.0
        self.happiness = 50.0
        
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 200 # Wolniejsza animacja dla spania
        
        # Pozycja stworka (środek)
        self.rect = animations[self.state][0].get_rect(center=(WIDTH//2, HEIGHT//2))

    def update(self, dt):
        # Jeśli śpi, statystyki spadają wolniej lub wcale
        if self.state == "SLEEP":
            self.hunger -= 0.1 * dt
            self.animation_speed = 33 # Spokojny oddech
        else:
            self.hunger -= 1.0 * dt
            self.happiness -= 0.5 * dt
            self.animation_speed = 33

        # Logika powrotu do IDLE po jedzeniu
        if self.state == "EAT" and self.current_frame >= len(animations["EAT"]) - 1:
            self.state = "IDLE"

        # Animacja
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(animations[self.state])
            self.last_update = now

    def draw(self, surface):
        img = animations[self.state][self.current_frame]
        surface.blit(img, self.rect)

    def handle_click(self, pos):
        # Sprawdzamy czy kliknięto bezpośrednio w stworka
        if self.rect.collidepoint(pos):
            if self.state == "SLEEP":
                print("Pobudka!")
                self.state = "IDLE"
                self.current_frame = 0
            elif self.state == "IDLE":
                self.happiness = min(100, self.happiness + 5)
                print("Głaskanie :)")

    def feed(self):
        if self.state != "SLEEP": # Nie można karmić przez sen!
            self.state = "EAT"
            self.current_frame = 0
            self.hunger = min(100, self.hunger + 20)
        else:
            print("Stworek śpi, nie zje teraz.")

# --- GŁÓWNA PĘTLA ---
pou = Pet()
font = pygame.font.SysFont("Arial", 24)

while True:
    dt = clock.tick(60) / 1000
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 1. Próba interakcji ze stworkiem (pobudka/głaskanie)
            pou.handle_click(event.pos)
            
            # 2. Przycisk karmienia (na dole ekranu)
            if event.pos[1] > 520:
                pou.feed()

    pou.update(dt)
    pou.draw(screen)

    # Interfejs
    status_color = (200, 0, 0) if pou.state == "SLEEP" else (0, 150, 0)
    info = font.render(f"STATUS: {pou.state} | GŁÓD: {int(pou.hunger)}%", True, status_color)
    screen.blit(info, (20, 20))
    
    if pou.state == "SLEEP":
        hint = font.render("KLIKNIJ NA STWORKA, ABY GO OBUDZIĆ", True, (100, 100, 100))
        screen.blit(hint, (WIDTH//2 - 180, 150))

    # Przycisk
    pygame.draw.rect(screen, (50, 50, 50), (0, 520, WIDTH, 80))
    btn_text = font.render("DAJ JEŚĆ", True, (255, 255, 255))
    screen.blit(btn_text, (WIDTH//2 - 40, 545))

    pygame.display.flip()