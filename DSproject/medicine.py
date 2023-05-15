import pygame
from settings import *


class MedicineTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, roomNO):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.roomNO = roomNO
        self.pos = pos


class Medicine:
    def __init__(self, roomNO, pos):
        # graphics
        self.medicine_surf = pygame.image.load(r'./medicine/134.png').convert_alpha()
        self.roomNO = roomNO
        self.pos = pos

    def create_medicine_tile(self, medicine_sprites):
        MedicineTile(self.pos, self.medicine_surf, medicine_sprites, self.roomNO)
