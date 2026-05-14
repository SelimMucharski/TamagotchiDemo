import os
import sys
import pygame
import datetime
from pygame.locals import *

# --- KONFIGURACJA ŚRODOWISKA ---
# Używamy sterownika 'dummy', aby Pygame nie szukało fizycznego monitora HDMI
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_NOMOUSE'] = '1'

# ---- PARAMETRY EKRANU ----
WIDTH, HEIGHT = 480, 320
FPS = 30
FB_DEVICE = "/dev/fb0"  # Skoro fbi tam zadziałało, zostawiamy fb0

# Kolory Pip-Boy
BLACK      = (  0,   0,   0)
GREEN      = (  0, 255,  70)
GREEN_DIM  = (  0, 140,  40)
GREEN_DARK = (  0,  50,  15)
BG         = (  5,  15,   5)

TABS = ["STAT", "INV", "DATA", "MAP", "RADIO"]

STATS = [("STR", 7), ("PER", 5), ("END", 6), ("CHA", 4), ("INT", 8), ("AGI", 6), ("LCK", 5)]
INVENTORY = ["Stimpak x 12", "RadAway x 3", "Nuka-Cola x 7", "10mm Ammo x 84", "Bobby Pin x 22", "Laser Pistol x 1"]

class PipBoyUI:
    def __init__(self):
        pygame.init()
        
        # Tworzymy wirtualną powierzchnię w RAM zamiast okna
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.active_tab = 0

        # Otwieramy framebuffer
        try:
            self.fb = open(FB_DEVICE, "wb")
        except PermissionError:
            print("BŁĄD: Brak uprawnień do /dev/fb0. Uruchom program przez: sudo python3 test.py")
            sys.exit()

        # Czcionki
        try:
            self.font_big   = pygame.font.SysFont("monospace", 22, bold=True)
            self.font_med   = pygame.font.SysFont("monospace", 16)
            self.font_small = pygame.font.SysFont("monospace", 13)
        except:
            self.font_big   = pygame.font.Font(None, 26)
            self.font_med   = pygame.font.Font(None, 20)
            self.font_small = pygame.font.Font(None, 16)

    def draw_text(self, text, font, color, x, y):
        surf = font.render(text, True, color)
        self.screen.blit(surf, (x, y))

    def draw_bar(self, x, y, w, h, value):
        pygame.draw.rect(self.screen, GREEN_DARK, (x, y, w, h))
        filled = int(w * value / 10)
        pygame.draw.rect(self.screen, GREEN, (x, y, filled, h))
        pygame.draw.rect(self.screen, GREEN_DIM, (x, y, w, h), 1)

    def update_display(self):
        """Wysyła dane z Pygame bezpośrednio do /dev/fb0"""
        # Konwertujemy obraz na format 16-bitowy (RGB565) - najczęstszy dla TFT
        # Jeśli kolory będą dziwne, zmień na: raw = self.screen.convert(16).get_buffer()
        raw = self.screen.convert(16).get_buffer()
        self.fb.seek(0)
        self.fb.write(raw)
        self.fb.flush()

    def render(self):
        self.screen.fill(BG)
        
        # HEADER
        pygame.draw.rect(self.screen, GREEN_DARK, (0, 0, WIDTH, 28))
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.draw_text(f"  PIP-BOY 3000          {now}", self.font_big, GREEN, 4, 4)
        
        # TABS
        tab_w = WIDTH // len(TABS)
        for i, name in enumerate(TABS):
            x = i * tab_w
            if i == self.active_tab:
                pygame.draw.rect(self.screen, GREEN_DIM, (x, 30, tab_w - 2, 24))
                self.draw_text(name, self.font_med, BLACK, x + 10, 34)
            else:
                self.draw_text(name, self.font_med, GREEN_DIM, x + 10, 34)
        
        # CONTENT (STAT example)
        y = 70
        if self.active_tab == 0:
            for name, val in STATS:
                self.draw_text(name, self.font_med, GREEN, 20, y)
                self.draw_bar(80, y + 2, 150, 12, val)
                y += 30
        else:
            self.draw_text("SEKCJA W BUDOWIE...", self.font_big, GREEN, 50, 150)

        # FOOTER
        pygame.draw.line(self.screen, GREEN_DIM, (0, HEIGHT-20), (WIDTH, HEIGHT-20), 1)
        self.draw_text(" [ KLIKNIJ ENTER ABY ZMIENIĆ ZAKŁADKĘ ] ", self.font_small, GREEN_DIM, 10, HEIGHT-18)

    def run(self):
        print("Pip-Boy uruchomiony. Naciśnij Ctrl+C w terminalu, aby wyjść.")
        running = True
        try:
            while running:
                # Ponieważ używamy 'dummy', zdarzenia klawiatury z SSH nie wejdą przez pygame.event
                # W tej wersji robimy auto-rotację zakładek co 3 sekundy dla testu wyświetlacza
                self.active_tab = (pygame.time.get_ticks() // 3000) % len(TABS)
                
                self.render()
                self.update_display()
                self.clock.tick(FPS)
        except KeyboardInterrupt:
            running = False
        
        self.fb.close()
        pygame.quit()

if __name__ == "__main__":
    ui = PipBoyUI()
    ui.run()