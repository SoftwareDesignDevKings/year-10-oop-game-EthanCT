WIDTH = 800
HEIGHT = 600
FPS = 60

# movement speeds
PLAYER_SPEED = 3
DEFAULT_ENEMY_SPEED = 1

SPAWN_MARGIN = 50
MIN_SPAWN_DISTANCE_FROM_PLAYER = 200

ENEMY_SCALE_FACTOR = 2
PLAYER_SCALE_FACTOR = 2
FLOOR_TILE_SCALE_FACTOR = 2
HEALTH_SCALE_FACTOR = 3

PUSHBACK_DISTANCE = 80
ENEMY_KNOCKBACK_SPEED = 5

FIREBALL_SCALE_FACTOR = 1.5

# fireball base damage and starting cooldown in frames
FIREBALL_BASE_DAMAGE    = 1
FIREBALL_SHOOT_COOLDOWN = 40

# health values per enemy type
ENEMY_HEALTH = {
    "orc"              : 3,
    "undead"           : 2,
    "demon"            : 5,
    "crying_whisp"     : 2,
    "mini_orc"         : 2,
    "big_orc"          : 6,
    "radioactive_slime": 3,
    "mini_demon"       : 3,
    "mud_slime"        : 2,
    "pumpkin_man"      : 4,
    "hooded_skeleton"  : 3,
}

# controls which enemy types can spawn in each world
# index matches the WORLDS list in ui_screens.py: 0=Crypt, 1=Inferno, 2=Wastes, 3=Glacier
WORLD_ENEMY_POOLS = [
    # The Crypt: undead, skeletal and ghostly enemies
    ["undead", "hooded_skeleton", "crying_whisp", "pumpkin_man"],

    # The Inferno: demons and fire creatures
    ["demon", "mini_demon", "radioactive_slime"],

    # The Wastes: orcs and swamp creatures
    ["orc", "mini_orc", "big_orc", "mud_slime"],

    # The Glacier: slower, tougher frozen enemies
    ["hooded_skeleton", "big_orc", "crying_whisp", "mud_slime"],
]

# health bar drawn above each enemy sprite
HEALTH_BAR_WIDTH  = 40
HEALTH_BAR_HEIGHT = 5
HEALTH_BAR_OFFSET = 10   # pixels above the enemy rect

# damage text floats upward for this many frames before disappearing
DAMAGE_TEXT_LIFETIME = 45
DAMAGE_TEXT_RISE     = 1

# how many positions to keep for the fireball trail
FIREBALL_TRAIL_LENGTH = 8

# how many normal waves between boss waves
BOSS_WAVE_INTERVAL     = 5

# enemy stat scaling applied each wave on top of base values
WAVE_HEALTH_SCALE      = 1     # extra max health per wave
WAVE_SPEED_SCALE       = 0.1   # extra speed per wave

# how long the wave announcement stays on screen in frames
WAVE_ANNOUNCE_DURATION = 180

BOSS_BASE_HEALTH       = 30    # health on wave 5, the first boss wave
BOSS_HEALTH_PER_WAVE   = 20    # additional health each subsequent boss wave
BOSS_BASE_SPEED        = 0.8   # boss walks slower than regular enemies
BOSS_SCALE_FACTOR      = 3     # sprite scale multiplier

# boss health bar
BOSS_BAR_WIDTH         = 120
BOSS_BAR_HEIGHT        = 8
BOSS_BAR_OFFSET        = 14    # pixels above the boss rect

# radial burst - fires projectiles in all directions
BOSS_BURST_COUNT       = 8     # projectiles per burst
BOSS_BURST_INTERVAL    = 180   # frames between bursts (~3 seconds)
BOSS_PROJECTILE_SPEED  = 4
BOSS_PROJECTILE_SIZE   = 20
BOSS_PROJECTILE_DAMAGE = 1

# charge attack
BOSS_CHARGE_INTERVAL   = 240   # frames between charges (~4 seconds)
BOSS_CHARGE_DURATION   = 30    # how many frames the charge lasts
BOSS_CHARGE_SPEED      = 6     # pixels per frame while charging

# minion spawn
BOSS_MINION_INTERVAL   = 300   # frames between spawns (~5 seconds)
BOSS_MINION_COUNT      = 3     # enemies dropped per spawn