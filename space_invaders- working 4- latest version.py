import pygame
import random
pygame.init()

# Set up the display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Enemies, Bullets, and Power-Ups')

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#load the player sprite
player_image = pygame.image.load('zhead.png')
player_rect = player_image.get_rect()
player_rect.topleft =(320, 440)

#initial position of the player
circle_x = 320
circle_y = 440  # Start at the bottom of the screen

# Movement speed of the player
player_speed = 4

# Enemy properties
enemy_width = 50
enemy_height = 50
enemy_speed = 1
enemies = [pygame.Rect(random.randint(0, 640 - enemy_width), 0, enemy_width, enemy_height) for _ in range(5)]

# Extra enemy properties (half the size, twice the speed)
extra_enemy_width = 25
extra_enemy_height = 25
extra_enemy_speed = 2
extra_enemies = []

# Bullet properties
bullet_width = 5
bullet_height = 20
bullet_speed = 5
bullets = []

# Power-up properties
power_up_size = 30
power_ups = [pygame.Rect(random.randint(0, 640 - power_up_size), random.randint(0, 480 - power_up_size), power_up_size, power_up_size) for _ in range(3)]

# Extra life power-up
extra_life_power_up = None
extra_lives = 1
extra_life_given_for_score = 0  # Track the score when the last extra life was given

# Score
score = 0
high_score = 0
font = pygame.font.Font(None, 36)  # Use a default font and size 36

# Function to create a new enemy
def create_enemy():
    x = random.randint(0, 640 - enemy_width)
    y = 0 - enemy_height
    return pygame.Rect(x, y, enemy_width, enemy_height)

# Function to create a new extra enemy
def create_extra_enemy():
    x = random.randint(0, 640 - extra_enemy_width)
    y = 0 - extra_enemy_height
    return pygame.Rect(x, y, extra_enemy_width, extra_enemy_height)

# Function to create a new power-up
def create_power_up():
    x = random.randint(0, 640 - power_up_size)
    y = random.randint(0, 480 - power_up_size)
    return pygame.Rect(x, y, power_up_size, power_up_size)

# Function to create an extra life power-up as a red heart shape
def create_extra_life_power_up():
    x = random.randint(0, 640 - power_up_size)
    y = random.randint(0, 480 - power_up_size)
    return pygame.Rect(x, y, power_up_size, power_up_size)

