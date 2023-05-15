import pygame
from settings import *


class Message(pygame.sprite.Sprite):
    def __init__(self, message, groups):
        super().__init__(groups)
        self.font = pygame.font.Font(None, 36)
        self.image = self.font.render(message, True, (255, 0, 0))
        self.rect = self.image.get_rect(center=(GAME_SCREEN_WIDTH // 2, GAME_SCREEN_HEIGHT // 2))
        self.timer = 0