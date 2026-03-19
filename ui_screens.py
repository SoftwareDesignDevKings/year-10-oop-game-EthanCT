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

    title_surf = font_large.render("DUNGEON SHOOTER", True, (255, 200, 50))
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 130))
    surface.blit(title_surf, title_rect)

    subtitle_surf = font_small.render("Survive the endless hordes", True, (180, 180, 180))
    subtitle_rect = subtitle_surf.get_rect(center=(WIDTH // 2, 185))
    surface.blit(subtitle_surf, subtitle_rect)

    btn_w, btn_h = 260, 44
    cx = WIDTH // 2 - btn_w // 2

    btn_play     = Button(cx, 250, btn_w, btn_h, "PLAY",          font_small)
    btn_worlds   = Button(cx, 310, btn_w, btn_h, "SELECT WORLD",  font_small)
    btn_stats    = Button(cx, 370, btn_w, btn_h, "STATS",         font_small)
    btn_settings = Button(cx, 430, btn_w, btn_h, "SETTINGS",      font_small)
    btn_quit     = Button(cx, 490, btn_w, btn_h, "QUIT",          font_small,
                          color=(120, 40, 40), hover_color=(180, 60, 60))

    for btn in [btn_play, btn_worlds, btn_stats, btn_settings, btn_quit]:
        btn.draw(surface)

    return {
        "play"    : btn_play,
        "worlds"  : btn_worlds,
        "stats"   : btn_stats,
        "settings": btn_settings,
        "quit"    : btn_quit,
    }


def draw_world_select(surface, font_small, font_large, selected_world_index):
    surface.fill((15, 20, 35))

    title_surf = font_large.render("SELECT WORLD", True, (100, 200, 255))
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 80))
    surface.blit(title_surf, title_rect)

    buttons = {}
    btn_w, btn_h = 320, 50

    for i, world in enumerate(WORLDS):
        # highlight the selected world with a gold border
        border_col = (255, 220, 50) if i == selected_world_index else (150, 150, 150)
        btn = Button(WIDTH // 2 - btn_w // 2, 160 + i * 80, btn_w, btn_h,
                     world["name"], font_small,
                     color=(40, 60, 100), hover_color=(60, 90, 150),
                     border_color=border_col, border_width=3)
        btn.draw(surface)
        buttons[f"world_{i}"] = btn

        # short description shown below each world button
        desc_surf = font_small.render(world["desc"], True, (160, 160, 160))
        desc_rect = desc_surf.get_rect(center=(WIDTH // 2, 160 + i * 80 + btn_h + 10))
        surface.blit(desc_surf, desc_rect)

    btn_back = Button(30, HEIGHT - 60, 140, 40, "BACK", font_small,
                      color=(60, 60, 60), hover_color=(100, 100, 100))
    btn_back.draw(surface)
    buttons["back"] = btn_back

    btn_confirm = Button(WIDTH - 200, HEIGHT - 60, 170, 40, "CONFIRM", font_small,
                         color=(40, 120, 40), hover_color=(60, 180, 60))
    btn_confirm.draw(surface)
    buttons["confirm"] = btn_confirm

    sel_name = WORLDS[selected_world_index]["name"]
    sel_surf = font_small.render(f"Selected: {sel_name}", True, (255, 220, 50))
    sel_rect = sel_surf.get_rect(center=(WIDTH // 2, HEIGHT - 45))
    surface.blit(sel_surf, sel_rect)

    return buttons


def draw_game_over(surface, font_small, font_large, player_level, player_xp, kills):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surface.blit(overlay, (0, 0))

    go_surf = font_large.render("GAME OVER", True, (220, 30, 30))
    go_rect = go_surf.get_rect(center=(WIDTH // 2, 150))
    surface.blit(go_surf, go_rect)

    # show the session results
    stats_lines = [
        f"Level Reached : {player_level}",
        f"XP Earned     : {player_xp}",
        f"Enemies Killed: {kills}",
    ]
    for i, line in enumerate(stats_lines):
        s = font_small.render(line, True, (220, 220, 220))
        r = s.get_rect(center=(WIDTH // 2, 240 + i * 40))
        surface.blit(s, r)

    btn_w, btn_h = 220, 44
    cx = WIDTH // 2 - btn_w // 2

    btn_retry  = Button(cx, 390, btn_w, btn_h, "PLAY AGAIN", font_small,
                        color=(40, 100, 40), hover_color=(60, 160, 60))
    btn_menu   = Button(cx, 450, btn_w, btn_h, "MAIN MENU",  font_small)
    btn_quit   = Button(cx, 510, btn_w, btn_h, "QUIT",       font_small,
                        color=(120, 40, 40), hover_color=(180, 60, 60))

    for btn in [btn_retry, btn_menu, btn_quit]:
        btn.draw(surface)

    return {"retry": btn_retry, "menu": btn_menu, "quit": btn_quit}


def draw_victory(surface, font_small, font_large, player_level, player_xp, kills):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surface.blit(overlay, (0, 0))

    v_surf = font_large.render("VICTORY!", True, (255, 215, 0))
    v_rect = v_surf.get_rect(center=(WIDTH // 2, 150))
    surface.blit(v_surf, v_rect)

    # show the session results
    stats_lines = [
        f"Level Reached : {player_level}",
        f"XP Earned     : {player_xp}",
        f"Enemies Killed: {kills}",
    ]
    for i, line in enumerate(stats_lines):
        s = font_small.render(line, True, (220, 220, 220))
        r = s.get_rect(center=(WIDTH // 2, 240 + i * 40))
        surface.blit(s, r)

    btn_w, btn_h = 220, 44
    cx = WIDTH // 2 - btn_w // 2

    btn_retry = Button(cx, 390, btn_w, btn_h, "PLAY AGAIN", font_small,
                       color=(40, 100, 40), hover_color=(60, 160, 60))
    btn_menu  = Button(cx, 450, btn_w, btn_h, "MAIN MENU",  font_small)
    btn_quit  = Button(cx, 510, btn_w, btn_h, "QUIT",       font_small,
                       color=(120, 40, 40), hover_color=(180, 60, 60))

    for btn in [btn_retry, btn_menu, btn_quit]:
        btn.draw(surface)

    return {"retry": btn_retry, "menu": btn_menu, "quit": btn_quit}


def draw_stats_screen(surface, font_small, font_large, stats):
    surface.fill((10, 15, 25))

    title_surf = font_large.render("STATISTICS", True, (100, 200, 255))
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 80))
    surface.blit(title_surf, title_rect)

    rows = [
        ("Games Played",   str(stats.get("games_played",  0))),
        ("Total Kills",    str(stats.get("total_kills",   0))),
        ("Total Coins",    str(stats.get("total_coins",   0))),
        ("Highest Level",  str(stats.get("highest_level", 1))),
        ("Total XP",       str(stats.get("total_xp",      0))),
    ]

    for i, (label, value) in enumerate(rows):
        label_surf = font_small.render(label, True, (180, 180, 180))
        value_surf = font_small.render(value, True, (255, 255, 255))

        y_pos = 170 + i * 50
        surface.blit(label_surf, (160, y_pos))
        surface.blit(value_surf, (550, y_pos))

        pygame.draw.line(surface, (60, 60, 60), (150, y_pos + 35), (WIDTH - 150, y_pos + 35))

    btn_back = Button(WIDTH // 2 - 110, HEIGHT - 70, 220, 44, "BACK TO MENU", font_small)
    btn_back.draw(surface)

    return {"back": btn_back}


def draw_settings_screen(surface, font_small, font_large, settings):
    surface.fill((10, 15, 25))

    title_surf = font_large.render("SETTINGS", True, (100, 200, 255))
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 80))
    surface.blit(title_surf, title_rect)

    # label and settings key for each toggle row
    toggle_rows = [
        ("Music",            "music_enabled"),
        ("Sound Effects",    "sfx_enabled"),
        ("Show FPS",         "show_fps"),
        ("Enemy Indicators", "enemy_indicators"),
    ]

    buttons = {}
    for i, (label, key) in enumerate(toggle_rows):
        y_pos = 170 + i * 70

        label_surf = font_small.render(label, True, (200, 200, 200))
        surface.blit(label_surf, (160, y_pos + 8))

        # green when on, red when off
        is_on       = settings.get(key, True)
        btn_text    = "ON"  if is_on else "OFF"
        btn_color   = (40, 120, 40)   if is_on else (120, 40, 40)
        btn_hover   = (60, 180, 60)   if is_on else (180, 60, 60)

        btn = Button(WIDTH - 220, y_pos, 100, 40, btn_text, font_small,
                     color=btn_color, hover_color=btn_hover)
        btn.draw(surface)
        buttons[f"toggle_{key}"] = btn

        pygame.draw.line(surface, (60, 60, 60), (150, y_pos + 55), (WIDTH - 150, y_pos + 55))

    btn_back = Button(WIDTH // 2 - 110, HEIGHT - 70, 220, 44, "BACK TO MENU", font_small)
    btn_back.draw(surface)
    buttons["back"] = btn_back

    return buttons


def draw_pause_menu(surface, font_small, font_large):
    # semi-transparent overlay so the game is still visible behind the menu
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    title_surf = font_large.render("PAUSED", True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 170))
    surface.blit(title_surf, title_rect)

    btn_w, btn_h = 220, 44
    cx = WIDTH // 2 - btn_w // 2

    btn_resume = Button(cx, 270, btn_w, btn_h, "RESUME",    font_small,
                        color=(40, 100, 40), hover_color=(60, 160, 60))
    btn_menu   = Button(cx, 330, btn_w, btn_h, "MAIN MENU", font_small)
    btn_quit   = Button(cx, 390, btn_w, btn_h, "QUIT",      font_small,
                        color=(120, 40, 40), hover_color=(180, 60, 60))

    for btn in [btn_resume, btn_menu, btn_quit]:
        btn.draw(surface)

    return {"resume": btn_resume, "menu": btn_menu, "quit": btn_quit}