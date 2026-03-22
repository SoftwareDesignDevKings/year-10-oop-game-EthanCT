import pygame
from constants import *
from fireball import Fireball
import math


class Player:
    def __init__(self, x, y, assets):
        self.x = x
        self.y = y

        self.speed           = PLAYER_SPEED
        self.animations      = assets["player"]
        self.state           = "idle"
        self.frame_index     = 0
        self.animation_timer = 0
        self.animation_speed = 8

        self.image       = self.animations[self.state][self.frame_index]
        self.rect        = self.image.get_rect(center=(self.x, self.y))
        self.facing_left = False

        self.health = 5
        self.xp     = 0
        self.level  = 1

        self.fireball_image = assets["fireball"][0]

        self.fireball_speed  = 5
        self.fireball_size   = 50
        self.fireball_count  = 1
        self.shoot_cooldown  = FIREBALL_SHOOT_COOLDOWN
        self.shoot_timer     = 0
        self.fireballs       = []

        # starts at base damage, increases through the upgrade system
        self.fireball_damage = FIREBALL_BASE_DAMAGE

        # how many extra enemies each fireball passes through (0 = stops on first hit)
        self.fireball_pierce_count = 0

    def shoot_toward_position(self, target_x, target_y):
        if self.shoot_timer < self.shoot_cooldown:
            return

        delta_x  = target_x - self.x
        delta_y  = target_y - self.y
        distance = math.sqrt(delta_x**2 + delta_y**2)
        if distance == 0:
            return

        base_velocity_x = (delta_x / distance) * self.fireball_speed
        base_velocity_y = (delta_y / distance) * self.fireball_speed

        degrees_between_fireballs = 10
        base_angle                = math.atan2(base_velocity_y, base_velocity_x)
        spread_centre_offset      = (self.fireball_count - 1) / 2

        for fireball_index in range(self.fireball_count):
            offset_from_centre = fireball_index - spread_centre_offset
            spread_angle       = math.radians(degrees_between_fireballs * offset_from_centre)
            final_angle        = base_angle + spread_angle

            final_velocity_x = math.cos(final_angle) * self.fireball_speed
            final_velocity_y = math.sin(final_angle) * self.fireball_speed

            # pass current fireball_damage and pierce_count so upgrades are reflected immediately
            fireball = Fireball(self.x, self.y, final_velocity_x, final_velocity_y,
                                self.fireball_size, self.fireball_image,
                                damage=self.fireball_damage,
                                pierce_count=self.fireball_pierce_count)

            self.fireballs.append(fireball)
        self.shoot_timer = 0

    def shoot_toward_mouse(self, mouse_position):
        mouse_x, mouse_y = mouse_position
        self.shoot_toward_position(mouse_x, mouse_y)

    def shoot_toward_enemy(self, enemy):
        self.shoot_toward_position(enemy.x, enemy.y)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def add_xp(self, amount):
        self.xp += amount

    def handle_input(self):

        keys = pygame.key.get_pressed()

        velocity_x, velocity_y = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            velocity_x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            velocity_x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            velocity_y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            velocity_y += self.speed

        self.x += velocity_x
        self.y += velocity_y

        # keep the player inside the screen
        self.x = max(0, min(self.x, WIDTH))
        self.y = max(0, min(self.y, HEIGHT))
        self.rect.center = (self.x, self.y)

        # switch animation state based on whether we're moving
        if velocity_x != 0 or velocity_y != 0:
            self.state = "run"
        else:
            self.state = "idle"

        # flip sprite based on horizontal movement direction
        if velocity_x < 0:
            self.facing_left = True
        elif velocity_x > 0:
            self.facing_left = False

    def draw(self, surface):
        if self.facing_left:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

        for fireball in self.fireballs:
            fireball.draw(surface)

    def update(self):
        # count up every frame so the shoot cooldown actually elapses
        if self.shoot_timer < self.shoot_cooldown:
            self.shoot_timer += 1

        for fireball in self.fireballs:
            fireball.update()
            if fireball.y < 0 or fireball.y > HEIGHT or fireball.x < 0 or fireball.x > WIDTH:
                self.fireballs.remove(fireball)

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            current_frames       = self.animations[self.state]
            self.frame_index     = (self.frame_index + 1) % len(current_frames)
            saved_centre         = self.rect.center
            self.image           = current_frames[self.frame_index]
            self.rect            = self.image.get_rect()
            self.rect.center     = saved_centre