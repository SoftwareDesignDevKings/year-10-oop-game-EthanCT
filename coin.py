from constants import *
import pygame
import math

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (7, 7), 7)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, player_x, player_y):
        # slide toward the player if they're within the magnet radius
        delta_x  = player_x - self.x
        delta_y  = player_y - self.y
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        if distance < COIN_MAGNET_RADIUS and distance != 0:
            self.x += (delta_x / distance) * COIN_MAGNET_SPEED
            self.y += (delta_y / distance) * COIN_MAGNET_SPEED
            self.rect.center = (int(self.x), int(self.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)