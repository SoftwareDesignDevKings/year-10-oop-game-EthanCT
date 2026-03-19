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
        self.image      = image
        self.rect       = self.image.get_rect(center=(self.x, self.y))

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
        self.is_charging    = False
        self.charge_dx      = 0
        self.charge_dy      = 0
        self.charge_frames  = 0

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def _do_radial_burst(self):
        # spread BOSS_BURST_COUNT projectiles evenly around 360 degrees
        for i in range(BOSS_BURST_COUNT):
            angle = math.radians((360 / BOSS_BURST_COUNT) * i)
            vx    = math.cos(angle) * BOSS_PROJECTILE_SPEED
            vy    = math.sin(angle) * BOSS_PROJECTILE_SPEED
            proj  = Fireball(self.x, self.y, vx, vy,
                             BOSS_PROJECTILE_SIZE, self.fireball_image,
                             damage=BOSS_PROJECTILE_DAMAGE)
            self.projectiles.append(proj)

    def _start_charge(self, player):
        # lock direction toward the player then let update() carry it forward
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist != 0:
            self.charge_dx   = dx / dist
            self.charge_dy   = dy / dist
        self.is_charging  = True
        self.charge_frames = BOSS_CHARGE_DURATION

    def _spawn_minions(self, enemy_list, world_index):
        # pick random enemy types from the current world's pool and drop them nearby
        pool = WORLD_ENEMY_POOLS[world_index]
        for _ in range(BOSS_MINION_COUNT):
            angle  = random.uniform(0, math.pi * 2)
            dist   = random.randint(60, 120)
            mx     = self.x + math.cos(angle) * dist
            my     = self.y + math.sin(angle) * dist
            etype  = random.choice(pool)
            minion = Enemy(mx, my, etype, self.enemy_assets)
            enemy_list.append(minion)

    def update(self, player, enemy_list, world_index):

        # movement - either charging at full speed or walking slowly toward the player
        if self.is_charging:
            self.x += self.charge_dx * BOSS_CHARGE_SPEED
            self.y += self.charge_dy * BOSS_CHARGE_SPEED
            self.charge_frames -= 1
            if self.charge_frames <= 0:
                self.is_charging = False
        else:
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist != 0:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed

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
        for proj in self.projectiles:
            proj.update()
        self.projectiles = [
            p for p in self.projectiles
            if 0 <= p.x <= WIDTH and 0 <= p.y <= HEIGHT
        ]

    def draw(self, surface):

        surface.blit(self.image, self.rect)

        # health bar sits above the sprite, wider than regular enemy bars
        bar_x  = self.rect.centerx - BOSS_BAR_WIDTH // 2
        bar_y  = self.rect.top - BOSS_BAR_OFFSET

        # dark red background
        pygame.draw.rect(surface, (80, 0, 0),
                         (bar_x, bar_y, BOSS_BAR_WIDTH, BOSS_BAR_HEIGHT))

        # fill colour shifts from yellow (full health) toward red (low health)
        ratio    = self.health / self.max_health
        bar_col  = (
            int(255 * (1 - ratio)),
            int(200 * ratio),
            0
        )
        fill_w   = int(BOSS_BAR_WIDTH * ratio)
        pygame.draw.rect(surface, bar_col,
                         (bar_x, bar_y, fill_w, BOSS_BAR_HEIGHT))

        for proj in self.projectiles:
            proj.draw(surface)