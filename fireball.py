from constants import *
import pygame
import math
import random

class Fireball:
    def __init__(self, x, y, velocity_x, velocity_y, size, image, damage=FIREBALL_BASE_DAMAGE, pierce_count=0):
        self.x          = x
        self.y          = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.size       = size

        # damage dealt on hit - comes from the player's fireball_damage stat
        self.damage = damage

        # how many additional enemies this fireball can pass through before dying
        # 0 means it stops on the first enemy it hits (default behaviour)
        self.pierce_count = pierce_count

        # tracks which enemies have already been hit so we don't double-count
        self.hit_enemies = set()

        self.base_image    = pygame.transform.scale(image, (size, size))
        self.rotated_image = self.base_image
        self.rect          = self.base_image.get_rect(center=(self.x, self.y))

        # stores recent positions so we can draw the fading trail behind it
        self.trail_positions = []

        # live reference to the enemy we're currently homing toward
        # keeping the object itself (not just coords) means we follow it as it moves
        # set back to None once we're lined up or the enemy dies
        self.homing_target = None

    def redirect_toward(self, enemy):
        # store the enemy object so update() can track its position every frame
        self.homing_target = enemy

    def update(self):

        # if we have a homing target, nudge our velocity a few degrees toward it each frame
        if self.homing_target is not None:
            target_x = self.homing_target.x
            target_y = self.homing_target.y

            desired_angle = math.atan2(target_y - self.y, target_x - self.x)
            current_angle = math.atan2(self.velocity_y, self.velocity_x)

            # find the shortest angular gap between where we are and where we want to be
            # wrapping through -pi/+pi so we always turn the short way around
            angle_diff = desired_angle - current_angle
            while angle_diff >  math.pi: angle_diff -= 2 * math.pi
            while angle_diff < -math.pi: angle_diff += 2 * math.pi

            # clamp the step to PIERCE_TURN_RATE degrees so the curve looks smooth
            max_turn    = math.radians(PIERCE_TURN_RATE)
            turn_amount = max(-max_turn, min(max_turn, angle_diff))
            new_angle   = current_angle + turn_amount

            speed           = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)
            self.velocity_x = math.cos(new_angle) * speed
            self.velocity_y = math.sin(new_angle) * speed

            # clear the target once we're basically pointing at it - fly straight from here
            if abs(angle_diff) < math.radians(PIERCE_TURN_RATE):
                self.homing_target = None

        # save position before moving so the trail lags behind correctly
        self.trail_positions.append((self.x, self.y))
        if len(self.trail_positions) > FIREBALL_TRAIL_LENGTH:
            self.trail_positions.pop(0)

        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.center = (self.x, self.y)

        # rotate the sprite to face the direction of travel
        travel_angle       = -math.degrees(math.atan2(self.velocity_y, self.velocity_x))
        self.rotated_image = pygame.transform.rotate(self.base_image, travel_angle)
        self.rect          = self.rotated_image.get_rect(center=(self.x, self.y))

    def draw(self, surface):

        # draw the trail as a series of shrinking, fading orange circles
        number_of_trail_positions = len(self.trail_positions)
        for trail_index, (trail_x, trail_y) in enumerate(self.trail_positions):

            # older positions are smaller and more transparent
            fade_progress = (trail_index + 1) / number_of_trail_positions
            alpha         = int(200 * fade_progress)
            radius        = max(2, int((self.size // 4) * fade_progress))

            # use a temp surface so we can set alpha per particle
            trail_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (255, 120, 20, alpha), (radius, radius), radius)
            surface.blit(trail_surface, (int(trail_x) - radius, int(trail_y) - radius))

        surface.blit(self.rotated_image, self.rect)


class FlameParticle:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

        # random outward drift in any direction
        angle        = random.uniform(0, math.pi * 2)
        speed        = random.uniform(0.5, FLAME_PARTICLE_SPEED)
        self.vel_x   = math.cos(angle) * speed
        self.vel_y   = math.sin(angle) * speed

        self.lifetime     = FLAME_PARTICLE_LIFETIME
        self.max_lifetime = FLAME_PARTICLE_LIFETIME

        # pick a warm colour - deep red through orange to bright yellow
        red   = 255
        green = random.randint(60, 200)
        self.colour = (red, green, 0)

    def update(self):
        self.x        += self.vel_x
        self.y        += self.vel_y
        self.lifetime -= 1

    @property
    def expired(self):
        return self.lifetime <= 0

    def draw(self, surface):
        alpha        = int(255 * (self.lifetime / self.max_lifetime))
        particle_surf = pygame.Surface((FLAME_PARTICLE_SIZE, FLAME_PARTICLE_SIZE), pygame.SRCALPHA)
        r, g, b      = self.colour
        particle_surf.fill((r, g, b, alpha))
        surface.blit(particle_surf, (int(self.x), int(self.y)))