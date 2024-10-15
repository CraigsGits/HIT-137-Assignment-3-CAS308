import pygame
import random

# Initialise Pygame
pygame.init()

# Game settings 
SCREEN_WIDTH = 1000 
SCREEN_HEIGHT = 1000 
PLAYER_SPEED = 7 
JUMP_HEIGHT = 20 
GRAVITY = 0.5 
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 

# Initialise
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Hero game")

# Clock for frame rate
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("comic sans", 24)

# Load your Hero, Enemy and final boss emblems
# .png File location required for each
HeroIm = pygame.image.load('army.png').convert_alpha()
EnemyIm = pygame.image.load('elden.radahn.png').convert_alpha()
BossIm = pygame.image.load('elden.boss.png').convert_alpha()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(HeroIm, (80, 100)) # Scale hero image
        self.rect = self.image.get_rect() # Rectangle around emblem
        self.rect.center = (100, SCREEN_HEIGHT - 70) # Set starting position
        self.speed = PLAYER_SPEED # Set player movement speed
        self.jump_speed = JUMP_HEIGHT # Set player jump height
        self.y_velocity = 0 # Set initial vertical velocity
        self.on_ground = True # Set ground status
        self.health = 100 # Set inital health
        self.lives = 5 # Set inital lives

    def update(self):
        movement = pygame.key.get_pressed()
        
        # Horizontal movement
        if movement[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if movement[pygame.K_RIGHT]:
            self.rect.x += self.speed
            
        # Jumping
        if movement[pygame.K_SPACE] and self.on_ground:
            self.y_velocity = -self.jump_speed
            self.on_ground = False
        
        # Apply Gravity
        self.y_velocity += GRAVITY
        self.rect.y += self.y_velocity
        
        # Make sures player stays on ground
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.on_ground = True
            self.y_velocity = 0

    # Creates a ne projectile        
    def shoot(self):
        return Projectile(self.rect.right, self.rect.centery)
    
    # Makes sure player can take damage
    def take_damage(self, damage):
        self.health -= damage # Reduces health
        if self.health <= 0:
            self.lives -= 1 # Reduces lives if health depletes 
            self.health = 100 # Reset Health
            if self.lives <= 0:
                return True  # Game Over
        return False  # Not Game Over

# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5)) # Creates a surface for the projectile
        self.image.fill((255, 0, 0))  # Fill the surface with red
        self.rect = self.image.get_rect() # Rectangle around the surface
        self.rect.center = (x, y) # Sets projectile inital postion
        self.speed = 7 # Sets projectile speed 

    # Move the projectile
    def update(self):
        self.rect.x += self.speed 
        if self.rect.x > SCREEN_WIDTH: 
            self.kill() # Removes projectile if it leaves the screen

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y=None, speed=2, health=50):
        super().__init__()
        self.image = pygame.transform.scale(EnemyIm, (80, 100))  # Scale enemy image
        self.rect = self.image.get_rect() # Rectangle around the image
        if y is None:
            y = SCREEN_HEIGHT - 100  # Spawn near the bottom of the screen
        self.rect.center = (x, y) # Set enemy inital position
        self.speed = speed # Set enemy speed
        self.health = health # Set enemy health
    
    # Enemy Movement
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill() # Removes enemy when it leaves the screem
    
    # Ensures enemies can take damage
    def take_damage(self, damage):
        self.health -= damage # Reduces Health
        if self.health <= 0:
            self.kill() # Removes enemy if its health is depleted

# Boss Enemy Class (Enemy class with a few adjustments)
class BossEnemy(Enemy):
    def __init__(self, x, y=None):
        if y is None:
            y = SCREEN_HEIGHT - 100  # Spawn near the bottom of the screen
        super().__init__(x, y, speed=3, health=300) # Set inital position, speed and healh
        self.image = pygame.transform.scale(BossIm, (80, 120))  # Scale the Boss

# Collectible Class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y=None, kind="health"):
        super().__init__()
        self.image = pygame.Surface((20, 20)) # Creates a surface
        if kind == "health":
            self.image.fill((0, 255, 0))  # Fills the surface green for health
        elif kind == "life":
            self.image.fill((255, 255, 0))  # Fills the surface yellow for an extra life
        self.rect = self.image.get_rect()
        if y is None:
            y = SCREEN_HEIGHT - 100  # Spawns the collectable near the bottom of the screen
        self.rect.center = (x, y) # Sets collectable inital position 
        self.kind = kind # Type of collectable

    # Extra health and life 
    def apply(self, player):
        if self.kind == "health":
            player.health = min(100, player.health + 20) # Increase health
        elif self.kind == "life": 
            player.lives += 1 # Increase life
        self.kill() # Removes collectable after being collected

