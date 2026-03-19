import pygame
from constants import *
from fireball import Fireball
import math


class Player:
    def __init__(self, x, y, assets):
        self.x = x
        self.y = y

        self.speed = PLAYER_SPEED
        self.animations = assets["player"]
        self.state = "idle"
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 8

        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.facing_left = False

        self.health = 5
        self.xp = 0
        self.level = 1

        self.fireball_image = assets["fireball"][0] 

        self.fireball_speed  = 10
        self.fireball_size   = 50
        self.fireball_count  = 1
        self.shoot_cooldown  = FIREBALL_SHOOT_COOLDOWN
        self.shoot_timer     = 0
        self.fireballs       = []

        # starts at base damage, increases through the upgrade system
        self.fireball_damage = FIREBALL_BASE_DAMAGE

    def shoot_toward_position(self, tx, ty):
        if self.shoot_timer >= self.shoot_cooldown:
            return

        dx = tx - self.x
        dy = ty - self.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist == 0:
            return

        vx = (dx / dist) * self.fireball_speed
        vy = (dy / dist) * self.fireball_speed

        angle_spread = 10
        base_angle = math.atan2(vy, vx)
        mid = (self.fireball_count - 1) / 2

        for i in range(self.fireball_count):
            offset = i - mid
            spread_radians = math.radians(angle_spread * offset)
            angle = base_angle + spread_radians

            final_vx = math.cos(angle) * self.fireball_speed
            final_vy = math.sin(angle) * self.fireball_speed

            # pass current fireball_damage so upgrades are reflected immediately
            fireball = Fireball(self.x, self.y, final_vx, final_vy,
                                self.fireball_size, self.fireball_image,
                                damage=self.fireball_damage)

            self.fireballs.append(fireball)
        self.shoot_timer = 0

    def shoot_toward_mouse(self, pos):
        mx, my = pos  # mx/my = mouse x/y
        self.shoot_toward_position(mx, my)

    def shoot_toward_enemy(self, enemy):
        self.shoot_toward_position(enemy.x, enemy.y)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def add_xp(self, amount):
        self.xp += amount

    def handle_input(self):

        keys = pygame.key.get_pressed()

        vel_x, vel_y = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vel_x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vel_x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vel_y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vel_y += self.speed

        self.x += vel_x
        self.y += vel_y

        # keep the player inside the screen
        self.x = max(0, min(self.x, WIDTH))
        self.y = max(0, min(self.y, HEIGHT))
        self.rect.center = (self.x, self.y)

        # switch animation state based on whether we're moving
        if vel_x != 0 or vel_y != 0:
            self.state = "run"
        else:
            self.state = "idle"

        # flip sprite based on horizontal movement direction
        if vel_x < 0:
            self.facing_left = True
        elif vel_x > 0:
            self.facing_left = False  

    def draw(self, surface):
        if self.facing_left:
            flipped_img = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_img, self.rect)
        else:
            surface.blit(self.image, self.rect)

        for fireball in self.fireballs:
            fireball.draw(surface)
    
    def update(self):
        for fireball in self.fireballs:
            fireball.update()
            if fireball.y < 0 or fireball.y > HEIGHT or fireball.x < 0 or fireball.x > WIDTH:
                self.fireballs.remove(fireball)

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            frames = self.animations[self.state]
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center