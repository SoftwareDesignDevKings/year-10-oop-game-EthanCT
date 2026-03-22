import pygame
from constants import *
from button import Button


# each function draws a full screen and returns the buttons it contains so
# game.py can handle click events without duplicating any drawing logic

# add more entries here to extend the world selection screen
WORLDS = [
    {"name": "The Crypt",    "desc": "Dark corridors, undead hordes"},
    {"name": "The Inferno",  "desc": "Demons and fire pits await"},
    {"name": "The Wastes",   "desc": "Orcs roam endless wastelands"},
    {"name": "The Glacier",  "desc": "Frozen wastes, chilling horrors"},
]


def draw_main_menu(surface, font_small, font_large):
    surface.fill((20, 10, 30))

    title_surface = font_large.render("DUNGEON SHOOTER", True, (255, 200, 50))
    surface.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 130)))

    subtitle_surface = font_small.render("Survive the endless hordes", True, (180, 180, 180))
    surface.blit(subtitle_surface, subtitle_surface.get_rect(center=(WIDTH // 2, 185)))

    button_width  = 260
    button_height = 44
    button_left   = WIDTH // 2 - button_width // 2

    button_play     = Button(button_left, 250, button_width, button_height, "PLAY",         font_small)
    button_worlds   = Button(button_left, 310, button_width, button_height, "SELECT WORLD", font_small)
    button_stats    = Button(button_left, 370, button_width, button_height, "STATS",        font_small)
    button_settings = Button(button_left, 430, button_width, button_height, "SETTINGS",     font_small)
    button_quit     = Button(button_left, 490, button_width, button_height, "QUIT",         font_small,
                             color=(120, 40, 40), hover_color=(180, 60, 60))

    for button in [button_play, button_worlds, button_stats, button_settings, button_quit]:
        button.draw(surface)

    return {
        "play"    : button_play,
        "worlds"  : button_worlds,
        "stats"   : button_stats,
        "settings": button_settings,
        "quit"    : button_quit,
    }


def draw_world_select(surface, font_small, font_large, selected_world_index):
    surface.fill((15, 20, 35))

    title_surface = font_large.render("SELECT WORLD", True, (100, 200, 255))
    surface.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 80)))

    buttons       = {}
    button_width  = 320
    button_height = 50

    for world_index, world in enumerate(WORLDS):
        # highlight the selected world with a gold border
        border_colour = (255, 220, 50) if world_index == selected_world_index else (150, 150, 150)
        button_top    = 160 + world_index * 80
        button        = Button(WIDTH // 2 - button_width // 2, button_top, button_width, button_height,
                               world["name"], font_small,
                               color=(40, 60, 100), hover_color=(60, 90, 150),
                               border_color=border_colour, border_width=3)
        button.draw(surface)
        buttons[f"world_{world_index}"] = button

        # short description shown below each world button
        desc_surface = font_small.render(world["desc"], True, (160, 160, 160))
        surface.blit(desc_surface, desc_surface.get_rect(center=(WIDTH // 2, button_top + button_height + 10)))

    button_back = Button(30, HEIGHT - 60, 140, 40, "BACK", font_small,
                         color=(60, 60, 60), hover_color=(100, 100, 100))
    button_back.draw(surface)
    buttons["back"] = button_back

    button_confirm = Button(WIDTH - 200, HEIGHT - 60, 170, 40, "CONFIRM", font_small,
                            color=(40, 120, 40), hover_color=(60, 180, 60))
    button_confirm.draw(surface)
    buttons["confirm"] = button_confirm

    selected_world_name = WORLDS[selected_world_index]["name"]
    selected_surf       = font_small.render(f"Selected: {selected_world_name}", True, (255, 220, 50))
    surface.blit(selected_surf, selected_surf.get_rect(center=(WIDTH // 2, HEIGHT - 45)))

    return buttons


def draw_game_over(surface, font_small, font_large, player_level, player_xp, kills):
    dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dark_overlay.fill((0, 0, 0, 200))
    surface.blit(dark_overlay, (0, 0))

    title_surface = font_large.render("GAME OVER", True, (220, 30, 30))
    surface.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 150)))

    # show the session results
    result_lines = [
        f"Level Reached : {player_level}",
        f"XP Earned     : {player_xp}",
        f"Enemies Killed: {kills}",
    ]
    for line_index, line_text in enumerate(result_lines):
        line_surface = font_small.render(line_text, True, (220, 220, 220))
        surface.blit(line_surface, line_surface.get_rect(center=(WIDTH // 2, 240 + line_index * 40)))

    button_width  = 220
    button_height = 44
    button_left   = WIDTH // 2 - button_width // 2

    button_retry = Button(button_left, 390, button_width, button_height, "PLAY AGAIN", font_small,
                          color=(40, 100, 40), hover_color=(60, 160, 60))
    button_menu  = Button(button_left, 450, button_width, button_height, "MAIN MENU",  font_small)
    button_quit  = Button(button_left, 510, button_width, button_height, "QUIT",       font_small,
                          color=(120, 40, 40), hover_color=(180, 60, 60))

    for button in [button_retry, button_menu, button_quit]:
        button.draw(surface)

    return {"retry": button_retry, "menu": button_menu, "quit": button_quit}


def draw_victory(surface, font_small, font_large, player_level, player_xp, kills):
    dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dark_overlay.fill((0, 0, 0, 200))
    surface.blit(dark_overlay, (0, 0))

    title_surface = font_large.render("VICTORY!", True, (255, 215, 0))
    surface.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 150)))

    # show the session results
    result_lines = [
        f"Level Reached : {player_level}",
        f"XP Earned     : {player_xp}",
        f"Enemies Killed: {kills}",
    ]
    for line_index, line_text in enumerate(result_lines):
        line_surface = font_small.render(line_text, True, (220, 220, 220))
        surface.blit(line_surface, line_surface.get_rect(center=(WIDTH // 2, 240 + line_index * 40)))

    button_width  = 220
    button_height = 44
    button_left   = WIDTH // 2 - button_width // 2

    button_retry = Button(button_left, 390, button_width, button_height, "PLAY AGAIN", font_small,
                          color=(40, 100, 40), hover_color=(60, 160, 60))
    button_menu  = Button(button_left, 450, button_width, button_height, "MAIN MENU",  font_small)
    button_quit  = Button(button_left, 510, button_width, button_height, "QUIT",       font_small,
                          color=(120, 40, 40), hover_color=(180, 60, 60))

    for button in [button_retry, button_menu, button_quit]:
        button.draw(surface)

    return {"retry": button_retry, "menu": button_menu, "quit": button_quit}


def draw_stats_screen(surface, font_small, font_large, stats):
    surface.fill((10, 15, 25))

    title_surface = font_large.render("STATISTICS", True, (100, 200, 255))
    surface.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 80)))

    stat_rows = [
        ("Games Played",   str(stats.get("games_played",  0))),
        ("Total Kills",    str(stats.get("total_kills",   0))),
        ("Total Coins",    str(stats.get("total_coins",   0))),
        ("Highest Level",  str(stats.get("highest_level", 1))),
        ("Total XP",       str(stats.get("total_xp",      0))),
    ]

    for row_index, (label_text, value_text) in enumerate(stat_rows):
        label_surface = font_small.render(label_text, True, (180, 180, 180))
        value_surface = font_small.render(value_text, True, (255, 255, 255))

        row_y = 170 + row_index * 50
        surface.blit(label_surface, (160, row_y))
        surface.blit(value_surface, (550, row_y))

        pygame.draw.line(surface, (60, 60, 60), (150, row_y + 35), (WIDTH - 150, row_y + 35))

    button_back = Button(WIDTH // 2 - 110, HEIGHT - 70, 220, 44, "BACK TO MENU", font_small)
    button_back.draw(surface)

    return {"back": button_back}


def draw_settings_screen(surface, font_small, font_large, settings):
    surface.fill((10, 15, 25))

    title_surface = font_large.render("SETTINGS", True, (100, 200, 255))
    surface.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 80)))

    # label and settings key for each toggle row
    toggle_rows = [
        ("Music",            "music_enabled"),
        ("Sound Effects",    "sfx_enabled"),
        ("Show FPS",         "show_fps"),
        ("Enemy Indicators", "enemy_indicators"),
    ]

    buttons = {}
    for row_index, (label_text, settings_key) in enumerate(toggle_rows):
        row_y = 170 + row_index * 70

        label_surface = font_small.render(label_text, True, (200, 200, 200))
        surface.blit(label_surface, (160, row_y + 8))

        # green when on, red when off
        is_on        = settings.get(settings_key, True)
        button_text  = "ON"  if is_on else "OFF"
        button_color = (40, 120, 40) if is_on else (120, 40, 40)
        button_hover = (60, 180, 60) if is_on else (180, 60, 60)

        toggle_button = Button(WIDTH - 220, row_y, 100, 40, button_text, font_small,
                               color=button_color, hover_color=button_hover)
        toggle_button.draw(surface)
        buttons[f"toggle_{settings_key}"] = toggle_button

        pygame.draw.line(surface, (60, 60, 60), (150, row_y + 55), (WIDTH - 150, row_y + 55))

    button_back = Button(WIDTH // 2 - 110, HEIGHT - 70, 220, 44, "BACK TO MENU", font_small)
    button_back.draw(surface)
    buttons["back"] = button_back

    return buttons


def draw_pause_menu(surface, font_small, font_large):
    # semi-transparent overlay so the game is still visible behind the menu
    dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dark_overlay.fill((0, 0, 0, 160))
    surface.blit(dark_overlay, (0, 0))

    title_surface = font_large.render("PAUSED", True, (255, 255, 255))
    surface.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 170)))

    button_width  = 220
    button_height = 44
    button_left   = WIDTH // 2 - button_width // 2

    button_resume = Button(button_left, 270, button_width, button_height, "RESUME",    font_small,
                           color=(40, 100, 40), hover_color=(60, 160, 60))
    button_menu   = Button(button_left, 330, button_width, button_height, "MAIN MENU", font_small)
    button_quit   = Button(button_left, 390, button_width, button_height, "QUIT",      font_small,
                           color=(120, 40, 40), hover_color=(180, 60, 60))

    for button in [button_resume, button_menu, button_quit]:
        button.draw(surface)

    return {"resume": button_resume, "menu": button_menu, "quit": button_quit}