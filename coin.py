from constants import *
import pygame

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (7, 7), 7)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)