import pygame
from constants import *
import os


# loads a sequence of numbered frames from the assets folder, e.g. orc_0.png, orc_1.png...
# scale_factor just multiplies the original image dimensions
def load_frames(prefix, frame_count, scale_factor=1, folder="assets"):
    frames = []
    for frame_number in range(frame_count):
        image_path = os.path.join(folder, f"{prefix}_{frame_number}.png")
        image = pygame.image.load(image_path).convert_alpha()

        if scale_factor != 1:
            scaled_width  = image.get_width()  * scale_factor
            scaled_height = image.get_height() * scale_factor
            image = pygame.transform.scale(image, (scaled_width, scaled_height))

        frames.append(image)
    return frames


def load_floor_tiles(folder="assets"):
    floor_tiles = []
    for tile_number in range(8):
        tile_path = os.path.join(folder, f"floor_{tile_number}.png")
        tile = pygame.image.load(tile_path).convert()

        if FLOOR_TILE_SCALE_FACTOR != 1:
            scaled_width  = tile.get_width()  * FLOOR_TILE_SCALE_FACTOR
            scaled_height = tile.get_height() * FLOOR_TILE_SCALE_FACTOR
            tile = pygame.transform.scale(tile, (scaled_width, scaled_height))

        floor_tiles.append(tile)
    return floor_tiles


# loads 8 tiles for a specific world theme, filenames follow floor_0_crypt.png etc.
def load_world_tiles(theme, folder="assets"):
    tiles = []
    for tile_number in range(8):
        tile_path = os.path.join(folder, f"floor_{tile_number}_{theme}.png")
        tile = pygame.image.load(tile_path).convert()

        if FLOOR_TILE_SCALE_FACTOR != 1:
            scaled_width  = tile.get_width()  * FLOOR_TILE_SCALE_FACTOR
            scaled_height = tile.get_height() * FLOOR_TILE_SCALE_FACTOR
            tile = pygame.transform.scale(tile, (scaled_width, scaled_height))

        tiles.append(tile)
    return tiles


def load_assets():
    assets = {}

    # enemies - original three plus the newer ones added later
    assets["enemies"] = {
        "orc":               load_frames("orc",               4, scale_factor=ENEMY_SCALE_FACTOR),
        "undead":            load_frames("undead",            4, scale_factor=ENEMY_SCALE_FACTOR),
        "demon":             load_frames("demon",             4, scale_factor=ENEMY_SCALE_FACTOR),
        "crying_whisp":      load_frames("crying_whisp",      4, scale_factor=ENEMY_SCALE_FACTOR),
        "mini_orc":          load_frames("mini_orc",          4, scale_factor=ENEMY_SCALE_FACTOR),
        "big_orc":           load_frames("big_orc",           4, scale_factor=ENEMY_SCALE_FACTOR),
        "radioactive_slime": load_frames("radioactive_slime", 4, scale_factor=ENEMY_SCALE_FACTOR),
        "mini_demon":        load_frames("mini_demon",        4, scale_factor=ENEMY_SCALE_FACTOR),
        "mud_slime":         load_frames("mud_slime",         4, scale_factor=ENEMY_SCALE_FACTOR),
        "pumpkin_man":       load_frames("pumkin_man",        4, scale_factor=ENEMY_SCALE_FACTOR),
        "hooded_skeleton":   load_frames("hooded_skeleton",   4, scale_factor=ENEMY_SCALE_FACTOR),
    }

    # player
    assets["player"] = {
        "idle": load_frames("player_idle", 4, scale_factor=PLAYER_SCALE_FACTOR),
        "run":  load_frames("player_run",  4, scale_factor=PLAYER_SCALE_FACTOR),
    }

    # fireball
    assets["fireball"] = load_frames("fireball", 1, scale_factor=FIREBALL_SCALE_FACTOR)

    # generic floor tiles kept as a fallback in case no world is selected
    assets["floor_tiles"] = load_floor_tiles()

    # world-specific tile sets, index matches WORLDS in ui_screens.py
    # 0=crypt, 1=inferno, 2=wastelands, 3=glacier
    assets["world_tiles"] = [
        load_world_tiles("crypt"),
        load_world_tiles("inferno"),
        load_world_tiles("wastelands"),
        load_world_tiles("glacier"),
    ]

    # health bar sprites
    assets["health"] = load_frames("health", 6, scale_factor=HEALTH_SCALE_FACTOR)

    # boss is just a single frame sprite
    assets["boss"] = load_frames("final_boss", 1, scale_factor=BOSS_SCALE_FACTOR)

    return assets