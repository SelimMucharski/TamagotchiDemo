import os
import pygame
from PIL import Image, ImageSequence

# Importujemy klasy z rozdzielonego pliku
from VirtualPet import Pet, PetDrawer, State

# --- KONFIGURACJA EKRANU ADAFRUIT (FB0) ---
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_NOMOUSE'] = '1'

WIDTH, HEIGHT = 480, 320
FB_DEVICE = "/dev/fb0"

def load_gif(filename):
    """Rozbija GIF na listę powierzchni Pygame."""
    try:
        pil_image = Image.open(filename)
        frames = []
        for frame in ImageSequence.Iterator(pil_image):
            frame = frame.convert("RGBA")
            pygame_surface = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            # Skalowanie dopasowane do 480x320
            pygame_surface = pygame.transform.scale(pygame_surface, (200, 200))
            frames.append(pygame_surface)
        return frames
    except Exception as e:
        print(f"Błąd ładowania {filename}: {e}")
        surf = pygame.Surface((200, 200))
        surf.fill((200, 200, 200))
        return [surf]

def main():
    pygame.init()
    # Tworzymy powierzchnię w pamięci (nie okno)
    screen_surf = pygame.Surface((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    # Ładowanie animacji (upewnij się, że pliki są w tym samym folderze)
    animations = {
        State.IDLE: load_gif("idle.gif"),
        State.EAT: load_gif("eat.gif"),
        State.SLEEP: load_gif("sleep.gif"),
        State.SAD: load_gif("idle.gif")
    }

    my_pet = Pet()
    drawer = PetDrawer(animations)
    
    try:
        fb = open(FB_DEVICE, "wb")
    except PermissionError:
        print("BŁĄD: Uruchom program przez 'sudo python3 main.py'")
        return

    print("Tamagotchi uruchomione na /dev/fb0. Naciśnij Ctrl+C, aby wyjść.")
    
    try:
        while True:
            dt = clock.tick(30) / 1000.0
            
            # --- LOGIKA ---
            my_pet.update_stats(dt)
            
            # Auto-karmienie dla testu wizualnego
            if my_pet.hunger < 20:
                my_pet.feed()
                # Powrót do IDLE po 2 sekundach
                pygame.time.set_timer(pygame.USEREVENT, 2000)

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if my_pet.state == State.EAT:
                        my_pet.state = State.IDLE
                    pygame.time.set_timer(pygame.USEREVENT, 0)

            # --- RYSOWANIE ---
            screen_surf.fill((255, 253, 230)) # Tło kremowe
            drawer.draw(screen_surf, my_pet)
            drawer.draw_ui(screen_surf, my_pet)

            # --- WYŚWIETLANIE (FB0) ---
            raw_data = screen_surf.convert(16).get_buffer()
            fb.seek(0)
            fb.write(raw_data)
            fb.flush()

    except KeyboardInterrupt:
        print("\nZamykanie...")
    finally:
        fb.close()
        pygame.quit()

if __name__ == "__main__":
    main()