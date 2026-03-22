import pygame
from constants import *
import math


class Enemy:
    def __init__(self, x, y, enemy_type, enemy_assets, speed=DEFAULT_ENEMY_SPEED):
        self.x     = x
        self.y     = y
        self.speed = speed

        self.frames          = enemy_assets[enemy_type]
        self.frame_index     = 0
        self.animation_timer = 0
        self.animation_speed = 8
        self.image           = self.frames[self.frame_index]
        self.rect            = self.image.get_rect(center=(self.x, self.y))

        self.enemy_type  = enemy_type
        self.facing_left = False

        # TODO: Define knockback properties
        self.knockback_distance_remaining = 0
        self.knockback_direction_x        = 0
        self.knockback_direction_y        = 0

        # look up max health for this enemy type, default to 1 if missing
        self.max_health = ENEMY_HEALTH.get(enemy_type, 1)
        self.health     = self.max_health

    def move_toward_player(self, player):

        # direction vector toward the player
        delta_x  = player.x - self.x
        delta_y  = player.y - self.y
        distance = (delta_x**2 + delta_y**2) ** 0.5

        if distance != 0:
            self.x += (delta_x / distance) * self.speed
            self.y += (delta_y / distance) * self.speed

        self.facing_left = delta_x < 0

        self.rect.center = (self.x, self.y)

    def apply_knockback(self):

        step = min(ENEMY_KNOCKBACK_SPEED, self.knockback_distance_remaining)
        self.knockback_distance_remaining -= step

        self.x += self.knockback_direction_x * step
        self.y += self.knockback_direction_y * step

        self.facing_left = self.knockback_direction_x < 0

        self.rect.center = (self.x, self.y)

    def set_knockback(self, player_x, player_y, distance):

        delta_x = self.x - player_x
        delta_y = self.y - player_y
        length  = math.sqrt(delta_x * delta_x + delta_y * delta_y)

        if length != 0:
            self.knockback_direction_x        = delta_x / length
            self.knockback_direction_y        = delta_y / length
            self.knockback_distance_remaining = distance

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def animate(self):

        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index     = (self.frame_index + 1) % len(self.frames)
            saved_centre         = self.rect.center
            self.image           = self.frames[self.frame_index]
            self.rect            = self.image.get_rect()
            self.rect.center     = saved_centre

    def draw(self, surface):

        if self.facing_left:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

        # only show the health bar once the enemy has taken some damage
        if self.health < self.max_health:
            bar_left = self.rect.centerx - HEALTH_BAR_WIDTH // 2
            bar_top  = self.rect.top - HEALTH_BAR_OFFSET

            # empty bar background
            pygame.draw.rect(surface, (80, 0, 0), (bar_left, bar_top, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))

            # filled portion representing current health
            fill_width = int(HEALTH_BAR_WIDTH * (self.health / self.max_health))
            pygame.draw.rect(surface, (200, 30, 30), (bar_left, bar_top, fill_width, HEALTH_BAR_HEIGHT))

    def update(self, player):
        # knockback takes priority - don't move toward the player while being pushed
        if self.knockback_distance_remaining > 0:
            self.apply_knockback()
        else:
            self.move_toward_player(player)
        self.animate()