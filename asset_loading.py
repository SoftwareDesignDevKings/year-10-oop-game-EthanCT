import pygame
from constants import *
import os




# --------------------------------------------------------------------------
#                       ASSET LOADING - DO NOT TOUCH
# --------------------------------------------------------------------------

def load_frames(prefix, frame_count, scale_factor=1, folder="assets"):
    frames = []
    for i in range(frame_count):
        image_path = os.path.join(folder, f"{prefix}_{i}.png")
        img = pygame.image.load(image_path).convert_alpha()
        
        if scale_factor != 1:
            w = img.get_width() * scale_factor
            h = img.get_height() * scale_factor
            img = pygame.transform.scale(img, (w, h))
        
        frames.append(img)
    return frames

def load_floor_tiles(folder="assets"):
    floor_tiles = []
    for i in range(8):
        path = os.path.join(folder, f"floor_{i}.png")
        tile = pygame.image.load(path).convert()
        
        if FLOOR_TILE_SCALE_FACTOR != 1:
            tw = tile.get_width() * FLOOR_TILE_SCALE_FACTOR
            th = tile.get_height() * FLOOR_TILE_SCALE_FACTOR
            tile = pygame.transform.scale(tile, (tw, th))
        
        floor_tiles.append(tile)
    return floor_tiles

# --------------------------------------------------------------------------
#                    WORLD TILE LOADERS - NEW
# --------------------------------------------------------------------------
# Each function loads 8 tiles for its specific world theme.
# Tile filenames follow the pattern: floor_0_<theme>.png ... floor_7_<theme>.png

def load_world_tiles(theme, folder="assets"):
    tiles = []
    for i in range(8):
        path = os.path.join(folder, f"floor_{i}_{theme}.png")
        tile = pygame.image.load(path).convert()

        if FLOOR_TILE_SCALE_FACTOR != 1:
            tw = tile.get_width() * FLOOR_TILE_SCALE_FACTOR
            th = tile.get_height() * FLOOR_TILE_SCALE_FACTOR
            tile = pygame.transform.scale(tile, (tw, th))

        tiles.append(tile)
    return tiles

# --------------------------------------------------------------------------

def load_assets():
    assets = {}

    # Enemies
    assets["enemies"] = {
        "orc":               load_frames("orc",               4, scale_factor=ENEMY_SCALE_FACTOR),
        "undead":            load_frames("undead",            4, scale_factor=ENEMY_SCALE_FACTOR),
        "demon":             load_frames("demon",             4, scale_factor=ENEMY_SCALE_FACTOR),
        # ------------------------------------------------------------------
        #                     NEW ENEMIES - NEW
        # ------------------------------------------------------------------
        "crying_whisp":      load_frames("crying_whisp",      4, scale_factor=ENEMY_SCALE_FACTOR),
        "mini_orc":          load_frames("mini_orc",          4, scale_factor=ENEMY_SCALE_FACTOR),
        "big_orc":           load_frames("big_orc",           4, scale_factor=ENEMY_SCALE_FACTOR),
        "radioactive_slime": load_frames("radioactive_slime", 4, scale_factor=ENEMY_SCALE_FACTOR),
        "mini_demon":        load_frames("mini_demon",        4, scale_factor=ENEMY_SCALE_FACTOR),
        "mud_slime":         load_frames("mud_slime",         4, scale_factor=ENEMY_SCALE_FACTOR),
        "pumpkin_man":       load_frames("pumkin_man",        4, scale_factor=ENEMY_SCALE_FACTOR),
        "hooded_skeleton":   load_frames("hooded_skeleton",   4, scale_factor=ENEMY_SCALE_FACTOR),
        # ------------------------------------------------------------------
    }

    # Player
    assets["player"] = {
        "idle": load_frames("player_idle", 4, scale_factor=PLAYER_SCALE_FACTOR),
        "run":  load_frames("player_run",  4, scale_factor=PLAYER_SCALE_FACTOR),
    }

    # Fireball
    assets["fireball"] = load_frames("fireball", 1, scale_factor=FIREBALL_SCALE_FACTOR)

    # Floor (original generic tiles kept for fallback)
    assets["floor_tiles"] = load_floor_tiles()

    # ------------------------------------------------------------------
    #                  WORLD-SPECIFIC TILE SETS - NEW
    # ------------------------------------------------------------------
    # Ordered to match WORLDS list index in ui_screens.py:
    #   index 0 = The Crypt    -> crypt tiles
    #   index 1 = The Inferno  -> inferno tiles
    #   index 2 = The Wastes   -> wastelands tiles
    #   index 3 = The Glacier  -> glacier tiles
    assets["world_tiles"] = [
        load_world_tiles("crypt"),
        load_world_tiles("inferno"),
        load_world_tiles("wastelands"),
        load_world_tiles("glacier"),
    ]
    # ------------------------------------------------------------------

    # Health images
    assets["health"] = load_frames("health", 6, scale_factor=HEALTH_SCALE_FACTOR)

    # ------------------------------------------------------------------
    #                    BOSS SPRITE - NEW
    # ------------------------------------------------------------------
    # Single frame sprite loaded the same way as all other assets
    assets["boss"] = load_frames("final_boss", 1, scale_factor=BOSS_SCALE_FACTOR)
    # ------------------------------------------------------------------

    return assets