# Function to draw a heart shape
def draw_heart(screen, color, rect):
    half_width = rect.width // 2
    pygame.draw.circle(screen, color, (rect.x + half_width // 2, rect.y + half_width // 2), half_width // 2)
    pygame.draw.circle(screen, color, (rect.x + 3 * half_width // 2, rect.y + half_width // 2), half_width // 2)
    pygame.draw.polygon(screen, color, [(rect.x, rect.y + half_width // 2), (rect.x + rect.width, rect.y + half_width // 2), (rect.x + half_width, rect.y + rect.height)])
# Set up the clock to control the frame rate
clock = pygame.time.Clock()

# Power-up effect states
power_up_effects = {
    'faster_bullets': False,
    'bigger_bullets': False,
    'spread_shot': False
}

# Power-up duration
power_up_timer = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        circle_x -= player_speed
    if keys[pygame.K_RIGHT]:
        circle_x += player_speed
    if keys[pygame.K_UP]:
        circle_y -= player_speed
    if keys[pygame.K_DOWN]:
        circle_y += player_speed
    if keys[pygame.K_SPACE]:
        if len(bullets) < 3:
            if power_up_effects['spread_shot']:
                bullets.append(pygame.Rect(circle_x - 10, circle_y - 20, bullet_width, bullet_height))
                bullets.append(pygame.Rect(circle_x, circle_y - 20, bullet_width, bullet_height))
                bullets.append(pygame.Rect(circle_x + 10, circle_y - 20, bullet_width, bullet_height))
            else:
                bullets.append(pygame.Rect(circle_x, circle_y - 20, bullet_width, bullet_height))

    screen.fill(WHITE)  # Fill the screen with white
    pygame.draw.circle(screen, GREEN, (circle_x, circle_y), 20)  # Draw the player circle

    # Move and draw enemies
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > 480:
            enemies.remove(enemy)
            enemies.append(create_enemy())
        pygame.draw.rect(screen, BLUE, enemy)

    # Move and draw extra enemies
    for extra_enemy in extra_enemies:
        extra_enemy.y += extra_enemy_speed
        if extra_enemy.y > 480:
            extra_enemies.remove(extra_enemy)
            extra_enemies.append(create_extra_enemy())
        pygame.draw.rect(screen, RED, extra_enemy)

    # Move bullets
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)
        pygame.draw.rect(screen, RED, bullet)

    # Check for bullet collisions with enemies
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10
                break
        for extra_enemy in extra_enemies:
            if bullet.colliderect(extra_enemy):
                extra_enemies.remove(extra_enemy)
                score += 20  # Extra score for extra enemies
                break

    # Check for collision with power-ups
    player_rect = pygame.Rect(circle_x - 20, circle_y - 20, 40, 40)
    for power_up in power_ups:
        if player_rect.colliderect(power_up):
            power_ups.remove(power_up)
            score += 50  # Bonus score for collecting power-up
            # Randomly select a power-up effect
            effect = random.choice(['faster_bullets', 'bigger_bullets', 'spread_shot'])
            power_up_effects[effect] = True
            power_up_timer = 300  # Effect lasts for 5 seconds (60 FPS * 5 seconds)

    # Draw power-ups
    for power_up in power_ups:
        pygame.draw.rect(screen, YELLOW, power_up)

    # Ensure power-ups are periodically added
    if len(power_ups) < 3:
        power_ups.append(create_power_up())

    # Ensure new enemies are continuously added
    if len(enemies) < 5:
        enemies.append(create_enemy())

    # Ensure new extra enemies are added when score is 1500 or more
    if score >= 1500 and len(extra_enemies) < 5:
        extra_enemies.append(create_extra_enemy())

    # Apply power-up effects
    if power_up_effects['faster_bullets']:
        bullet_speed = 20
    else:
        bullet_speed = 15

    if power_up_effects['bigger_bullets']:
        bullet_width, bullet_height = 10, 40
    else:
        bullet_width, bullet_height = 5, 20

    # Decrement power-up timer
    if power_up_timer > 0:
        power_up_timer -= 1
    else:
        power_up_effects = {
            'faster_bullets': False,
            'bigger_bullets': False,
            'spread_shot': False
        }

    # Create extra life power-up when the score reaches multiples of 5000 and only once per 1000 score increment
    if score >= 5000 and score // 5000 > extra_life_given_for_score:
        extra_life_power_up = create_extra_life_power_up()
        extra_life_given_for_score = score // 5000

    # Draw extra life power-up as a heart
    if extra_life_power_up:
        draw_heart(screen, RED, extra_life_power_up)

    # Check for collision with extra life power-up
    if extra_life_power_up and player_rect.colliderect(extra_life_power_up):
        extra_lives += 1
        extra_life_power_up = None
        score += 100  # Extra bonus score for collecting extra life

    # Check for collision between player and enemies
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            if extra_lives > 0:
                extra_lives -= 1
                circle_x, circle_y = 320, 440  # Reset player position
    # Check for collision between player and enemies
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            if extra_lives > 0:
                extra_lives -= 1
                circle_x, circle_y = 320, 440  # Reset player position
            else:
                running = False
                print("Game Over")
                if score > high_score:
                    high_score = score

    # Render the score text
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    high_score_text = font.render(f'High Score: {high_score}', True, (0, 0, 0))
    extra_lives_text = font.render(f'Lives: {extra_lives}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))  # Position the score at the top-left corner
    screen.blit(high_score_text, (10, 40))  # Position the high score below the score
    screen.blit(extra_lives_text, (10, 70))  # Position the lives below the high score

    pygame.display.flip()  # Update the display

    clock.tick(60)  # Control the frame rate

# Game over loop to keep the window open
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill(WHITE)
    game_over_text = font.render('Game Over', True, (0, 0, 0))
    screen.blit(game_over_text, (250, 220))
    high_score_text = font.render(f'High Score: {high_score}', True, (0, 0, 0))
    screen.blit(high_score_text, (250, 260))
    pygame.display.flip()
