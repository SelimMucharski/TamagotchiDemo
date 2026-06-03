SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

# center of word frame of referance
WORLD_0X = SCREEN_WIDTH // 2
WORLD_0Y = SCREEN_HEIGHT - 10


def world_to_screen(x, y):
    px = x + WORLD_0X
    py = WORLD_0Y - y
    return (px, py)


def screen_to_word(px, py):
    x = px - WORLD_0X
    y = WORLD_0Y - py
    return (x, y)
