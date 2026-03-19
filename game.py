import pygame
import os
import random
from constants import *
from asset_loading import * 
from player import Player
from enemy import Enemy
import math
from coin import Coin
from button import Button
from ui_screens import *
from stats_manager    import *
from settings_manager import *
from damage_text import DamageText
from boss import Boss


class Game:
    def __init__(self):
        
        pygame.init()
        
        # window setup
        self.screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
        pygame.display.set_caption("Shooter")

        self.clock = pygame.time.Clock()
       
        self.assets = load_assets()

        # fonts
        font_path = os.path.join("assets", "PressStart2P.ttf")
        self.font_small = pygame.font.Font(font_path, 18)
        self.font_large = pygame.font.Font(font_path, 32)

        # background gets rebuilt in reset_game() with world-specific tiles
        self.background = self.create_random_background(WIDTH, HEIGHT, self.assets["floor_tiles"])

        self.running = True
        self.game_over = False

        self.enemies = []

        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 60
        self.enemies_per_spawn = 1

        self.coins = []

        self.in_level_up_menu = False
        self.upgrade_options = []

        # game state
        self.game_state = "main_menu"

        # which world is highlighted on the world select screen
        self.selected_world_index = 0

        # persistent stats and settings loaded from disk
        self.stats    = load_stats()
        self.settings = load_settings()

        # per-session counters reset each run
        self.session_kills = 0
        self.session_coins = 0

        # button dicts returned by each draw function - rebuilt every frame
        self._ui_buttons      = {}
        # upgrade card buttons - rebuilt each frame the upgrade menu is open
        self._upgrade_buttons = []

        # wave system
        self.wave_number        = 1
        self.wave_state         = "spawning"   # "spawning", "active", "cleared", "boss_active"
        self.boss               = None         # None when no boss is alive
        self.wave_announce_timer = 0
        self.wave_announce_text  = ""

        self.reset_game()

    def spawn_enemies(self):
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_interval:
            self.enemy_spawn_timer = 0

            for _ in range(self.enemies_per_spawn):
                side = random.choice(["top", "bottom", "left", "right"])
                if side == "top":
                    x = random.randint(0, WIDTH)
                    y = SPAWN_MARGIN
                elif side == "bottom":
                    x = random.randint(0, WIDTH)
                    y = HEIGHT + SPAWN_MARGIN
                elif side == "left":
                    x = -SPAWN_MARGIN
                    y = random.randint(0, HEIGHT)
                else:
                    x = WIDTH + SPAWN_MARGIN
                    y = random.randint(0, HEIGHT)

                # skip the spawn if it would be too close to the player
                distance_to_player = math.sqrt((x - self.player.x) ** 2 + (y - self.player.y) ** 2)
                if distance_to_player < MIN_SPAWN_DISTANCE_FROM_PLAYER:
                    continue

                # pick a random enemy type from this world's pool
                pool        = WORLD_ENEMY_POOLS[self.selected_world_index]
                enemy_type  = random.choice(pool)
                enemy = Enemy(x, y, enemy_type, self.assets["enemies"])
                self.enemies.append(enemy)

    def check_for_level_up(self):
        xp_needed = self.player.level * self.player.level * 5
        if self.player.xp >= xp_needed:
            self.player.level += 1
            self.in_level_up_menu = True
            self.upgrade_options = self.pick_random_upgrades(3)

            # ramp up spawns every time the player levels up
            self.enemies_per_spawn += 1

    def pick_random_upgrades(self, num):
        possible_upgrades = [
            {"name": "Bigger Fireball",  "desc": "Fireball size +5"},
            {"name": "Faster Fireball",  "desc": "Fireball speed +2"},
            {"name": "Extra Fireball",   "desc": "Fire additional fireball"},
            {"name": "Shorter Cooldown", "desc": "Shoot more frequently"},
            {"name": "More Damage",      "desc": "Fireball damage +1"},
        ]
        return random.sample(possible_upgrades, k=num)
    
    def apply_upgrade(self, player, upgrade):
        name = upgrade["name"]
        if name == "Bigger Fireball":
            player.fireball_size += 5
        elif name == "Faster Fireball":
            player.fireball_speed += 2
        elif name == "Extra Fireball":
            player.fireball_count += 1
        elif name == "Shorter Cooldown":
            player.shoot_cooldown = max(1, int(player.shoot_cooldown * 0.8))
        elif name == "More Damage":
            player.fireball_damage += 1

    def check_player_coin_collisions(self):
        coins_collected = []
        for coin in self.coins:
            if coin.rect.colliderect(self.player.rect):
                coins_collected.append(coin)
                self.player.add_xp(1)

        for c in coins_collected:
            if c in self.coins:
                self.coins.remove(c)
                self.session_coins += 1

    def check_fireball_enemy_collisions(self):
        for fireball in self.player.fireballs:
            for enemy in self.enemies:
                if fireball.rect.colliderect(enemy.rect):
                    if fireball in self.player.fireballs:
                        self.player.fireballs.remove(fireball)

                    enemy.take_damage(fireball.damage)

                    # spawn floating damage number at the hit location
                    dmg_text = DamageText(enemy.x, enemy.rect.top,
                                          fireball.damage, self.font_small)
                    self.damage_texts.append(dmg_text)

                    # only remove and drop coin once health hits zero
                    if enemy.health <= 0:
                        new_coin = Coin(enemy.x, enemy.y)
                        self.coins.append(new_coin)
                        self.enemies.remove(enemy)
                        self.session_kills += 1

                    break

            # also check whether this fireball hit the boss
            if self.boss and fireball in self.player.fireballs:
                if fireball.rect.colliderect(self.boss.rect):
                    self.player.fireballs.remove(fireball)
                    self.boss.take_damage(fireball.damage)

                    dmg_text = DamageText(self.boss.x, self.boss.rect.top,
                                          fireball.damage, self.font_small)
                    self.damage_texts.append(dmg_text)

    def check_player_enemy_collisions(self):
        collided = False
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                collided = True
                break

        if collided:
            self.player.take_damage(1)
            px, py = self.player.x, self.player.y
            for enemy in self.enemies:
                enemy.set_knockback(px, py, PUSHBACK_DISTANCE)

    def find_nearest_enemy(self):
        if not self.enemies:
            return None
        
        nearest = None
        min_dist = float('inf')
        px, py = self.player.x, self.player.y
        for enemy in self.enemies:
            dist = math.sqrt((enemy.x - px) ** 2 + (enemy.y - py) ** 2)
            if dist < min_dist:
                min_dist = dist
                nearest = enemy
        return nearest

    def draw_game_over_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        game_over_surf = self.font_large.render("GAME OVER!", True, (255, 0, 0))
        game_over_rect = game_over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.screen.blit(game_over_surf, game_over_rect)

        prompt_surf = self.font_small.render("Press R to Play Again or ESC to Quit", True, (255, 255, 255))
        prompt_rect = prompt_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        self.screen.blit(prompt_surf, prompt_rect)

    def reset_game(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2, self.assets)
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemies_per_spawn = 1
        self.coins = []
        self.game_over = False

        # rebuild background with the selected world's tile set
        world_tiles = self.assets["world_tiles"][self.selected_world_index]
        self.background = self.create_random_background(WIDTH, HEIGHT, world_tiles)

        # reset per-session counters
        self.session_kills = 0
        self.session_coins = 0

        self.damage_texts = []

        # reset wave system
        self.wave_number         = 1
        self.wave_state          = "spawning"
        self.boss                = None
        self.wave_announce_timer = 0
        self.wave_announce_text  = ""

    def create_random_background(self, width, height, floor_tiles):
        background = pygame.Surface((width, height))

        tile_w = floor_tiles[0].get_width()
        tile_h = floor_tiles[0].get_height()

        # fill the surface with randomly chosen tiles
        for y in range(0, height, tile_h):
            for x in range(0, width, tile_w):
                tile = random.choice(floor_tiles)
                background.blit(tile, (x, y))
        return background

    def finalise_session_stats(self):
        # called at the end of a run to flush everything into the persistent stats file
        self.stats["games_played"]  += 1
        self.stats["total_kills"]   += self.session_kills
        self.stats["total_coins"]   += self.session_coins
        self.stats["total_xp"]      += self.player.xp
        self.stats["highest_level"]  = max(self.stats["highest_level"],
                                           self.player.level)
        save_stats(self.stats)
    
    def run(self):
        while self.running:
            self.clock.tick(FPS)

            self.handle_events()

            # only run gameplay logic when actively playing
            if self.game_state == "playing":
                if not self.game_over and not self.in_level_up_menu:
                    self.update()
            # paused state intentionally skips update

            self.draw()

        # only reached after self.running is set to False
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # route events to the correct state handler
            elif self.game_state == "main_menu":
                self._handle_main_menu_event(event)
            elif self.game_state == "world_select":
                self._handle_world_select_event(event)
            elif self.game_state == "stats":
                self._handle_stats_event(event)
            elif self.game_state == "settings":
                self._handle_settings_event(event)
            elif self.game_state in ("game_over", "victory"):
                self._handle_end_screen_event(event)
            elif self.game_state == "paused":
                self._handle_paused_event(event)
            elif self.game_state == "playing":
                self._handle_playing_event(event)

    def _handle_main_menu_event(self, event):
        btns = self._ui_buttons
        if btns.get("play")       and btns["play"].is_clicked(event):
            self.reset_game()
            self.game_state = "playing"
        elif btns.get("worlds")   and btns["worlds"].is_clicked(event):
            self.game_state = "world_select"
        elif btns.get("stats")    and btns["stats"].is_clicked(event):
            self.game_state = "stats"
        elif btns.get("settings") and btns["settings"].is_clicked(event):
            self.game_state = "settings"
        elif btns.get("quit")     and btns["quit"].is_clicked(event):
            self.running = False

    def _handle_world_select_event(self, event):
        btns = self._ui_buttons
        # check each world button to see if it was clicked
        for i in range(len(WORLDS)):
            key = f"world_{i}"
            if btns.get(key) and btns[key].is_clicked(event):
                self.selected_world_index = i

        if btns.get("confirm") and btns["confirm"].is_clicked(event):
            self.reset_game()
            self.game_state = "playing"
        elif btns.get("back")  and btns["back"].is_clicked(event):
            self.game_state = "main_menu"

    def _handle_stats_event(self, event):
        btns = self._ui_buttons
        if btns.get("back") and btns["back"].is_clicked(event):
            self.game_state = "main_menu"

    def _handle_settings_event(self, event):
        btns = self._ui_buttons
        if btns.get("back") and btns["back"].is_clicked(event):
            save_settings(self.settings)
            self.game_state = "main_menu"
        # flip any toggle that was clicked
        for key in list(self.settings.keys()):
            btn_key = f"toggle_{key}"
            if btns.get(btn_key) and btns[btn_key].is_clicked(event):
                self.settings[key] = not self.settings[key]

    def _handle_end_screen_event(self, event):
        btns = self._ui_buttons
        if btns.get("retry") and btns["retry"].is_clicked(event):
            self.reset_game()
            self.game_state = "playing"
        elif btns.get("menu") and btns["menu"].is_clicked(event):
            self.game_state = "main_menu"
        elif btns.get("quit") and btns["quit"].is_clicked(event):
            self.running = False

    def _handle_paused_event(self, event):
        btns = self._ui_buttons
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_state = "playing"
        elif btns.get("resume") and btns["resume"].is_clicked(event):
            self.game_state = "playing"
        elif btns.get("menu") and btns["menu"].is_clicked(event):
            self.reset_game()
            self.game_state = "main_menu"
        elif btns.get("quit") and btns["quit"].is_clicked(event):
            self.running = False

    def _handle_playing_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.game_over:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
            else:
                if not self.in_level_up_menu:
                    if event.key == pygame.K_SPACE:
                        nearest_enemy = self.find_nearest_enemy()
                        if nearest_enemy:
                            self.player.shoot_toward_enemy(nearest_enemy)
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "paused"
                else:
                    # 1/2/3 to pick an upgrade
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        index = event.key - pygame.K_1
                        if 0 <= index < len(self.upgrade_options):
                            chosen_upgrade = self.upgrade_options[index]
                            self.apply_upgrade(self.player, chosen_upgrade)
                            self.in_level_up_menu  = False
                            self._upgrade_buttons  = []
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.in_level_up_menu:
                    # check if the click landed on any upgrade button
                    for i, btn in enumerate(self._upgrade_buttons):
                        if btn.is_clicked(event):
                            self.apply_upgrade(self.player, self.upgrade_options[i])
                            self.in_level_up_menu  = False
                            self._upgrade_buttons  = []
                            break
                else:
                    # left click to shoot toward the mouse
                    self.player.shoot_toward_mouse(event.pos)

    def start_new_wave(self):
        # decide whether to run a boss wave or a normal wave
        if self.wave_number % BOSS_WAVE_INTERVAL == 0:
            self.wave_announce_text  = f"BOSS WAVE {self.wave_number}"
            self.wave_state          = "boss_active"
            self.spawn_boss()
        else:
            self.wave_announce_text  = f"WAVE {self.wave_number}"
            self.wave_state          = "active"
            self.spawn_normal_wave()

        self.wave_announce_timer = WAVE_ANNOUNCE_DURATION

    def spawn_normal_wave(self):
        pool        = WORLD_ENEMY_POOLS[self.selected_world_index]
        count       = self.wave_number + 1   # starts at 2 on wave 1, grows by 1 each wave
        extra_speed = (self.wave_number - 1) * WAVE_SPEED_SCALE

        for _ in range(count):
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                x = random.randint(0, WIDTH);  y = SPAWN_MARGIN
            elif side == "bottom":
                x = random.randint(0, WIDTH);  y = HEIGHT + SPAWN_MARGIN
            elif side == "left":
                x = -SPAWN_MARGIN;             y = random.randint(0, HEIGHT)
            else:
                x = WIDTH + SPAWN_MARGIN;      y = random.randint(0, HEIGHT)

            dist_to_player = math.sqrt((x - self.player.x)**2 + (y - self.player.y)**2)
            if dist_to_player < MIN_SPAWN_DISTANCE_FROM_PLAYER:
                continue

            enemy_type = random.choice(pool)
            enemy      = Enemy(x, y, enemy_type, self.assets["enemies"],
                               speed=DEFAULT_ENEMY_SPEED + extra_speed)

            # scale health with the wave number
            enemy.max_health += (self.wave_number - 1) * WAVE_HEALTH_SCALE
            enemy.health      = enemy.max_health

            self.enemies.append(enemy)

    def spawn_boss(self):
        boss_image = self.assets["boss"][0]
        self.boss  = Boss(
            WIDTH // 2, SPAWN_MARGIN + 60,
            self.wave_number,
            boss_image,
            self.assets["enemies"],
            self.assets["fireball"][0]
        )

    def update_wave(self):
        # kick off wave 1 immediately on game start
        if self.wave_state == "spawning":
            self.start_new_wave()
            return

        if self.wave_state == "active":
            # normal wave clears when all enemies are dead
            if len(self.enemies) == 0:
                self.wave_number += 1
                self.wave_state   = "spawning"

        elif self.wave_state == "boss_active":
            if self.boss:
                self.boss.update(self.player, self.enemies,
                                 self.selected_world_index)

                # check if any boss projectiles hit the player
                for proj in self.boss.projectiles:
                    if proj.rect.colliderect(self.player.rect):
                        self.player.take_damage(proj.damage)
                        self.boss.projectiles.remove(proj)
                        break

                # boss died - scatter coins, award XP, move to next wave
                if self.boss.health <= 0:
                    for _ in range(5):
                        cx = self.boss.x + random.randint(-30, 30)
                        cy = self.boss.y + random.randint(-30, 30)
                        self.coins.append(Coin(cx, cy))
                    self.session_kills += 1
                    self.boss          = None
                    self.wave_number  += 1
                    self.wave_state    = "spawning"

        # count down the announcement banner
        if self.wave_announce_timer > 0:
            self.wave_announce_timer -= 1

    def update(self):
        self.player.handle_input()
        self.player.update()

        # fireball collisions (fireballs already moved inside player.update)
        self.check_fireball_enemy_collisions()

        self.check_player_coin_collisions()

        for enemy in self.enemies:
            # move toward player and animate
            enemy.update(self.player)

        self.check_player_enemy_collisions()

        if self.player.health <= 0:
            self.game_over = True
            self.finalise_session_stats()
            self.game_state = "game_over"
            return

        # tick and cull expired damage texts
        for dmg_text in self.damage_texts:
            dmg_text.update()
        self.damage_texts = [d for d in self.damage_texts if not d.expired]

        self.update_wave()

        # NOTE: spawn_enemies() is intentionally not called here.
        # The wave system controls all enemy spawning via spawn_normal_wave()
        # and spawn_boss(). Calling it alongside would mean enemies trickle in
        # forever and waves would never clear.
        self.check_for_level_up()

    def draw_upgrade_menu(self):
        # dark overlay behind the upgrade panel
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        title_surf = self.font_large.render("LEVEL UP!", True, (255, 255, 0))
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 90))
        self.screen.blit(title_surf, title_rect)

        sub_surf = self.font_small.render("Choose an upgrade", True, (200, 200, 200))
        sub_rect = sub_surf.get_rect(center=(WIDTH // 2, 135))
        self.screen.blit(sub_surf, sub_rect)

        # three cards sit side by side horizontally, centred on screen
        # card_w and card_h are big so there's room for name + description
        # gap is the space between cards
        # total row width = 3 * card_w + 2 * gap
        # row_x is where the first card starts so the whole row is centred
        card_w  = 190
        card_h  = 280
        gap     = 20
        card_y  = 175
        row_w   = 3 * card_w + 2 * gap
        row_x   = WIDTH // 2 - row_w // 2

        self._upgrade_buttons = []
        for i, upgrade in enumerate(self.upgrade_options):
            # each card starts gap + card_w further right than the previous one
            card_x = row_x + i * (card_w + gap)

            btn = Button(card_x, card_y, card_w, card_h,
                         "",   # no label - we draw the text manually below
                         self.font_small,
                         color=(40, 50, 90), hover_color=(65, 80, 140),
                         border_color=(120, 140, 230), border_width=3)
            btn.draw(self.screen)
            self._upgrade_buttons.append(btn)

            # number badge at the top of each card
            num_surf = self.font_large.render(str(i + 1), True, (255, 220, 60))
            num_rect = num_surf.get_rect(center=(card_x + card_w // 2, card_y + 40))
            self.screen.blit(num_surf, num_rect)

            # upgrade name, word-wrapped manually across two lines if needed
            # we just centre it below the number badge
            name_surf = self.font_small.render(upgrade["name"], True, (255, 255, 255))
            name_rect = name_surf.get_rect(center=(card_x + card_w // 2, card_y + 100))
            self.screen.blit(name_surf, name_rect)

            # thin divider line between name and description
            line_y = card_y + 125
            pygame.draw.line(self.screen, (80, 100, 180),
                             (card_x + 15, line_y), (card_x + card_w - 15, line_y), 1)

            # description - split on space so it wraps across two short lines
            # this avoids text spilling outside the card on narrow widths
            words     = upgrade["desc"].split(" ")
            mid       = len(words) // 2
            line1     = " ".join(words[:mid])
            line2     = " ".join(words[mid:])
            for j, line in enumerate([line1, line2]):
                d_surf = self.font_small.render(line, True, (160, 190, 255))
                d_rect = d_surf.get_rect(center=(card_x + card_w // 2, card_y + 160 + j * 30))
                self.screen.blit(d_surf, d_rect)

        hint_surf = self.font_small.render("click a card  or  press 1 / 2 / 3", True, (100, 100, 100))
        hint_rect = hint_surf.get_rect(center=(WIDTH // 2, card_y + card_h + 22))
        self.screen.blit(hint_surf, hint_rect)

    def draw(self):
        # route to the correct screen based on game state
        if self.game_state == "main_menu":
            self._ui_buttons = draw_main_menu(self.screen, self.font_small, self.font_large)
            pygame.display.flip()
            return

        if self.game_state == "world_select":
            self._ui_buttons = draw_world_select(self.screen, self.font_small,
                                                  self.font_large,
                                                  self.selected_world_index)
            pygame.display.flip()
            return

        if self.game_state == "stats":
            self._ui_buttons = draw_stats_screen(self.screen, self.font_small,
                                                  self.font_large, self.stats)
            pygame.display.flip()
            return

        if self.game_state == "settings":
            self._ui_buttons = draw_settings_screen(self.screen, self.font_small,
                                                      self.font_large, self.settings)
            pygame.display.flip()
            return

        if self.game_state == "game_over":
            # draw the gameplay frame underneath then overlay the end screen
            self.screen.blit(self.background, (0, 0))
            self._ui_buttons = draw_game_over(self.screen, self.font_small,
                                               self.font_large, self.player.level,
                                               self.player.xp, self.session_kills)
            if self.settings.get("show_fps"):
                self._draw_fps()
            pygame.display.flip()
            return

        if self.game_state == "victory":
            self.screen.blit(self.background, (0, 0))
            self._ui_buttons = draw_victory(self.screen, self.font_small,
                                             self.font_large, self.player.level,
                                             self.player.xp, self.session_kills)
            if self.settings.get("show_fps"):
                self._draw_fps()
            pygame.display.flip()
            return

        # draw the live gameplay frame first, then layer the pause menu on top
        if self.game_state == "paused":
            self._draw_gameplay_frame()
            self._ui_buttons = draw_pause_menu(self.screen, self.font_small,
                                               self.font_large)
            if self.settings.get("show_fps"):
                self._draw_fps()
            pygame.display.flip()
            return

        # playing state
        self._draw_gameplay_frame()

        if self.in_level_up_menu:
            self.draw_upgrade_menu()

        if self.game_over:
            self.draw_game_over_screen()

        if self.settings.get("show_fps"):
            self._draw_fps()

        pygame.display.flip()

    def _draw_gameplay_frame(self):
        # draws background, coins, player, enemies, damage texts and HUD
        self.screen.blit(self.background, (0, 0))

        for coin in self.coins:
            coin.draw(self.screen)

        if not self.game_over:
            self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for dmg_text in self.damage_texts:
            dmg_text.draw(self.screen)

        hp = max(0, min(self.player.health, 5))
        health_img = self.assets["health"][hp]
        self.screen.blit(health_img, (10, 10))

        xp_text_surf = self.font_small.render(f"XP: {self.player.xp}", True, (255, 255, 255))
        self.screen.blit(xp_text_surf, (10, 70))

        next_level_xp = self.player.level * self.player.level * 5
        xp_to_next = max(0, next_level_xp - self.player.xp)
        xp_next_surf = self.font_small.render(f"Next Lvl XP: {xp_to_next}", True, (255, 255, 255))
        self.screen.blit(xp_next_surf, (10, 100))

        if self.boss:
            self.boss.draw(self.screen)

        wave_surf = self.font_small.render(f"WAVE: {self.wave_number}", True, (255, 255, 255))
        self.screen.blit(wave_surf, (10, 130))

        # wave announcement banner - fades out over WAVE_ANNOUNCE_DURATION frames
        if self.wave_announce_timer > 0:
            alpha    = int(255 * (self.wave_announce_timer / WAVE_ANNOUNCE_DURATION))
            is_boss  = "BOSS" in self.wave_announce_text
            colour   = (255, 60, 60) if is_boss else (255, 220, 50)

            ann_surf = self.font_large.render(self.wave_announce_text, True, colour)
            ann_surf.set_alpha(alpha)
            ann_rect = ann_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            self.screen.blit(ann_surf, ann_rect)

    def _draw_fps(self):
        fps_surf = self.font_small.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 0))
        self.screen.blit(fps_surf, (WIDTH - 120, 10))