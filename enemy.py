import pygame
from constants import *
import math


class Enemy:
    def __init__(self, x, y, enemy_type, enemy_assets, speed=DEFAULT_ENEMY_SPEED):
        self.x = x
        self.y = y
        self.speed = speed
        
        self.frames = enemy_assets[enemy_type]
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 8
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        self.enemy_type = enemy_type 
        self.facing_left = False
        
        # TODO: Define knockback properties
        self.knockback_dist_remaining = 0
        self.knockback_dx = 0
        self.knockback_dy = 0

        # look up max health for this enemy type, default to 1 if missing
        self.max_health = ENEMY_HEALTH.get(enemy_type, 1)
        self.health     = self.max_health

    def move_toward_player(self, player):

        # direction vector toward the player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance != 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

        self.facing_left = dx < 0 

        self.rect.center = (self.x, self.y)
        pass

    def apply_knockback(self):
        
        step = min(ENEMY_KNOCKBACK_SPEED, self.knockback_dist_remaining)
        self.knockback_dist_remaining -= step

        self.x += self.knockback_dx * step
        self.y += self.knockback_dy * step

        if self.knockback_dx < 0:
            self.facing_left = True
        else:
            self.facing_left = False

        self.rect.center = (self.x, self.y)

    def set_knockback(self, px, py, dist):

        dx = self.x - px
        dy = self.y - py

        length = math.sqrt(dx*dx + dy*dy)

        if length != 0:
            self.knockback_dx = dx / length
            self.knockback_dy = dy / length
            self.knockback_dist_remaining = dist
        pass

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def animate(self):
        
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            center = self.rect.center
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = center
        pass

    def draw(self, surface):
        
        if self.facing_left:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

        # only show the health bar once the enemy has taken some damage
        if self.health < self.max_health:
            bar_x = self.rect.centerx - HEALTH_BAR_WIDTH // 2
            bar_y = self.rect.top - HEALTH_BAR_OFFSET

            # empty bar background
            pygame.draw.rect(surface, (80, 0, 0),
                             (bar_x, bar_y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))

            # filled portion representing current health
            fill_w = int(HEALTH_BAR_WIDTH * (self.health / self.max_health))
            pygame.draw.rect(surface, (200, 30, 30),
                             (bar_x, bar_y, fill_w, HEALTH_BAR_HEIGHT))

    def update(self, player):
        # knockback takes priority - don't move toward the player while being pushed
        if self.knockback_dist_remaining > 0:
            self.apply_knockback()
        else:
            self.move_toward_player(player)
        self.animate()