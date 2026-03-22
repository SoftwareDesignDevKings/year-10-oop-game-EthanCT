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
from fireball import FlameParticle


class Game:
    def __init__(self):

        pygame.init()
        pygame.mixer.init()

        # window setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shooter")

        self.clock  = pygame.time.Clock()
        self.assets = load_assets()

        # fonts
        font_path        = os.path.join("assets", "PressStart2P.ttf")
        self.font_small  = pygame.font.Font(font_path, 18)
        self.font_large  = pygame.font.Font(font_path, 32)

        # track which music file is currently loaded so we don't restart it unnecessarily
        self.current_music = None

        # background gets rebuilt in reset_game() with world-specific tiles
        self.background = self.create_random_background(WIDTH, HEIGHT, self.assets["floor_tiles"])

        self.running   = True
        self.game_over = False

        self.enemies = []

        self.enemy_spawn_timer    = 0
        self.enemy_spawn_interval = 60
        self.enemies_per_spawn    = 1

        self.coins = []

        self.in_level_up_menu = False
        self.upgrade_options  = []

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
        self.ui_buttons      = {}
        # upgrade card buttons - rebuilt each frame the upgrade menu is open
        self.upgrade_buttons = []

        # wave system
        self.wave_number         = 1
        self.wave_state          = "spawning"   # "spawning", "active", "cleared", "boss_active"
        self.boss                = None         # None when no boss is alive
        self.wave_announce_timer = 0
        self.wave_announce_text  = ""

        self.reset_game()

    def spawn_enemies(self):
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_interval:
            self.enemy_spawn_timer = 0

            for _ in range(self.enemies_per_spawn):
                spawn_side = random.choice(["top", "bottom", "left", "right"])
                if spawn_side == "top":
                    spawn_x = random.randint(0, WIDTH)
                    spawn_y = SPAWN_MARGIN
                elif spawn_side == "bottom":
                    spawn_x = random.randint(0, WIDTH)
                    spawn_y = HEIGHT + SPAWN_MARGIN
                elif spawn_side == "left":
                    spawn_x = -SPAWN_MARGIN
                    spawn_y = random.randint(0, HEIGHT)
                else:
                    spawn_x = WIDTH + SPAWN_MARGIN
                    spawn_y = random.randint(0, HEIGHT)

                # skip the spawn if it would be too close to the player
                distance_to_player = math.sqrt((spawn_x - self.player.x) ** 2 + (spawn_y - self.player.y) ** 2)
                if distance_to_player < MIN_SPAWN_DISTANCE_FROM_PLAYER:
                    continue

                # pick a random enemy type from this world's pool
                enemy_pool = WORLD_ENEMY_POOLS[self.selected_world_index]
                enemy_type = random.choice(enemy_pool)
                enemy      = Enemy(spawn_x, spawn_y, enemy_type, self.assets["enemies"])
                self.enemies.append(enemy)

    def check_for_level_up(self):
        xp_needed_for_next_level = self.player.level * self.player.level * 5
        if self.player.xp >= xp_needed_for_next_level:
            self.player.level    += 1
            self.in_level_up_menu = True
            self.upgrade_options  = self.pick_random_upgrades(3)

            # ramp up spawns every time the player levels up
            self.enemies_per_spawn += 1

    def pick_random_upgrades(self, number_of_options):
        possible_upgrades = [
            {"name": "Bigger Fireball",          "desc": "Fireball size +5"},
            {"name": "Faster Fireball",          "desc": "Fireball speed +2"},
            {"name": "Extra Fireball",           "desc": "Fire additional fireball"},
            {"name": "Shorter Cooldown",         "desc": "Shoot more frequently"},
            {"name": "More Damage",              "desc": "Fireball damage +1"},
            {"name": "Unyielding Determination", "desc": "Fireballs pierce through enemies"},
        ]
        return random.sample(possible_upgrades, k=number_of_options)

    def apply_upgrade(self, player, upgrade):
        upgrade_name = upgrade["name"]
        if upgrade_name == "Bigger Fireball":
            player.fireball_size += 5
        elif upgrade_name == "Faster Fireball":
            player.fireball_speed += 2
        elif upgrade_name == "Extra Fireball":
            player.fireball_count += 1
        elif upgrade_name == "Shorter Cooldown":
            player.shoot_cooldown = max(1, int(player.shoot_cooldown * 0.8))
        elif upgrade_name == "More Damage":
            player.fireball_damage += 1
        elif upgrade_name == "Unyielding Determination":
            # each time this is picked the fireball punches through one more enemy
            player.fireball_pierce_count += 1

    def check_player_coin_collisions(self):
        coins_collected = []
        for coin in self.coins:
            # slide the coin toward the player if they're close enough
            coin.update(self.player.x, self.player.y)

            if coin.rect.colliderect(self.player.rect):
                coins_collected.append(coin)
                self.player.add_xp(5)

        for collected_coin in coins_collected:
            if collected_coin in self.coins:
                self.coins.remove(collected_coin)
                self.session_coins += 1

    def check_fireball_enemy_collisions(self):
        for fireball in self.player.fireballs[:]:
            for enemy in self.enemies[:]:

                # skip enemies this fireball has already passed through
                if id(enemy) in fireball.hit_enemies:
                    continue

                if fireball.rect.colliderect(enemy.rect):

                    # record the hit so we don't damage this enemy again on the next frame
                    fireball.hit_enemies.add(id(enemy))

                    enemy.take_damage(fireball.damage)

                    # spawn floating damage number at the hit location
                    damage_popup = DamageText(enemy.x, enemy.rect.top, fireball.damage, self.font_small)
                    self.damage_texts.append(damage_popup)

                    # burst of small flame particles at the impact point
                    for _ in range(FLAME_PARTICLE_COUNT):
                        self.flame_particles.append(FlameParticle(enemy.x, enemy.y))

                    # only remove and drop coin once health hits zero
                    if enemy.health <= 0:
                        self.coins.append(Coin(enemy.x, enemy.y))
                        self.enemies.remove(enemy)
                        self.session_kills += 1

                    # use up one pierce charge - remove the fireball only when they run out
                    if fireball.pierce_count > 0:
                        fireball.pierce_count -= 1
                        # lock onto the nearest valid enemy and start curving toward it
                        next_target = self.find_nearest_unhit_enemy(fireball)
                        if next_target:
                            fireball.redirect_toward(next_target)
                    else:
                        if fireball in self.player.fireballs:
                            self.player.fireballs.remove(fireball)
                        break

        # also check whether any surviving fireballs hit the boss
        for fireball in self.player.fireballs[:]:
            if self.boss and fireball.rect.colliderect(self.boss.rect):
                if id(self.boss) not in fireball.hit_enemies:
                    fireball.hit_enemies.add(id(self.boss))
                    self.boss.take_damage(fireball.damage)

                    damage_popup = DamageText(self.boss.x, self.boss.rect.top, fireball.damage, self.font_small)
                    self.damage_texts.append(damage_popup)

                    # boss always kills the fireball - it's one very large target
                    if fireball in self.player.fireballs:
                        self.player.fireballs.remove(fireball)

    def check_player_enemy_collisions(self):
        player_was_hit = False
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                player_was_hit = True
                break

        if player_was_hit:
            self.player.take_damage(1)
            player_x = self.player.x
            player_y = self.player.y
            for enemy in self.enemies:
                enemy.set_knockback(player_x, player_y, PUSHBACK_DISTANCE)

    def find_nearest_enemy(self):
        if not self.enemies:
            return None

        nearest_enemy    = None
        nearest_distance = float('inf')
        player_x         = self.player.x
        player_y         = self.player.y

        for enemy in self.enemies:
            distance = math.sqrt((enemy.x - player_x) ** 2 + (enemy.y - player_y) ** 2)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_enemy    = enemy

        return nearest_enemy

    def find_nearest_unhit_enemy(self, fireball):
        # finds the closest enemy the fireball hasn't already hit, measured from the fireball's position
        # enemies closer than PIERCE_MIN_DISTANCE are ignored - no point in a tiny hop
        nearest_enemy    = None
        nearest_distance = float('inf')

        for enemy in self.enemies:
            if id(enemy) in fireball.hit_enemies:
                continue
            distance = math.sqrt((enemy.x - fireball.x) ** 2 + (enemy.y - fireball.y) ** 2)
            if distance < PIERCE_MIN_DISTANCE:
                continue
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_enemy    = enemy

        return nearest_enemy

    def draw_game_over_screen(self):
        dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 180))
        self.screen.blit(dark_overlay, (0, 0))

        game_over_surface = self.font_large.render("GAME OVER!", True, (255, 0, 0))
        self.screen.blit(game_over_surface, game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))

        prompt_surface = self.font_small.render("Press R to Play Again or ESC to Quit", True, (255, 255, 255))
        self.screen.blit(prompt_surface, prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

    def reset_game(self):
        self.player            = Player(WIDTH // 2, HEIGHT // 2, self.assets)
        self.enemies           = []
        self.enemy_spawn_timer = 0
        self.enemies_per_spawn = 1
        self.coins             = []
        self.game_over         = False

        # rebuild background with the selected world's tile set
        world_tiles     = self.assets["world_tiles"][self.selected_world_index]
        self.background = self.create_random_background(WIDTH, HEIGHT, world_tiles)

        # reset per-session counters
        self.session_kills = 0
        self.session_coins = 0

        self.damage_texts     = []
        self.flame_particles  = []

        # reset wave system
        self.wave_number         = 1
        self.wave_state          = "spawning"
        self.boss                = None
        self.wave_announce_timer = 0
        self.wave_announce_text  = ""

    def create_random_background(self, width, height, floor_tiles):
        background_surface = pygame.Surface((width, height))

        tile_width  = floor_tiles[0].get_width()
        tile_height = floor_tiles[0].get_height()

        # fill the surface with randomly chosen tiles
        for tile_y in range(0, height, tile_height):
            for tile_x in range(0, width, tile_width):
                random_tile = random.choice(floor_tiles)
                background_surface.blit(random_tile, (tile_x, tile_y))

        return background_surface

    def finalise_session_stats(self):
        # called at the end of a run to flush everything into the persistent stats file
        self.stats["games_played"]  += 1
        self.stats["total_kills"]   += self.session_kills
        self.stats["total_coins"]   += self.session_coins
        self.stats["total_xp"]      += self.player.xp
        self.stats["highest_level"]  = max(self.stats["highest_level"], self.player.level)
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

            self.update_music()
            self.draw()

        # only reached after self.running is set to False
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # route events to the correct state handler
            elif self.game_state == "main_menu":
                self.handle_main_menu_event(event)
            elif self.game_state == "world_select":
                self.handle_world_select_event(event)
            elif self.game_state == "stats":
                self.handle_stats_event(event)
            elif self.game_state == "settings":
                self.handle_settings_event(event)
            elif self.game_state in ("game_over", "victory"):
                self.handle_end_screen_event(event)
            elif self.game_state == "paused":
                self.handle_paused_event(event)
            elif self.game_state == "playing":
                self.handle_playing_event(event)

    def handle_main_menu_event(self, event):
        buttons = self.ui_buttons
        if buttons.get("play")       and buttons["play"].is_clicked(event):
            self.reset_game()
            self.game_state = "playing"
        elif buttons.get("worlds")   and buttons["worlds"].is_clicked(event):
            self.game_state = "world_select"
        elif buttons.get("stats")    and buttons["stats"].is_clicked(event):
            self.game_state = "stats"
        elif buttons.get("settings") and buttons["settings"].is_clicked(event):
            self.game_state = "settings"
        elif buttons.get("quit")     and buttons["quit"].is_clicked(event):
            self.running = False

    def handle_world_select_event(self, event):
        buttons = self.ui_buttons
        # check each world button to see if it was clicked
        for world_index in range(len(WORLDS)):
            button_key = f"world_{world_index}"
            if buttons.get(button_key) and buttons[button_key].is_clicked(event):
                self.selected_world_index = world_index

        if buttons.get("confirm") and buttons["confirm"].is_clicked(event):
            self.reset_game()
            self.game_state = "playing"
        elif buttons.get("back") and buttons["back"].is_clicked(event):
            self.game_state = "main_menu"

    def handle_stats_event(self, event):
        buttons = self.ui_buttons
        if buttons.get("back") and buttons["back"].is_clicked(event):
            self.game_state = "main_menu"

    def handle_settings_event(self, event):
        buttons = self.ui_buttons
        if buttons.get("back") and buttons["back"].is_clicked(event):
            save_settings(self.settings)
            self.game_state = "main_menu"
        # flip any toggle that was clicked
        for settings_key in list(self.settings.keys()):
            button_key = f"toggle_{settings_key}"
            if buttons.get(button_key) and buttons[button_key].is_clicked(event):
                self.settings[settings_key] = not self.settings[settings_key]
                # clear the cached track so _update_music reloads it on the next frame
                if settings_key == "music_enabled":
                    self.current_music = None

    def handle_end_screen_event(self, event):
        buttons = self.ui_buttons
        if buttons.get("retry") and buttons["retry"].is_clicked(event):
            self.reset_game()
            self.game_state = "playing"
        elif buttons.get("menu") and buttons["menu"].is_clicked(event):
            self.game_state = "main_menu"
        elif buttons.get("quit") and buttons["quit"].is_clicked(event):
            self.running = False

    def handle_paused_event(self, event):
        buttons = self.ui_buttons
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_state = "playing"
        elif buttons.get("resume") and buttons["resume"].is_clicked(event):
            self.game_state = "playing"
        elif buttons.get("menu") and buttons["menu"].is_clicked(event):
            self.reset_game()
            self.game_state = "main_menu"
        elif buttons.get("quit") and buttons["quit"].is_clicked(event):
            self.running = False

    def handle_playing_event(self, event):
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
                        chosen_index = event.key - pygame.K_1
                        if 0 <= chosen_index < len(self.upgrade_options):
                            self.apply_upgrade(self.player, self.upgrade_options[chosen_index])
                            self.in_level_up_menu  = False
                            self.upgrade_buttons  = []

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.in_level_up_menu:
                    # check if the click landed on any upgrade button
                    for card_index, card_button in enumerate(self.upgrade_buttons):
                        if card_button.is_clicked(event):
                            self.apply_upgrade(self.player, self.upgrade_options[card_index])
                            self.in_level_up_menu  = False
                            self.upgrade_buttons  = []
                            break
                else:
                    # left click to shoot toward the mouse
                    self.player.shoot_toward_mouse(event.pos)

    def start_new_wave(self):
        # decide whether to run a boss wave or a normal wave
        if self.wave_number % BOSS_WAVE_INTERVAL == 0:
            self.wave_announce_text = f"BOSS WAVE {self.wave_number}"
            self.wave_state         = "boss_active"
            self.spawn_boss()
        else:
            self.wave_announce_text = f"WAVE {self.wave_number}"
            self.wave_state         = "active"
            self.spawn_normal_wave()

        self.wave_announce_timer = WAVE_ANNOUNCE_DURATION

    def spawn_normal_wave(self):
        enemy_pool  = WORLD_ENEMY_POOLS[self.selected_world_index]
        enemy_count = self.wave_number + 1   # starts at 2 on wave 1, grows by 1 each wave
        extra_speed = (self.wave_number - 1) * WAVE_SPEED_SCALE

        for _ in range(enemy_count):
            spawn_side = random.choice(["top", "bottom", "left", "right"])
            if spawn_side == "top":
                spawn_x = random.randint(0, WIDTH)
                spawn_y = SPAWN_MARGIN
            elif spawn_side == "bottom":
                spawn_x = random.randint(0, WIDTH)
                spawn_y = HEIGHT + SPAWN_MARGIN
            elif spawn_side == "left":
                spawn_x = -SPAWN_MARGIN
                spawn_y = random.randint(0, HEIGHT)
            else:
                spawn_x = WIDTH + SPAWN_MARGIN
                spawn_y = random.randint(0, HEIGHT)

            distance_to_player = math.sqrt((spawn_x - self.player.x)**2 + (spawn_y - self.player.y)**2)
            if distance_to_player < MIN_SPAWN_DISTANCE_FROM_PLAYER:
                continue

            enemy_type = random.choice(enemy_pool)
            enemy      = Enemy(spawn_x, spawn_y, enemy_type, self.assets["enemies"],
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
                self.boss.update(self.player, self.enemies, self.selected_world_index)

                # check if any boss projectiles hit the player
                for boss_projectile in self.boss.projectiles:
                    if boss_projectile.rect.colliderect(self.player.rect):
                        self.player.take_damage(boss_projectile.damage)
                        self.boss.projectiles.remove(boss_projectile)
                        break

                # boss died - scatter coins, award XP, move to next wave
                if self.boss.health <= 0:
                    for _ in range(5):
                        coin_x = self.boss.x + random.randint(-30, 30)
                        coin_y = self.boss.y + random.randint(-30, 30)
                        self.coins.append(Coin(coin_x, coin_y))
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
        for damage_text in self.damage_texts:
            damage_text.update()
        self.damage_texts = [text for text in self.damage_texts if not text.expired]

        # tick and cull expired flame particles
        for particle in self.flame_particles:
            particle.update()
        self.flame_particles = [p for p in self.flame_particles if not p.expired]

        self.update_wave()

        # NOTE: spawn_enemies() is intentionally not called here.
        # The wave system controls all enemy spawning via spawn_normal_wave()
        # and spawn_boss(). Calling it alongside would mean enemies trickle in
        # forever and waves would never clear.
        self.check_for_level_up()

    def draw_upgrade_menu(self):
        # dark overlay so the gameplay behind the cards is still visible but dimmed
        dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 200))
        self.screen.blit(dark_overlay, (0, 0))

        title_surface = self.font_large.render("LEVEL UP!", True, (255, 255, 0))
        self.screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 90)))

        subtitle_surface = self.font_small.render("Choose an upgrade", True, (200, 200, 200))
        self.screen.blit(subtitle_surface, subtitle_surface.get_rect(center=(WIDTH // 2, 135)))

        # --- card layout ---
        # all three cards share the same width, height, and top edge (card_top)
        # gap_between_cards is the empty space separating each card from the next
        # total_row_width is the combined width of all three cards plus the two gaps between them
        # row_left_edge is the x position where the first card starts,
        #   calculated so the whole row is centred on screen
        card_width        = 210
        card_height       = 290
        gap_between_cards = 18
        card_top          = 170
        total_row_width   = 3 * card_width + 2 * gap_between_cards
        row_left_edge     = WIDTH // 2 - total_row_width // 2

        # how many pixels of padding to keep between text and the card edges
        # used when checking whether a rendered string fits inside the card
        text_padding_sides = 12

        # the maximum pixel width a text line is allowed to be before we split it
        max_text_width = card_width - (text_padding_sides * 2)

        self.upgrade_buttons = []

        for card_index, upgrade in enumerate(self.upgrade_options):

            # x position of this card: move right by one card-width + one gap per card
            card_left     = row_left_edge + card_index * (card_width + gap_between_cards)
            card_centre_x = card_left + card_width // 2

            # draw the card background and border (empty label so Button handles styling only)
            card_button = Button(card_left, card_top, card_width, card_height, "", self.font_small,
                                 color=(40, 50, 90), hover_color=(65, 80, 140),
                                 border_color=(120, 140, 230), border_width=3)
            card_button.draw(self.screen)
            self.upgrade_buttons.append(card_button)

            # large number badge near the top of the card (1, 2, or 3)
            number_surface = self.font_large.render(str(card_index + 1), True, (255, 220, 60))
            self.screen.blit(number_surface, number_surface.get_rect(center=(card_centre_x, card_top + 38)))

            # --- upgrade name, wrapped if it won't fit on one line ---
            # font.size(text) returns (pixel_width, pixel_height) without actually rendering
            # we use this to check whether the name fits before committing to drawing it
            name_words         = upgrade["name"].split(" ")
            name_lines         = []
            current_line_words = []

            for word in name_words:
                # try adding this word to the current line and measure the result
                test_line       = " ".join(current_line_words + [word])
                test_line_width = self.font_small.size(test_line)[0]

                if test_line_width <= max_text_width:
                    # it fits, keep building this line
                    current_line_words.append(word)
                else:
                    # it doesn't fit - save the current line and start a new one with this word
                    if current_line_words:
                        name_lines.append(" ".join(current_line_words))
                    current_line_words = [word]

            # don't forget the last line still sitting in current_line_words
            if current_line_words:
                name_lines.append(" ".join(current_line_words))

            # draw each name line centred inside the card, stacked downward
            name_start_y      = card_top + 90
            line_height_small = 26   # vertical space between lines for font_small

            for line_number, name_line in enumerate(name_lines):
                name_line_surface = self.font_small.render(name_line, True, (255, 255, 255))
                self.screen.blit(name_line_surface, name_line_surface.get_rect(
                    center=(card_centre_x, name_start_y + line_number * line_height_small)))

            # thin divider line separating the name from the description
            # positioned just below wherever the last name line ended up
            divider_y = name_start_y + len(name_lines) * line_height_small + 8
            pygame.draw.line(self.screen, (80, 100, 180),
                             (card_left + 15, divider_y), (card_left + card_width - 15, divider_y), 1)

            # --- description, same pixel-aware wrapping as the name above ---
            desc_words         = upgrade["desc"].split(" ")
            desc_lines         = []
            current_line_words = []

            for word in desc_words:
                test_line       = " ".join(current_line_words + [word])
                test_line_width = self.font_small.size(test_line)[0]

                if test_line_width <= max_text_width:
                    current_line_words.append(word)
                else:
                    if current_line_words:
                        desc_lines.append(" ".join(current_line_words))
                    current_line_words = [word]

            if current_line_words:
                desc_lines.append(" ".join(current_line_words))

            # draw each description line below the divider
            desc_start_y = divider_y + 20

            for line_number, desc_line in enumerate(desc_lines):
                desc_line_surface = self.font_small.render(desc_line, True, (160, 190, 255))
                self.screen.blit(desc_line_surface, desc_line_surface.get_rect(
                    center=(card_centre_x, desc_start_y + line_number * line_height_small)))

        hint_surface = self.font_small.render("click a card  or  press 1 / 2 / 3", True, (100, 100, 100))
        self.screen.blit(hint_surface, hint_surface.get_rect(center=(WIDTH // 2, card_top + card_height + 22)))

    def draw(self):
        # route to the correct screen based on game state
        if self.game_state == "main_menu":
            self.ui_buttons = draw_main_menu(self.screen, self.font_small, self.font_large)
            pygame.display.flip()
            return

        if self.game_state == "world_select":
            self.ui_buttons = draw_world_select(self.screen, self.font_small,
                                                  self.font_large, self.selected_world_index)
            pygame.display.flip()
            return

        if self.game_state == "stats":
            self.ui_buttons = draw_stats_screen(self.screen, self.font_small,
                                                  self.font_large, self.stats)
            pygame.display.flip()
            return

        if self.game_state == "settings":
            self.ui_buttons = draw_settings_screen(self.screen, self.font_small,
                                                     self.font_large, self.settings)
            pygame.display.flip()
            return

        if self.game_state == "game_over":
            # draw the gameplay frame underneath then overlay the end screen
            self.screen.blit(self.background, (0, 0))
            self.ui_buttons = draw_game_over(self.screen, self.font_small,
                                               self.font_large, self.player.level,
                                               self.player.xp, self.session_kills)
            if self.settings.get("show_fps"):
                self.draw_fps()
            pygame.display.flip()
            return

        if self.game_state == "victory":
            self.screen.blit(self.background, (0, 0))
            self.ui_buttons = draw_victory(self.screen, self.font_small,
                                             self.font_large, self.player.level,
                                             self.player.xp, self.session_kills)
            if self.settings.get("show_fps"):
                self.draw_fps()
            pygame.display.flip()
            return

        # draw the live gameplay frame first, then layer the pause menu on top
        if self.game_state == "paused":
            self.draw_gameplay_frame()
            self.ui_buttons = draw_pause_menu(self.screen, self.font_small, self.font_large)
            if self.settings.get("show_fps"):
                self.draw_fps()
            pygame.display.flip()
            return

        # playing state
        self.draw_gameplay_frame()

        if self.in_level_up_menu:
            self.draw_upgrade_menu()

        if self.game_over:
            self.draw_game_over_screen()

        if self.settings.get("show_fps"):
            self.draw_fps()

        pygame.display.flip()

    def draw_gameplay_frame(self):
        # draws background, coins, player, enemies, damage texts and HUD
        self.screen.blit(self.background, (0, 0))

        for coin in self.coins:
            coin.draw(self.screen)

        if not self.game_over:
            self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for particle in self.flame_particles:
            particle.draw(self.screen)

        for damage_text in self.damage_texts:
            damage_text.draw(self.screen)

        clamped_health = max(0, min(self.player.health, 5))
        self.screen.blit(self.assets["health"][clamped_health], (10, 10))

        xp_surface = self.font_small.render(f"XP: {self.player.xp}", True, (255, 255, 255))
        self.screen.blit(xp_surface, (10, 70))

        xp_needed_for_next_level = self.player.level * self.player.level * 5
        xp_remaining             = max(0, xp_needed_for_next_level - self.player.xp)
        xp_remaining_surface     = self.font_small.render(f"Next Lvl XP: {xp_remaining}", True, (255, 255, 255))
        self.screen.blit(xp_remaining_surface, (10, 100))

        if self.boss:
            self.boss.draw(self.screen)

        wave_surface = self.font_small.render(f"WAVE: {self.wave_number}", True, (255, 255, 255))
        self.screen.blit(wave_surface, (10, 130))

        # wave announcement banner - fades out over WAVE_ANNOUNCE_DURATION frames
        if self.wave_announce_timer > 0:
            banner_alpha   = int(255 * (self.wave_announce_timer / WAVE_ANNOUNCE_DURATION))
            is_boss_wave   = "BOSS" in self.wave_announce_text
            banner_colour  = (255, 60, 60) if is_boss_wave else (255, 220, 50)
            banner_surface = self.font_large.render(self.wave_announce_text, True, banner_colour)
            banner_surface.set_alpha(banner_alpha)
            self.screen.blit(banner_surface, banner_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3)))

    def draw_fps(self):
        fps_surface = self.font_small.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 0))
        self.screen.blit(fps_surface, (WIDTH - 120, 10))

    def play_music(self, filepath):
        # skip if this track is already playing - avoids restarting on every frame
        if self.current_music == filepath:
            return

        self.current_music = filepath
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play(-1)   # -1 means loop forever

    def play_random_gameplay_track(self):
        # gamebg3 loops until wave 6, after that gamebg1 and gamebg2 alternate
        if self.wave_number < 6:
            track = os.path.join("assets", "gamebg3.mp3")
        else:
            tracks    = [os.path.join("assets", "gamebg1.mp3"), os.path.join("assets", "gamebg2.mp3")]
            remaining = [t for t in tracks if t != self.current_music]
            track     = random.choice(remaining)

        self.current_music = track
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(0)    # 0 means play once, then get_busy() goes false

    def update_music(self):
        # called every frame - routes to the right track based on game state

        if not self.settings.get("music_enabled"):
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            self.current_music = None
            return

        title_track = os.path.join("assets", "titlemusic.mp3")

        if self.game_state in ("main_menu", "world_select", "stats", "settings"):
            # always switch to title music when on menu screens
            if self.current_music != title_track:
                self.current_music = None   # force play_music to load it fresh
            self.play_music(title_track)

        elif self.game_state in ("playing", "paused"):
            intro_track = os.path.join("assets", "gamebg3.mp3")

            # if title was playing, switch immediately to a gameplay track
            if self.current_music == title_track:
                self.current_music = None
                self.play_random_gameplay_track()
            # cut over from gamebg3 to the main rotation once wave 6 is reached
            elif self.current_music == intro_track and self.wave_number >= 6:
                self.current_music = None
                self.play_random_gameplay_track()
            # if a gameplay track just finished, pick the next one
            elif not pygame.mixer.music.get_busy():
                self.play_random_gameplay_track()

        elif self.game_state in ("game_over", "victory"):
            # let whatever is playing finish naturally
            pass