# Display the "Game Over" screen
def game_over_screen():
    screen.fill(WHITE) # Makes screen white
    game_over_text = font.render("GAME OVER", True, BLACK) # Produces game over text
    restart_text = font.render("Press SPACE to Restart", True, BLACK) # Produces restart insrutctions
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50)) # Center text
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50)) # Center tect
    pygame.display.flip() # Updates the display

    # Restarts or quits the game
    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # Quit
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                restart = True # Restarts of space is pressed

# Display the "Game Complete" screen
def game_complete_screen(): 
    screen.fill(WHITE) # Fills with white colour 
    game_complete_text = font.render("GAME COMPLETE", True, BLACK) # Produces game complete text
    restart_text = font.render("Press SPACE to Restart", True, BLACK) # Produces restart text 
    screen.blit(game_complete_text, (SCREEN_WIDTH//2 - game_complete_text.get_width()//2, SCREEN_HEIGHT//2 - 50)) # Center text
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50)) # Center text
    pygame.display.flip() # Updates the display
    
    # Quit or restart
    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # Quits 
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                restart = True # Restarts 

# Main game loop
def main_game():
    player = Player() # Creates player instance 
    all_sprites = pygame.sprite.Group() # Group for all sprites
    projectiles = pygame.sprite.Group() # Group for all projectiles
    enemies = pygame.sprite.Group() # Group for all enemies
    collectibles = pygame.sprite.Group() # Group for all collectables 

    all_sprites.add(player) # Add player to the all sprites group 

    score = 0 # Initalise score
    enemy_timer = 0 # Timer for enemies
    collectible_timer = 0 # Timer for collectables
    level = 1 # Initalise game level
    enemy_count = 0 # Initalise enemy count
    enemies_to_next_level = 10  # Number of enemies to defeat to progress to the next level

    boss_fight = False # Flag to indicate if its a boss fight

    # Main game loop
    running = True # Game is running 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Exits game if the window is closed 

            # Creates projectiles 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:  # Shoot
                    projectile = player.shoot()
                    all_sprites.add(projectile) 
                    projectiles.add(projectile)

        # Spawning enemies periodically
        if not boss_fight:
            enemy_timer += 1
            if enemy_timer >= 60:  # Every second
                enemy_timer = 0
                # Spawn an enemy on the right side of the screen in the bottom half
                enemy_speed = 2 + level  # Increase speed with level
                enemy_health = 50 + (level - 1) * 25  # Increase health with level
                y_position = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 100)  # Bottom half of the screen
                enemy = Enemy(SCREEN_WIDTH + 40, y_position, enemy_speed, enemy_health)
                all_sprites.add(enemy)
                enemies.add(enemy)

        # Spawning collectibles periodically
        collectible_timer += 1
        if collectible_timer >= 300:  # Every 5 seconds
            collectible_timer = 0
            kind = random.choice(["health", "life"])  # Randomly choose type of collectible
            collectible = Collectible(random.randint(100, SCREEN_WIDTH - 100), SCREEN_HEIGHT - 100, kind)
            all_sprites.add(collectible)
            collectibles.add(collectible)

        # Update
        all_sprites.update()

        # Check for collisions
        for projectile in projectiles:
            enemy_hit = pygame.sprite.spritecollide(projectile, enemies, False) # Checks if projectile hits enemies
            for enemy in enemy_hit:
                enemy.take_damage(25) # Enemy takes damage
                projectile.kill() # Remove sprojectile after hits enemy
                score += 10 # Increases score 
                if not enemy.alive():
                    enemy_count += 1 # Increases enemy count if an enemy is killed
                    if enemy_count >= enemies_to_next_level and level < 3:
                        level += 1 # Progress to the next level
                        enemy_count = 0 # Resets enemy count 
                    # Boss fight
                    elif level == 3 and enemy_count >= enemies_to_next_level and not boss_fight:
                        boss_fight = True # Starts boss fight if level 3 is reached
                        boss = BossEnemy(SCREEN_WIDTH + 80)  # The boss will spawn near the bottom of the screen
                        all_sprites.add(boss)
                        enemies.add(boss)

        # Player collides with enemies
        if pygame.sprite.spritecollide(player, enemies, False):
            if player.take_damage(10): # Player takes damage
                game_over_screen() # Displays game over screen
                return main_game()  # Restart the game

        # Player collects collectibles
        for collectible in pygame.sprite.spritecollide(player, collectibles, False):
            collectible.apply(player) # Apply collectible effect onto the player

        # If boss is defeated, the game is complete
        if boss_fight and not boss.alive():
            game_complete_screen() # Display game complete screen
            return main_game()  # Restart the game

        # Drawing
        screen.fill(WHITE) 

        # Draw all sprites
        all_sprites.draw(screen)

        # Score and player health/lives
        score_text = font.render(f"Score: {score}", True, BLACK)
        health_text = font.render(f"Health: {player.health}", True, BLACK)
        lives_text = font.render(f"Lives: {player.lives}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 40))
        screen.blit(lives_text, (10, 70))
        screen.blit(level_text, (10, 100))

        # Update the display
        pygame.display.flip()

        # Set frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main_game() # Satrts the game
