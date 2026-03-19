# Shooter Game README

## Project Overview

Welcome to the **Shooter Game** project! This project guides you through building a dynamic shooter game using **Python** and **Pygame**, leveraging **Object-Oriented Programming (OOP)** principles to create a modular and maintainable codebase.

In this game, you'll control a player who can move around the screen, shoot fireballs at enemies, collect coins, gain experience points (XP), and level up. As you progress, enemies spawn more frequently, and upon leveling up, you can choose upgrades to enhance your abilities. The game also features a health system, knockback mechanics, a game over screen, and an intuitive upgrade menu.

By following this guide, you'll not only build a functional game but also gain a deep understanding of OOP concepts applied in game development.

---

## Table of Contents

1. [Understanding What We’re Building](#1-understanding-what-we’re-building)
2. [Create the Game Class](#2-create-the-game-class)
   - [2.1. Why We Use a Class](#21-why-we-use-a-class)
   - [2.2. Define the Class Structure](#22-define-the-class-structure)
3. [The `__init__` Method (Constructor)](#3-the-init-method-constructor)
4. [The `create_random_background` Method](#4-the-create_random_background-method)
5. [The `run` Method](#5-the-run-method)
6. [The `handle_events` Method](#6-the-handle_events-method)
7. [The `update` Method](#7-the-update-method)
8. [The `draw` Method](#8-the-draw-method)
9. [The Main Section](#9-the-main-section)
10. [Putting It All Together](#10-putting-it-all-together)
11. [Recap: OOP Concepts Learned](#11-recap-oop-concepts-learned)
12. [Add a Health System to the Player](#12-add-a-health-system-to-the-player)
13. [Improve Enemy Movement and Knockback](#13-improve-enemy-movement-and-knockback)
14. [Add Coins](#14-add-coins)
15. [Adding More Game Mechanics in Game Class](#15-adding-more-game-mechanics-in-game-class)
16. [Game Over and Restart](#16-game-over-and-restart)
17. [Draw the Health UI](#17-draw-the-health-ui)
18. [Update the Player to Handle Fireballs](#18-update-the-player-to-handle-fireballs)
19. [The Fireball Class](#19-the-fireball-class)
20. [Add Shooting Controls in the Game Event Loop](#20-add-shooting-controls-in-the-game-event-loop)
21. [Fireball-Enemy Collision](#21-fireball-enemy-collision)
22. [Add XP and Leveling to the Player](#22-add-xp-and-leveling-to-the-player)
23. [Define a Helper Function for XP Requirements](#23-define-a-helper-function-for-xp-requirements)
24. [Coins Grant XP](#24-coins-grant-xp)
25. [Add a Level-Up Check](#25-add-a-level-up-check)
26. [The Upgrade Menu](#26-the-upgrade-menu)
   - [26.1. Tracking Menu State](#261-tracking-menu-state)
   - [26.2. `pick_random_upgrades(num)`](#262-pick_random_upgradesnum)
   - [26.3. Applying an Upgrade](#263-applying-an-upgrade)
   - [26.4. Handling Key Input for the Menu](#264-handling-key-input-for-the-menu)
   - [26.5. Rendering the Upgrade Menu](#265-rendering-the-upgrade-menu)
27. [Updated UI for XP/Level](#27-updated-ui-for-xplevel)
28. [Polish: More Enemies Each Level](#28-polish-more-enemies-each-level)
29. [Updating the Game’s Title](#29-updating-the-games-title)
30. [Testing and Verifying](#30-testing-and-verifying)
31. [Final OOP Recap](#31-final-oop-recap)
32. [Continue Expanding](#32-continue-expanding)

---

## 1. Understanding What We’re Building

We’re developing a **Shooter Game** using **Python** and **Pygame**. The game includes the following features:

- **Player Movement**: Navigate the player around the screen using keyboard inputs.
- **Shooting Mechanics**: Fire fireballs towards the mouse position or the nearest enemy.
- **Enemies**: Spawn enemies that chase the player. Enemies can be knocked back upon collision.
- **Coins**: Collect coins dropped by defeated enemies to gain XP.
- **Experience Points (XP) & Levels**: Gain XP to level up and choose upgrades.
- **Upgrade Menu**: Select upgrades that enhance player abilities upon leveling up.
- **Health System**: Manage player health with visual indicators.
- **Game Over Screen**: Display a game over screen with options to restart or quit.

The project emphasises understanding and applying **Object-Oriented Programming (OOP)** concepts to create a clean, maintainable, and scalable codebase.

---

## 2. Create the Game Class

### 2.1. Why We Use a Class

In **Object-Oriented Programming (OOP)**, a class serves as a **blueprint** for creating objects that encapsulate both data and behaviour. By creating a `Game` class, we can:

- **Encapsulate** all game-related data and functionalities within a single entity.
- **Organise** the codebase, making it easier to manage and extend.
- **Reuse** and **maintain** the code effectively as the project grows.

### 2.2. Define the Class Structure

Navigate to the section labeled:

```python
# --------------------------------------------------------------------------
#                             GAME CLASS
# --------------------------------------------------------------------------
```

Replace the `# TODO: Write Game Class` placeholder with the following skeleton:

```python
class Game:
    def __init__(self):
        # We'll initialize our Pygame window, load assets, etc. here.
        pass

    def create_random_background(self, width, height, floor_tiles):
        # We'll fill this method with code to create a background surface.
        pass

    def run(self):
        # This is our main game loop.
        pass

    def handle_events(self):
        # We'll handle player input or window events here.
        pass

    def update(self):
        # We'll update game objects, check collisions, etc. here.
        pass

    def draw(self):
        # We'll draw the background and objects to the screen.
        pass
```

This structure outlines the essential methods needed for the `Game` class. Each method will handle specific aspects of the game, promoting a clean and organised codebase.

---

## 3. The `__init__` Method (Constructor)

The constructor in Python is defined by the `__init__` method. It initializes the **instance attributes** of the class.

### Implementation

Replace the `pass` in the `__init__` method with:

```python
def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shooter")
    self.clock = pygame.time.Clock()

    self.assets = load_assets()

    font_path = os.path.join("assets", "PressStart2P.ttf")
    self.font_small = pygame.font.Font(font_path, 18)
    self.font_large = pygame.font.Font(font_path, 32)

    self.background = self.create_random_background(
        WIDTH, HEIGHT, self.assets["floor_tiles"]
    )

    self.running = True
    self.game_over = False
```

### Explanation

1. **Initialize Pygame**:
    ```python
    pygame.init()
    ```
    Sets up all Pygame modules.

2. **Set Up Display**:
    ```python
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shooter")
    ```
    Creates the game window and sets its title.

3. **Clock for FPS Control**:
    ```python
    self.clock = pygame.time.Clock()
    ```
    Manages the game's frame rate.

4. **Load Assets**:
    ```python
    self.assets = load_assets()
    ```
    Loads all game assets like images and animations.

5. **Load Fonts**:
    ```python
    font_path = os.path.join("assets", "PressStart2P.ttf")
    self.font_small = pygame.font.Font(font_path, 18)
    self.font_large = pygame.font.Font(font_path, 32)
    ```
    Loads custom fonts for rendering text in the game.

6. **Create Background**:
    ```python
    self.background = self.create_random_background(
        WIDTH, HEIGHT, self.assets["floor_tiles"]
    )
    ```
    Generates a randomly tiled background using floor tiles.

7. **Game State Flags**:
    ```python
    self.running = True
    self.game_over = False
    ```
    Tracks whether the game is running or has ended.

### OOP Concepts

- **Instance Attributes**: Attributes like `self.screen`, `self.clock`, and `self.assets` are tied to each instance of the `Game` class.
- **Encapsulation**: All game initialization logic is contained within the `__init__` method, keeping it organised.

---

## 4. The `create_random_background` Method

This method generates a background by randomly placing floor tiles across the game window.

### Implementation

Replace the `pass` in the `create_random_background` method with:

```python
def create_random_background(self, width, height, floor_tiles):
    bg = pygame.Surface((width, height))
    tile_w = floor_tiles[0].get_width()
    tile_h = floor_tiles[0].get_height()
    for y in range(0, height, tile_h):
        for x in range(0, width, tile_w):
            tile = random.choice(floor_tiles)
            bg.blit(tile, (x, y))
    return bg
```

### What’s Happening Here?

- **Create a Surface**:
    ```python
    bg = pygame.Surface((width, height))
    ```
    Creates a new blank surface for the background.

- **Tile Dimensions**:
    ```python
    tile_w = floor_tiles[0].get_width()
    tile_h = floor_tiles[0].get_height()
    ```
    Assumes all floor tiles are the same size and retrieves their dimensions.

- **Loop Through the Screen**:
    ```python
    for y in range(0, height, tile_h):
        for x in range(0, width, tile_w):
            tile = random.choice(floor_tiles)
            bg.blit(tile, (x, y))
    ```
    Iterates over the screen in tile-sized steps, randomly selecting and placing tiles.

- **Return the Background**:
    ```python
    return bg
    ```
    Returns the fully tiled background surface.

### OOP Concepts

- **Method Encapsulation**: The background creation logic is encapsulated within its own method, promoting modularity.

---

## 5. The `run` Method

The `run` method contains the **main game loop**, which continuously processes events, updates the game state, and renders visuals until the game is exited.

### Implementation

Replace the `pass` in the `run` method with:

```python
def run(self):
    while self.running:
        self.clock.tick(FPS)    # Control the game speed: at most FPS frames per second.
        self.handle_events()    # Check for user input or other events.

        if not self.game_over:
            self.update()       # Only update if the game is not over.

        self.draw()             # Draw everything on screen.

    pygame.quit()               # Cleanly close Pygame once we exit the loop.
```

- **Main Loop**:
    ```python
    while self.running:
    ```
    Keeps the game running until `self.running` is set to `False`.

- **Frame Rate Control**:
    ```python
    self.clock.tick(FPS)
    ```
    Ensures the game runs at a consistent frame rate.

- **Event Handling**:
    ```python
    self.handle_events()
    ```
    Processes all user inputs and events.

- **Game State Update**:
    ```python
    if not self.game_over:
        self.update()
    ```
    Updates game objects only if the game is not over.

- **Rendering**:
    ```python
    self.draw()
    ```
    Renders all game visuals to the screen.

- **Clean Exit**:
    ```python
    pygame.quit()
    ```
    Ensures Pygame shuts down cleanly when the loop exits.

### OOP Concepts

- **Control Flow Encapsulation**: The game loop's logic is encapsulated within the `run` method, centralising the game's control flow.

---

## 6. The `handle_events` Method

Handles all **user inputs** and **window events**, such as quitting the game.

### Implementation

Replace the `pass` in the `handle_events` method with:

```python
def handle_events(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False
```

- **Event Loop**:
    ```python
    for event in pygame.event.get():
    ```
    Iterates through all events in the event queue.

- **Quit Event**:
    ```python
    if event.type == pygame.QUIT:
        self.running = False
    ```
    Sets `self.running` to `False` when the user attempts to close the game window, causing the main loop to exit.

### OOP Concepts

- **Method Encapsulation**: All event handling logic is contained within the `handle_events` method, promoting separation of concerns.

---

## 7. The `update` Method

Updates the **game state** each frame, such as moving the player or enemies, handling collisions, and spawning new enemies.

### Implementation

Initially, keep the `update` method empty:

```python
def update(self):
    pass
```

### Future Expansion

As the project progresses, you'll add functionality to this method, such as:

- Updating player and enemy positions.
- Handling collisions.
- Spawning new enemies.
- Managing game mechanics like shooting and collecting coins.

### OOP Concepts

- **Single Responsibility Principle**: The `update` method focuses solely on updating the game state, keeping responsibilities clear and organised.

---

## 8. The `draw` Method

Renders all **game visuals** to the screen each frame.

### Implementation

Replace the `pass` in the `draw` method with:

```python
def draw(self):
    self.screen.blit(self.background, (0, 0))
    pygame.display.flip()
```

- **Draw Background**:
    ```python
    self.screen.blit(self.background, (0, 0))
    ```
    Renders the background surface onto the game window.

- **Update Display**:
    ```python
    pygame.display.flip()
    ```
    Updates the entire display to reflect the drawn content.

### OOP Concepts

- **Method Encapsulation**: All rendering logic is encapsulated within the `draw` method, maintaining a clear structure.

---

## 9. The Main Section

The main section of the script **instantiates** the `Game` class and **starts** the game loop.

### Implementation

At the very bottom of your file, add:

```python
if __name__ == "__main__":
    game = Game()  # Creates a Game instance
    game.run()     # Starts the game loop
```

### Explanation

1. **Instantiation**:
    ```python
    game = Game()
    ```
    Creates an instance of the `Game` class, initializing all game components.

2. **Run the Game**:
    ```python
    game.run()
    ```
    Starts the main game loop, effectively running the game.

### OOP Concepts

- **Instantiation**: Creating an object from a class blueprint.
- **Entry Point**: Ensures that the game runs only when the script is executed directly, not when imported as a module.

---

## 10. Putting It All Together

Your `Game` class should now look like this (excluding unchanged sections for brevity):

```python
# --------------------------------------------------------------------------
#                             GAME CLASS
# --------------------------------------------------------------------------

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shooter")
        self.clock = pygame.time.Clock()

        self.assets = load_assets()

        font_path = os.path.join("assets", "PressStart2P.ttf")
        self.font_small = pygame.font.Font(font_path, 18)
        self.font_large = pygame.font.Font(font_path, 32)

        self.background = self.create_random_background(
            WIDTH, HEIGHT, self.assets["floor_tiles"]
        )

        self.running = True
        self.game_over = False

    def create_random_background(self, width, height, floor_tiles):
        bg = pygame.Surface((width, height))
        tile_w = floor_tiles[0].get_width()
        tile_h = floor_tiles[0].get_height()
        for y in range(0, height, tile_h):
            for x in range(0, width, tile_w):
                tile = random.choice(floor_tiles)
                bg.blit(tile, (x, y))
        return bg

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            
            if not self.game_over:
                self.update()

            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

# --------------------------------------------------------------------------
#                               MAIN
# --------------------------------------------------------------------------

if __name__ == "__main__":
    game = Game()
    game.run()
```

With these changes, you have effectively transformed the original **scaffold** into the **expected code**. The main addition is the `Game` class with its methods and the final `main` logic to start the game. Everything else (constants, asset-loading functions, etc.) remains the same.

---

## 11. Recap: OOP Concepts Learned

1. **Class**: We created a `Game` class to encapsulate all the game’s data and logic.
2. **Constructor** (`__init__`): Used to set up instance attributes like the game window, clock, assets, etc.
3. **Methods**: Organised functionalities into methods such as `run`, `handle_events`, `update`, and `draw`.
4. **Encapsulation**: Kept all game-related logic and data within the `Game` class, promoting modularity and maintainability.
5. **Instantiation**: Created an instance of the `Game` class and ran the game loop.

At this point, you have a functional but minimal game structure. You can see a window, a randomly generated floor background, and a stable loop that exits cleanly when the user closes the window. You now have a strong *foundation* on which to build features like player movement, enemy AI, fireballs, coins, etc.

---

## 12. Add a Health System to the Player

### 12.1. New `health` Attribute

Inside the `Player` class `__init__` method, add:

```python
self.health = 5  # out of 5
```

This tracks the player’s health. The value `5` corresponds to the total frames in `assets["health"]` (there are 6 frames, from 0 to 5 hearts, so max is 5).

### 12.2. `take_damage` Method

Create a new method in `Player`:

```python
def take_damage(self, amount):
    self.health = max(0, self.health - amount)
```

- Subtracts `amount` from `self.health`.
- `max(0, self.health - amount)` ensures health never goes below zero.

### OOP Explanation

- **Encapsulation**: The `health` attribute and `take_damage` method are encapsulated within the `Player` class, ensuring that health management is handled internally.
- **Data Integrity**: By controlling how health is modified, we maintain consistent game behaviour.

---

## 13. Improve Enemy Movement and Knockback

### 13.1. Knockback Attributes

In the `Enemy` class `__init__`, add the following lines:

```python
self.knockback_dist_remaining = 0
self.knockback_dx = 0
self.knockback_dy = 0
```

These attributes track how far the enemy is knocked back and in which direction.

### 13.2. `move_toward_player` vs. `apply_knockback`

Inside `Enemy.update(self, player)`, modify it as follows:

```python
def update(self, player):
    if self.knockback_dist_remaining > 0:
        self.apply_knockback()
    else:
        self.move_toward_player(player)
    self.animate()
```

- If `knockback_dist_remaining` is above zero, call `apply_knockback`.
- Otherwise, the enemy chases the player.

### 13.3. `set_knockback` Method

Define the `set_knockback` method in the `Enemy` class:

```python
def set_knockback(self, px, py, dist):
    dx = self.x - px
    dy = self.y - py
    length = math.sqrt(dx*dx + dy*dy)
    if length != 0:
        self.knockback_dx = dx / length
        self.knockback_dy = dy / length
        self.knockback_dist_remaining = dist
```

- `(px, py)` is the player’s position at the time of collision, ensuring the knockback moves away from the player.
- Calculates a normalised direction vector for knockback.
- Sets the remaining knockback distance.

### OOP Explanation

- **State Management**: Enemies can be in different states (chasing or being knocked back).
- **Method Encapsulation**: Movement and knockback logic are encapsulated within their respective methods, promoting readability and maintainability.

---

## 14. Add Coins

### 14.1. Coin Class

Create a new `Coin` class:

```python
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # For now, it's just a small gold-coloured rectangle:
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
```

- **Attributes**:
  - `(x, y)`: Position of the coin.
  - `image`: Visual representation (a gold-coloured square).
  - `rect`: Rectangle for positioning and collision detection.

### 14.2. Managing Coins

In the `Game` class, ensure you have a `self.coins` list to store all coin instances.

- **Initialization**:
    ```python
    self.coins = []
    ```
- **Spawning Coins**: Coins are spawned when enemies are defeated (handled in collision logic).

### OOP Explanation

- **Encapsulation**: The `Coin` class encapsulates all data and behaviour related to coins.
- **Separation of Concerns**: Managing coins is handled separately from other game entities, promoting modularity.

---

## 15. Adding More Game Mechanics in Game Class

### 15.1. Enemy Spawning Over Time

Introduce enemy spawning mechanics to increase game difficulty over time.

#### Add Attributes in `Game.__init__`:

```python
self.enemy_spawn_timer = 0
self.enemy_spawn_interval = 60  # spawn every 60 frames (~1 second at 60 FPS)
self.enemies_per_spawn = 1     # number of enemies to spawn each time
```

#### Implement `spawn_enemies` Method:

```python
def spawn_enemies(self):
    self.enemy_spawn_timer += 1
    if self.enemy_spawn_timer >= self.enemy_spawn_interval:
        self.enemy_spawn_timer = 0

        for _ in range(self.enemies_per_spawn):
            # Choose a random side of the screen
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                x = random.randint(0, WIDTH)
                y = -SPAWN_MARGIN
            elif side == "bottom":
                x = random.randint(0, WIDTH)
                y = HEIGHT + SPAWN_MARGIN
            elif side == "left":
                x = -SPAWN_MARGIN
                y = random.randint(0, HEIGHT)
            else:
                x = WIDTH + SPAWN_MARGIN
                y = random.randint(0, HEIGHT)

            # Pick an enemy type
            enemy_type = random.choice(list(self.assets["enemies"].keys()))
            enemy = Enemy(x, y, enemy_type, self.assets["enemies"])
            self.enemies.append(enemy)
```

### 15.2. Checking Collisions

Implement collision detection for player-coin and player-enemy interactions.

#### `check_player_coin_collisions` Method:

```python
def check_player_coin_collisions(self):
    coins_collected = []
    for coin in self.coins:
        if coin.rect.colliderect(self.player.rect):
            coins_collected.append(coin)
            self.player.add_xp(1)

    for c in coins_collected:
        if c in self.coins:
            self.coins.remove(c)
```

#### `check_player_enemy_collisions` Method:

```python
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
```

### OOP Explanation

- **Encapsulation**: Collision logic is encapsulated within its own methods.
- **Data Integrity**: Ensures collected coins and enemy interactions are properly managed.

---

## 16. Game Over and Restart

### 16.1. Drawing a “Game Over” Overlay

Add a method `draw_game_over_screen` in the `Game` class:

```python
def draw_game_over_screen(self):
    # Dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    self.screen.blit(overlay, (0, 0))

    # Game Over text
    game_over_surf = self.font_large.render("GAME OVER!", True, (255, 0, 0))
    game_over_rect = game_over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    self.screen.blit(game_over_surf, game_over_rect)

    # Prompt to restart or quit
    prompt_surf = self.font_small.render("Press R to Play Again or ESC to Quit", True, (255, 255, 255))
    prompt_rect = prompt_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    self.screen.blit(prompt_surf, prompt_rect)
```

### 16.2. Handle Key Presses in `handle_events`

Modify the `handle_events` method to handle game over inputs:

```python
elif event.type == pygame.KEYDOWN:
    if self.game_over:
        if event.key == pygame.K_r:
            self.reset_game()
        elif event.key == pygame.K_ESCAPE:
            self.running = False
    else:
        # Normal gameplay
        if not self.in_level_up_menu:
            if event.key == pygame.K_SPACE:
                nearest_enemy = self.find_nearest_enemy()
                if nearest_enemy:
                    self.player.shoot_toward_enemy(nearest_enemy)
```

### OOP Explanation

- **State Management**: The game tracks whether it's in a game over state and responds accordingly.
- **Encapsulation**: Game over logic is encapsulated within specific methods and conditions.

---

## 17. Draw the Health UI

Display the player's health on the screen using heart images.

### Implementation

Add a method `draw_ui` in the `Game` class:

```python
def draw_ui(self):
    # Only show UI if not game over
    if self.game_over:
        return

    hp = max(0, min(self.player.health, 5))
    health_img = self.assets["health"][hp]
    self.screen.blit(health_img, (10, 10))

    # Display Level and XP
    level_text_surf = self.font_small.render(f"Level: {self.player.level}", True, (255, 255, 255))
    self.screen.blit(level_text_surf, (10, 40))

    xp_text_surf = self.font_small.render(f"XP: {self.player.xp}", True, (255, 255, 255))
    self.screen.blit(xp_text_surf, (10, 70))

    # Show XP needed for next level
    next_level_xp = xp_required_for_level(self.player.level)
    xp_to_next = max(0, next_level_xp - self.player.xp)
    xp_next_surf = self.font_small.render(f"Next Lvl XP: {xp_to_next}", True, (255, 255, 255))
    self.screen.blit(xp_next_surf, (10, 100))
```

### Explanation

1. **Health Display**:
    - Clamps the player's health between 0 and 5.
    - Selects the corresponding heart image from `assets["health"]`.
    - Draws the heart image at the top-left corner.

2. **Level and XP Display**:
    - Renders and displays the player's current level and XP.
    - Shows the XP required for the next level.

### OOP Concepts

- **Separation of Concerns**: UI rendering is handled separately from game logic.
- **Encapsulation**: The `draw_ui` method manages all UI-related rendering.

---

## 18. Update the Player to Handle Fireballs

### 18.1. New Player Attributes

Inside your `Player.__init__`, add attributes for firing fireballs:

```python
self.fireball_speed = 10
self.fireball_size = 10
self.fireball_count = 1
self.shoot_cooldown = 20
self.shoot_timer = 0
self.fireballs = []
```

**Why these attributes?**

- `fireball_speed`: How fast fireballs travel.
- `fireball_size`: Pixel dimensions of each fireball’s square.
- `fireball_count`: Number of fireballs fired at once and the spread width.
- `shoot_cooldown`: Frames to wait between shots (20 frames at 60 FPS is ~0.33 seconds).
- `shoot_timer`: Tracks time since the last shot.
- `fireballs`: A list to store active fireballs.

### 18.2. Tracking the Shoot Timer

In `Player.update`, increment the shoot timer each frame and manage fireballs:

```python
def update(self):
    self.shoot_timer += 1
    self.update_fireballs()  # New method to update and remove fireballs
    self.update_animation()
```

- `self.shoot_timer += 1`: Ensures shooting only occurs if enough frames have passed.

### 18.3. `update_fireballs` Method

Create a method to move fireballs and remove them if they go off-screen:

```python
def update_fireballs(self):
    for fireball in self.fireballs:
        fireball.update()

    # Keep only fireballs still within the game window
    self.fireballs = [
        b for b in self.fireballs 
        if 0 < b.x < WIDTH and 0 < b.y < HEIGHT
    ]
```

- Updates each fireball's position.
- Removes fireballs that exit the screen boundaries.

### OOP Explanation

- **Encapsulation**: Fireball management is handled within the `Player` class.
- **Data Integrity**: Ensures fireballs are properly tracked and removed when necessary.

---

## 19. The Fireball Class

Introduce a new `Fireball` class to handle fireball behaviour.

### Implementation

Add the `Fireball` class under the `# --------------------------------------------------------------------------
#                            FIREBALL CLASS
# --------------------------------------------------------------------------` section:

```python
class Fireball:
    def __init__(self, x, y, vx, vy, size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.image.fill((255, 255, 255))  # White fireball
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
```

### Explanation

- **Attributes**:
  - `(x, y)`: Fireball position.
  - `(vx, vy)`: Velocity in the x/y directions.
  - `size`: Size of the fireball.
  - `image` and `rect`: Standard Pygame logic for rendering.

- **Methods**:
  - `update()`: Moves the fireball by `(vx, vy)`.
  - `draw(surface)`: Draws fireball on screen.

### OOP Concepts

- **Encapsulation**: All fireball-related data and behaviours are contained within the `Fireball` class.
- **Modularity**: The fireball's functionality is separate from other game entities, promoting clean code organisation.

---

## 20. Add Shooting Controls in the Game Event Loop

Enable the player to shoot fireballs using keyboard and mouse inputs.

### Implementation

Modify the `handle_events` method in the `Game` class:

```python
def handle_events(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.KEYDOWN:
            if self.game_over:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
            else:
                # Normal gameplay
                if not self.in_level_up_menu:
                    if event.key == pygame.K_SPACE:
                        nearest_enemy = self.find_nearest_enemy()
                        if nearest_enemy:
                            self.player.shoot_toward_enemy(nearest_enemy)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not self.game_over and not self.in_level_up_menu:
                if event.button == 1:  # Left mouse button
                    self.player.shoot_toward_mouse(event.pos)
```

### Explanation

1. **Spacebar** (`K_SPACE`): Shoots towards the nearest enemy.
2. **Left Mouse Click** (`event.button == 1`): Shoots towards the mouse cursor's position.
3. **Game Over Handling**: Allows restarting or quitting when the game is over.

### OOP Concepts

- **Encapsulation**: Shooting controls are managed within the `Player` class, maintaining separation from the `Game` class.
- **Event Handling**: Cleanly separates input handling from game logic.

---

## 21. Fireball-Enemy Collision

Implement collision detection between fireballs and enemies to handle enemy defeat and coin drops.

### Implementation

Add the following method to the `Game` class:

```python
def check_fireball_enemy_collisions(self):
    fireballs_to_remove = []
    enemies_to_remove = []

    for fireball in self.player.fireballs:
        for enemy in self.enemies:
            if fireball.rect.colliderect(enemy.rect):
                fireballs_to_remove.append(fireball)
                enemies_to_remove.append(enemy)
                # Create a coin at the enemy's position
                coin = Coin(enemy.x, enemy.y)
                self.coins.append(coin)
                break  # Stop checking more enemies for this fireball

    # Remove the destroyed fireballs and enemies
    for f in fireballs_to_remove:
        if f in self.player.fireballs:
            self.player.fireballs.remove(f)
    for e in enemies_to_remove:
        if e in self.enemies:
            self.enemies.remove(e)
```

### Explanation

1. **Collision Detection**:
    - Iterates through all fireballs and enemies.
    - Checks if any fireball's rectangle collides with an enemy's rectangle.

2. **Handling Collisions**:
    - Marks collided fireballs and enemies for removal.
    - Spawns a `Coin` at the defeated enemy's position.

3. **Cleanup**:
    - Removes fireballs that have hit enemies.
    - Removes defeated enemies from the game.

### OOP Concepts

- **Encapsulation**: Collision logic is contained within its own method.
- **Data Integrity**: Ensures fireballs and enemies are properly managed upon collision.

---

## 22. Add XP and Leveling to the Player

Introduce an experience points (XP) system that allows the player to level up and gain upgrades.

### 22.1. Player Attributes

In the `Player` class `__init__`, add:

```python
self.xp = 0
self.level = 1
```

- `self.xp`: Current amount of XP the player has.
- `self.level`: Current level of the player (starts at 1).

### 22.2. XP Update Method

Add the following method to the `Player` class:

```python
def add_xp(self, amount):
    self.xp += amount
```

- Increments the player's XP by the specified amount.

### OOP Concepts

- **Encapsulation**: XP and level attributes are managed within the `Player` class.
- **Data Integrity**: Provides a controlled way to modify XP.

---

## 23. Define a Helper Function for XP Requirements

Create a helper function to determine the XP required for each level.

### Implementation

Add the following function in the **Helper Functions** section:

```python
def xp_required_for_level(level):
    """
    Formula for how much total XP is required to *reach* a given level.
    """
    return level * level * 5
    # Examples:
    #   level=1 -> 1 * 1 * 5 = 5 xp
    #   level=2 -> 2 * 2 * 5 = 20 xp (total xp needed)
    #   level=3 -> 3 * 3 * 5 = 45 xp, etc.
```

### Explanation

- **Formula**: `level * level * 5`
    - Increases XP requirement quadratically, making higher levels progressively harder to achieve.

### OOP Concepts

- **Abstraction**: Abstracts the XP calculation logic into a separate function, promoting reusability.

---

## 24. Coins Grant XP

Ensure that collecting coins increases the player's XP.

### Implementation

Modify the `check_player_coin_collisions` method in the `Game` class:

```python
def check_player_coin_collisions(self):
    coins_collected = []
    for coin in self.coins:
        if coin.rect.colliderect(self.player.rect):
            coins_collected.append(coin)
            self.player.add_xp(1)  # Increment XP by 1 for each coin collected

    for c in coins_collected:
        if c in self.coins:
            self.coins.remove(c)
```

### Explanation

- **XP Increment**:
    - Each time the player collects a coin, their XP increases by 1.
- **Coin Removal**:
    - Collected coins are removed from the game.

### OOP Concepts

- **Encapsulation**: The `Player` class manages its own XP through the `add_xp` method.
- **Data Integrity**: Ensures that XP is correctly incremented upon collecting coins.

---

## 25. Add a Level-Up Check

Check if the player has enough XP to level up and handle the leveling process.

### Implementation

Add the following method to the `Game` class:

```python
def check_for_level_up(self):
    """Use xp_required_for_level() to see if player qualifies for next level."""
    xp_needed = xp_required_for_level(self.player.level)
    if self.player.xp >= xp_needed:
        # Leveled up
        self.player.level += 1
        self.in_level_up_menu = True
        self.upgrade_options = self.pick_random_upgrades(3)

        # Increase enemy spawns each time we level up
        self.enemies_per_spawn += 1
```

### Explanation

1. **Determine XP Needed**:
    - Uses `xp_required_for_level` to find the XP required for the current level.

2. **Level Up Process**:
    - Increments the player's level.
    - Activates the level-up menu for selecting upgrades.
    - Increases the number of enemies spawned each interval to ramp up difficulty.

### OOP Concepts

- **Encapsulation**: Level-up logic is contained within its own method.
- **State Management**: Manages game state transitions upon leveling up.

---

## 26. The Upgrade Menu

Allow players to select upgrades upon leveling up, enhancing their abilities.

### 26.1. Tracking Menu State

In the `Game` class `__init__`, add:

```python
self.in_level_up_menu = False
self.upgrade_options = []
```

- `self.in_level_up_menu`: Flag to indicate if the upgrade menu is active.
- `self.upgrade_options`: List of available upgrades to present to the player.

### 26.2. `pick_random_upgrades(num)`

Create a method to select random upgrades:

```python
def pick_random_upgrades(self, num):
    possible_upgrades = [
        {"name": "Bigger Fireball",  "desc": "Fireball size +5"},
        {"name": "Faster Fireball",  "desc": "Fireball speed +2"},
        {"name": "Extra Fireball",   "desc": "Fire additional fireball"},
        {"name": "Shorter Cooldown", "desc": "Shoot more frequently"},
    ]
    return random.sample(possible_upgrades, k=num)
```

### What’s Happening?

- `possible_upgrades` is a list of dictionaries describing each potential upgrade.
- `random.sample` chooses `num` distinct items from that list.

### 26.3. Applying an Upgrade

Define `apply_upgrade` method:

```python
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
```

### Explanation

- **Each Named Upgrade**:
    - Modifies some aspect of the player’s shooting.
    - Ensures that `shoot_cooldown` never becomes zero, which would break the game.

### 26.4. Handling Key Input for the Menu

Modify the `handle_events` method to handle upgrade selections:

```python
elif event.type == pygame.KEYDOWN:
    if self.game_over:
        if event.key == pygame.K_r:
            self.reset_game()
        elif event.key == pygame.K_ESCAPE:
            self.running = False
    else:
        # Normal gameplay
        if not self.in_level_up_menu:
            if event.key == pygame.K_SPACE:
                nearest_enemy = self.find_nearest_enemy()
                if nearest_enemy:
                    self.player.shoot_toward_enemy(nearest_enemy)
        else:
            # In upgrade menu
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                index = event.key - pygame.K_1  # 0,1,2
                if 0 <= index < len(self.upgrade_options):
                    upgrade = self.upgrade_options[index]
                    self.apply_upgrade(self.player, upgrade)
                    self.in_level_up_menu = False
```

### Walkthrough

- **Press 1, 2, or 3**:
    - Corresponds to selecting the first, second, or third upgrade.
    - Applies the selected upgrade and closes the upgrade menu.

### 26.5. Rendering the Upgrade Menu

Add a method `draw_upgrade_menu` in the `Game` class:

```python
def draw_upgrade_menu(self):
    # Dark overlay behind the menu
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    self.screen.blit(overlay, (0, 0))

    # Title
    title_surf = self.font_large.render("Choose an Upgrade!", True, (255, 255, 0))
    title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3 - 50))
    self.screen.blit(title_surf, title_rect)

    # Options
    for i, upgrade in enumerate(self.upgrade_options):
        text_str = f"{i+1}. {upgrade['name']} - {upgrade['desc']}"
        option_surf = self.font_small.render(text_str, True, (255, 255, 255))
        line_y = HEIGHT // 3 + i * 40
        option_rect = option_surf.get_rect(center=(WIDTH // 2, line_y))
        self.screen.blit(option_surf, option_rect)
```

### Explanation

1. **Dark Overlay**:
    - Creates a semi-transparent black overlay to focus attention on the upgrade menu.

2. **Title**:
    - Displays "Choose an Upgrade!" prominently.

3. **Upgrade Options**:
    - Lists each available upgrade with corresponding numbers (1, 2, 3).
    - Players can select an upgrade by pressing the corresponding number key.

### OOP Concepts

- **Encapsulation**: Upgrade menu rendering is contained within its own method.
- **Modularity**: Upgrade selection logic is separated from other game functionalities.

---

## 27. Updated UI for XP/Level

Enhance the `draw_ui` method to display the player's level and XP information.

### Implementation

Modify the `draw_ui` method in the `Game` class:

```python
def draw_ui(self):
    # Only show UI if not game over
    if self.game_over:
        return

    hp = max(0, min(self.player.health, 5))
    health_img = self.assets["health"][hp]
    self.screen.blit(health_img, (10, 10))

    # Display Level and XP
    level_text_surf = self.font_small.render(f"Level: {self.player.level}", True, (255, 255, 255))
    self.screen.blit(level_text_surf, (10, 40))

    xp_text_surf = self.font_small.render(f"XP: {self.player.xp}", True, (255, 255, 255))
    self.screen.blit(xp_text_surf, (10, 70))

    # Show XP needed for next level
    next_level_xp = xp_required_for_level(self.player.level)
    xp_to_next = max(0, next_level_xp - self.player.xp)
    xp_next_surf = self.font_small.render(f"Next Lvl XP: {xp_to_next}", True, (255, 255, 255))
    self.screen.blit(xp_next_surf, (10, 100))
```

### Explanation

1. **Health Display**:
    - Shows the player's current health using heart images.

2. **Level and XP Display**:
    - Displays the player's current level and XP.

3. **XP to Next Level**:
    - Shows how much more XP the player needs to reach the next level.

### OOP Concepts

- **Separation of Concerns**: UI elements are managed separately from game logic.
- **Encapsulation**: The `draw_ui` method handles all UI-related rendering.

---

## 28. Polish: More Enemies Each Level

Increase game difficulty by spawning more enemies each time the player levels up.

### Implementation

In the `check_for_level_up` method within the `Game` class, ensure the following line is present:

```python
self.enemies_per_spawn += 1
```

### Explanation

- Each time the player levels up, `self.enemies_per_spawn` increments by 1.
- This results in more enemies spawning each time the spawn timer triggers, making the game progressively harder.

### OOP Concepts

- **State Management**: Dynamically adjusts game difficulty based on player progress.
- **Encapsulation**: The `enemies_per_spawn` attribute is managed within the `Game` class.

---

## 29. Updating the Game’s Title

Differentiate the final version by updating the game window title to reflect added features.

### Implementation

In the `Game.__init__` method, set a more descriptive title:

```python
pygame.display.set_caption("Shooter: Game Over & Replay, More Enemies, XP Scaling")
```

### Explanation

- Provides clarity on the game's current version and features.
- Helps during development to identify different builds.

### OOP Concepts

- **Instance Attributes**: The game title is an instance attribute managed within the `Game` class.

---

## 30. Testing and Verifying

Ensure all implemented features work as intended.

### Checklist

1. **Coins**:
    - Spawn when enemies are hit by fireballs.
    - Collecting coins increases player XP.

2. **Level Up**:
    - Occurs when XP meets or exceeds the required threshold.
    - Triggers the upgrade menu.

3. **Upgrades**:
    - Pressing 1, 2, or 3 selects the corresponding upgrade.
    - Upgrades modify player attributes accordingly.

4. **Spawning**:
    - Each level up increases `self.enemies_per_spawn`, leading to more enemies spawning.

5. **UI**:
    - Displays health, level, XP, and XP needed for the next level correctly.

6. **Game Over**:
    - Occurs when player health reaches zero.
    - Displays the game over screen with options to restart or quit.

### OOP Concepts

- **Encapsulation**: Each feature is encapsulated within its respective class and method.
- **Modularity**: Testing each module independently ensures reliable and maintainable code.

---

## 31. Final OOP Recap

Throughout this project, we've applied several core OOP concepts:

1. **Encapsulation**: 
    - Managed game state and logic within dedicated classes (`Player`, `Enemy`, `Fireball`, `Coin`, `Game`).
    - Each class handles its own data and behaviours, promoting clean code organisation.

2. **Abstraction**:
    - Simplified complex systems (e.g., XP requirements, upgrade mechanics) through helper functions and encapsulated methods.
    - Allowed focusing on high-level game logic without getting bogged down by implementation details.

3. **Inheritance** (Potential Future Use):
    - Although not utilised yet, classes like `Player` and `Enemy` can inherit from a common base class in future expansions.

4. **Polymorphism** (Potential Future Use):
    - Facilitated treating different objects (e.g., various enemy types) uniformly, enabling flexibility and scalability.

5. **Single Responsibility Principle**:
    - Each class and method is responsible for a single aspect of the game, making the codebase easier to understand and maintain.

### Benefits Observed

- **Modularity**: Easy to add, remove, or modify features without affecting unrelated parts of the code.
- **Maintainability**: Organised structure simplifies debugging and future enhancements.
- **Reusability**: Classes and methods can be reused or extended for additional features or projects.

---

## 32. Continue Expanding

Congratulations on reaching the final expected code! Your game now includes comprehensive features like health management, enemy dynamics, shooting mechanics, XP and leveling, and an upgrade system. However, the journey doesn't end here. Here are some suggestions to further enhance your game:

1. **Special Enemy Types**:
    - Introduce enemies with unique behaviours or abilities.
    - Implement boss enemies with higher health and more complex attack patterns.

2. **Fireball Patterns**:
    - Create varied fireball types (e.g., homing fireballs, spread shots).
    - Implement power-ups that modify fireball behaviour temporarily.

3. **Persistent Scoring System**:
    - Track and display the player's score based on enemies defeated and coins collected.
    - Save high scores across game sessions.

4. **Sound Effects and Music**:
    - Add audio feedback for shooting, enemy defeats, and game over events.
    - Implement background music to enhance the gaming experience.

5. **Level Design**:
    - Design multiple levels with increasing difficulty and unique layouts.
    - Introduce obstacles or platforms for more strategic gameplay.

6. **Player Upgrades and Abilities**:
    - Expand the upgrade menu with more diverse and impactful upgrades.
    - Implement abilities like shields, dashes, or area-of-effect attacks.

7. **User Interface Enhancements**:
    - Add menus, settings, and pause functionality.
    - Implement visual effects like particle systems for explosions or fireball trails.

8. **Mobile Compatibility**:
    - Optimise controls for touch interfaces if targeting mobile platforms.

### OOP Concepts for Future Features

- **Inheritance**: Create base classes for enemies or fireballs to facilitate polymorphism.
- **Composition**: Combine multiple objects to build more complex behaviours or features.
- **Design Patterns**: Utilise patterns like Factory for enemy creation or Observer for event handling to further enhance code quality.

---

**Congratulations!** By following this comprehensive guide, you've built a robust shooter game that effectively utilises Object-Oriented Programming principles. Continue experimenting, learning, and expanding your project to create an even more engaging and polished game. Happy coding!

---

**Note**: While American English spellings have been converted to Australian English in the explanatory text, **code snippets** remain unchanged to preserve their functionality and compatibility with Pygame.