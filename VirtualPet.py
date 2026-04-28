import pygame
from enum import Enum

class State(Enum):
    SLEEP = 1
    IDLE = 2
    SAD = 3
    EAT = 4


class Pet:
    def __init__(self):
        self.state = State.SLEEP
        self.hunger = 80.0
        self.happiness = 50.0

    def update_stats(self, dt):
        if self.state == State.SLEEP:
            self.hunger -= 0.1 * dt
        else:
            self.hunger -= 1.0 * dt
            self.happiness -= 0.5 * dt
        
        if self.hunger < 30 and self.state == State.IDLE:
            self.state = State.SAD

    def touch(self):
        if self.state == State.SLEEP:
            self.state = State.IDLE
            return True
        if self.state == State.IDLE:
            self.happiness += 2
            self.happiness = min(self.happiness, 100)

    def feed(self):
        if self.state != State.SLEEP:
            self.state = State.EAT
            self.hunger = min(100, self.hunger + 20)
            return True
        return False

class PetDrawer:
    def __init__(self, animations_dict):
        self.animations = animations_dict
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.fps_ms = 33 
        self.last_state = None
        self.font = pygame.font.SysFont("Verdana", 20, bold=True)

    def _get_animation_speed(self, state):
        return 100 if state == State.SLEEP else self.fps_ms

    def draw_ui(self, surface, pet):
        """Rysuje paski statystyk i przyciski."""
        # 1. Tło dla paska górnego
        pygame.draw.rect(surface, (230, 230, 230), (0, 0, surface.get_width(), 60))
        pygame.draw.line(surface, (200, 200, 200), (0, 60), (surface.get_width(), 60), 2)

        # 2. Pasek GŁODU
        self._draw_status_bar(surface, 20, 20, pet.hunger, "GŁÓD", (255, 87, 51))
        
        # 3. Pasek SZCZĘŚCIA
        self._draw_status_bar(surface, 250, 20, pet.happiness, "FUN", (51, 165, 255))

        # 4. Przycisk KARMIENIA na dole
        btn_rect = pygame.Rect(surface.get_width() // 2 - 100, surface.get_height() - 80, 200, 60)
        color = (100, 200, 100) if pet.state != State.SLEEP else (150, 150, 150)
        pygame.draw.rect(surface, color, btn_rect, border_radius=15)
        pygame.draw.rect(surface, (50, 50, 50), btn_rect, 3, border_radius=15) # Obramowanie
        
        txt = "NAKARM" if pet.state != State.SLEEP else "ŚPI..."
        label = self.font.render(txt, True, (255, 255, 255))
        surface.blit(label, label.get_rect(center=btn_rect.center))
        
        return btn_rect

    def _draw_status_bar(self, surface, x, y, value, label_text, color):
        """Pomocnicza funkcja do rysowania ładnych pasków."""
        # Tekst
        txt = self.font.render(label_text, True, (50, 50, 50))
        surface.blit(txt, (x, y))
        
        # Obudowa paska
        bar_x = x + 70
        pygame.draw.rect(surface, (200, 200, 200), (bar_x, y + 2, 120, 20), border_radius=5)
        # Wypełnienie paska (min 0, żeby nie rysować ujemnych)
        fill_w = max(0, (value / 100) * 120)
        pygame.draw.rect(surface, color, (bar_x, y + 2, fill_w, 20), border_radius=5)

    def draw(self, surface, pet):
        # ... (poprzednia logika rysowania stworka) ...
        if pet.state != self.last_state:
            self.current_frame = 0
            self.last_state = pet.state

        now = pygame.time.get_ticks()
        speed = self._get_animation_speed(pet.state)
        
        if now - self.last_update > speed:
            self.current_frame = (self.current_frame + 1) % len(self.animations[pet.state])
            self.last_update = now

        img = self.animations[pet.state][self.current_frame]
        rect = img.get_rect(center=(surface.get_width()//2, surface.get_height()//2))
        surface.blit(img, rect)
        return rect