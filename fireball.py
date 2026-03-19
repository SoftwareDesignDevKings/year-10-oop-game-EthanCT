from constants import *
import pygame
import math

class Fireball:
    def __init__(self, x, y, vx, vy, size, image, damage=FIREBALL_BASE_DAMAGE):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size

        # damage dealt on hit - comes from the player's fireball_damage stat
        self.damage = damage

        self.base_image = pygame.transform.scale(image, (size, size))
        self.rotated_image = self.base_image
        self.rect = self.base_image.get_rect(center=(self.x, self.y))

        # stores recent positions so we can draw the fading trail behind it
        self.trail_positions = []

    def update(self):

        # save position before moving so the trail lags behind correctly
        self.trail_positions.append((self.x, self.y))
        if len(self.trail_positions) > FIREBALL_TRAIL_LENGTH:
            self.trail_positions.pop(0)

        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)

        # rotate the sprite to face the direction of travel
        angle = -math.degrees(math.atan2(self.vy, self.vx))
        self.rotated_image = pygame.transform.rotate(self.base_image, angle)
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    def draw(self, surface):

        # draw the trail as a series of shrinking, fading orange circles
        trail_count = len(self.trail_positions)
        for i, (tx, ty) in enumerate(self.trail_positions):

            # older positions are smaller and more transparent
            progress = (i + 1) / trail_count
            alpha    = int(200 * progress)
            radius   = max(2, int((self.size // 4) * progress))

            # use a temp surface so we can set alpha per particle
            trail_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, (255, 120, 20, alpha),
                               (radius, radius), radius)
            surface.blit(trail_surf, (int(tx) - radius, int(ty) - radius))

        surface.blit(self.rotated_image, self.rect)