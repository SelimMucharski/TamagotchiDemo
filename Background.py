import pygame
from utils import *


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        layers = [
            pygame.image.load("assets/1.png").convert_alpha(),
            pygame.image.load("assets/3.png").convert_alpha(),
            pygame.image.load("assets/4.png").convert_alpha(),
            pygame.image.load("assets/5.png").convert_alpha()
        ]

        width = layers[0].get_width()
        height = layers[0].get_height()

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        for layer in layers:
            layer = pygame.transform.scale(
                layer, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.image.blit(layer, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
