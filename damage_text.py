import pygame
from constants import *


# spawned whenever an enemy takes a hit - floats upward and fades out over
# DAMAGE_TEXT_LIFETIME frames, then marks itself as expired so Game can remove it

class DamageText:
    def __init__(self, x, y, amount, font):
        self.x      = float(x)
        self.y      = float(y)
        self.amount = amount
        self.font   = font

        self.lifetime     = DAMAGE_TEXT_LIFETIME
        self.max_lifetime = DAMAGE_TEXT_LIFETIME

    def update(self):
        self.y        -= DAMAGE_TEXT_RISE
        self.lifetime -= 1

    @property
    def expired(self):
        return self.lifetime <= 0

    def draw(self, surface):
        # alpha fades from fully opaque down to transparent as lifetime runs out
        alpha         = int(255 * (self.lifetime / self.max_lifetime))
        text_surface  = self.font.render(str(self.amount), True, (255, 220, 0))
        text_surface.set_alpha(alpha)
        surface.blit(text_surface, text_surface.get_rect(center=(int(self.x), int(self.y))))


# spawned whenever an enemy takes a hit - floats upward and fades out over
# DAMAGE_TEXT_LIFETIME frames, then marks itself as expired so Game can remove it

class DamageText:
    def __init__(self, x, y, amount, font):
        self.x      = float(x)
        self.y      = float(y)
        self.amount = amount
        self.font   = font

        self.lifetime     = DAMAGE_TEXT_LIFETIME
        self.max_lifetime = DAMAGE_TEXT_LIFETIME

    def update(self):
        self.y        -= DAMAGE_TEXT_RISE
        self.lifetime -= 1

    @property
    def expired(self):
        return self.lifetime <= 0

    def draw(self, surface):
        # alpha fades from fully opaque down to transparent as lifetime runs out
        alpha         = int(255 * (self.lifetime / self.max_lifetime))
        text_surface  = self.font.render(str(self.amount), True, (255, 220, 0))
        text_surface.set_alpha(alpha)
        surface.blit(text_surface, text_surface.get_rect(center=(int(self.x), int(self.y))))