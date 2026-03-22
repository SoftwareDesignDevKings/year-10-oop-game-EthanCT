import pygame
from constants import *
from fireball import Fireball
from enemy import Enemy
import math
import random


# Boss is separate from the regular Enemy class. It has three attack patterns:
#   1. radial burst  - fires fireballs in all directions at once
#   2. charge        - sprints toward the player every few seconds
#   3. minion spawn  - drops small enemies around itself

class Boss:
    def __init__(self, x, y, wave, image, enemy_assets, fireball_image):

        self.x = x
        self.y = y

        # health and speed both scale with wave number so later bosses hit harder
        self.max_health = BOSS_BASE_HEALTH + (wave - 1) * BOSS_HEALTH_PER_WAVE
        self.health     = self.max_health
        self.speed      = BOSS_BASE_SPEED

        # sprite loaded from final_boss.png via asset_loading
        self.image = image
        self.rect  = self.image.get_rect(center=(self.x, self.y))

        # keep references needed for spawning projectiles and minions
        self.enemy_assets   = enemy_assets
        self.fireball_image = fireball_image

        # projectiles fired by the boss, drawn and updated in Game
        self.projectiles = []

        # each timer counts up independently and fires when it hits its interval
        self.burst_timer  = 0
        self.charge_timer = 0
        self.minion_timer = 0

        # charge state - direction is locked in when the charge starts
        self.is_charging         = False
        self.charge_direction_x  = 0
        self.charge_direction_y  = 0
        self.charge_frames_left  = 0

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def _do_radial_burst(self):
        # spread BOSS_BURST_COUNT projectiles evenly around 360 degrees
        for projectile_index in range(BOSS_BURST_COUNT):
            angle      = math.radians((360 / BOSS_BURST_COUNT) * projectile_index)
            velocity_x = math.cos(angle) * BOSS_PROJECTILE_SPEED
            velocity_y = math.sin(angle) * BOSS_PROJECTILE_SPEED
            projectile = Fireball(self.x, self.y, velocity_x, velocity_y,
                                  BOSS_PROJECTILE_SIZE, self.fireball_image,
                                  damage=BOSS_PROJECTILE_DAMAGE)
            self.projectiles.append(projectile)

    def _start_charge(self, player):
        # lock direction toward the player then let update() carry it forward
        delta_x       = player.x - self.x
        delta_y       = player.y - self.y
        distance      = math.sqrt(delta_x * delta_x + delta_y * delta_y)
        if distance != 0:
            self.charge_direction_x = delta_x / distance
            self.charge_direction_y = delta_y / distance
        self.is_charging        = True
        self.charge_frames_left = BOSS_CHARGE_DURATION

    def _spawn_minions(self, enemy_list, world_index):
        # pick random enemy types from the current world's pool and drop them nearby
        enemy_pool = WORLD_ENEMY_POOLS[world_index]
        for _ in range(BOSS_MINION_COUNT):
            spawn_angle    = random.uniform(0, math.pi * 2)
            spawn_distance = random.randint(60, 120)
            spawn_x        = self.x + math.cos(spawn_angle) * spawn_distance
            spawn_y        = self.y + math.sin(spawn_angle) * spawn_distance
            enemy_type     = random.choice(enemy_pool)
            minion         = Enemy(spawn_x, spawn_y, enemy_type, self.enemy_assets)
            enemy_list.append(minion)

    def update(self, player, enemy_list, world_index):

        # movement - either charging at full speed or walking slowly toward the player
        if self.is_charging:
            self.x += self.charge_direction_x * BOSS_CHARGE_SPEED
            self.y += self.charge_direction_y * BOSS_CHARGE_SPEED
            self.charge_frames_left -= 1
            if self.charge_frames_left <= 0:
                self.is_charging = False
        else:
            delta_x  = player.x - self.x
            delta_y  = player.y - self.y
            distance = math.sqrt(delta_x * delta_x + delta_y * delta_y)
            if distance != 0:
                self.x += (delta_x / distance) * self.speed
                self.y += (delta_y / distance) * self.speed

        self.rect.center = (int(self.x), int(self.y))

        # tick all three attack timers and fire when they reach their thresholds
        self.burst_timer  += 1
        self.charge_timer += 1
        self.minion_timer += 1

        if self.burst_timer >= BOSS_BURST_INTERVAL:
            self.burst_timer = 0
            self._do_radial_burst()

        if self.charge_timer >= BOSS_CHARGE_INTERVAL and not self.is_charging:
            self.charge_timer = 0
            self._start_charge(player)

        if self.minion_timer >= BOSS_MINION_INTERVAL:
            self.minion_timer = 0
            self._spawn_minions(enemy_list, world_index)

        # update projectiles and cull anything that's left the screen
        for projectile in self.projectiles:
            projectile.update()
        self.projectiles = [
            p for p in self.projectiles
            if 0 <= p.x <= WIDTH and 0 <= p.y <= HEIGHT
        ]

    def draw(self, surface):

        surface.blit(self.image, self.rect)

        # health bar sits above the sprite, wider than regular enemy bars
        bar_left = self.rect.centerx - BOSS_BAR_WIDTH // 2
        bar_top  = self.rect.top - BOSS_BAR_OFFSET

        # dark red background
        pygame.draw.rect(surface, (80, 0, 0), (bar_left, bar_top, BOSS_BAR_WIDTH, BOSS_BAR_HEIGHT))

        # fill colour shifts from yellow (full health) toward red (low health)
        health_ratio = self.health / self.max_health
        bar_colour   = (int(255 * (1 - health_ratio)), int(200 * health_ratio), 0)
        fill_width   = int(BOSS_BAR_WIDTH * health_ratio)
        pygame.draw.rect(surface, bar_colour, (bar_left, bar_top, fill_width, BOSS_BAR_HEIGHT))

        for projectile in self.projectiles:
            projectile.draw(surface)