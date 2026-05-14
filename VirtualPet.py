import pygame
from enum import Enum

class State(Enum):
    SLEEP = 1
    IDLE = 2
    SAD = 3
    EAT = 4

class Pet:
    def __init__(self):
        self.state = State.IDLE
        self.hunger = 80.0
        self.happiness = 50.0

    def update_stats(self, dt):
        if self.state == State.SLEEP:
            self.hunger -= 0.1 * dt
        else:
            self.hunger -= 1.0 * dt
            self.happiness -= 0.5 * dt
        
        # Logika zmiany stanów
        if self.hunger < 30 and self.state == State.IDLE:
            self.state = State.SAD
        elif self.hunger >= 30 and self.state == State.SAD:
            self.state = State.IDLE

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
        try:
            self.font = pygame.font.SysFont("Verdana", 18, bold=True)
        except:
            self.font = pygame.font.Font(None, 22)

    def _get_animation_speed(self, state):
        return 100 if state == State.SLEEP else self.fps_ms

    def _draw_status_bar(self, surface, x, y, value, label_text, color):
        txt = self.font.render(label_text, True, (50, 50, 50))
        surface.blit(txt, (x, y))
        bar_x = x + 70
        pygame.draw.rect(surface, (200, 200, 200), (bar_x, y + 2, 120, 18), border_radius=5)
        fill_w = max(0, (min(100, value) / 100) * 120)
        pygame.draw.rect(surface, color, (bar_x, y + 2, fill_w, 18), border_radius=5)

    def draw_ui(self, surface, pet):
        # Pasek górny
        pygame.draw.rect(surface, (230, 230, 230), (0, 0, surface.get_width(), 50))
        pygame.draw.line(surface, (200, 200, 200), (0, 50), (surface.get_width(), 50), 2)
        
        self._draw_status_bar(surface, 15, 15, pet.hunger, "GŁÓD", (255, 87, 51))
        self._draw_status_bar(surface, 245, 15, pet.happiness, "FUN", (51, 165, 255))

    def draw(self, surface, pet):
        if pet.state != self.last_state:
            self.current_frame = 0
            self.last_state = pet.state

        now = pygame.time.get_ticks()
        speed = self._get_animation_speed(pet.state)
        
        if now - self.last_update > speed:
            self.current_frame = (self.current_frame + 1) % len(self.animations[pet.state])
            self.last_update = now

        img = self.animations[pet.state][self.current_frame]
        # Wyśrodkowanie na ekranie 480x320
        rect = img.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 30))
        surface.blit(img, rect)
        return rect