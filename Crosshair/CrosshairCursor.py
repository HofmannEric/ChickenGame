import pygame


class CrossCursor:
    def __init__(self):
        self.cursorImage = pygame.image.load("Crosshair/crosshair.png")
        self.cursorImage_rect = self.cursorImage.get_rect()
