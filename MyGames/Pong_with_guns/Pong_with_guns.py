import random
import sys
import pygame

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SPEED = 5
PADDLE_SPEED = 5
BULLET_SPEED = 5
BULLET_BALL_VELOCITY = 3  # Amount added when bullet hits ball
WHITE = (255, 255, 255)
HIT = (255, 185, 185)
LOW = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 185, 50)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with Guns")

# Initializing paddles and ball
player_paddle = pygame.Rect(50, HEIGHT // 2 - 50, 10, 100)
opponent_paddle = pygame.Rect(WIDTH - 60, HEIGHT // 2 - 50, 10, 100)
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_direction = [1, 1]  # down-right

# Initialize bullets for player and computer
bullets = []
computer_bullets = []

# Initialize explosion variables
explosion_radius = 0
explosion_position = (0, 0)
explosion_active = False

# Initialize player and opponent paddle size
player_paddle_width = 10
player_paddle_height = 100
opponent_paddle_width = 10
opponent_paddle_height = 100

# Initialize player and opponent paddle colors
player_paddle_color = WHITE
opponent_paddle_color = WHITE

# Score
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

# Computer variables
opponent_speed = 5
computer_bullet_timer = 60  # Lower timer for more bullets

# Main game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Shoot a bullet from the player
            bullet = pygame.Rect(
                player_paddle.right, player_paddle.centery - 2, 10, 20
            )
            bullets.append(bullet)

    # Move player based on keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    elif keys[pygame.K_s] and player_paddle.bottom < HEIGHT:
        player_paddle.y += PADDLE_SPEED
    elif keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    elif keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
        player_paddle.y += PADDLE_SPEED

    # Move computer paddle
    if ball.centery < opponent_paddle.centery:
        opponent_paddle.y -= opponent_speed
    elif ball.centery > opponent_paddle.centery:
        opponent_paddle.y += opponent_speed

    # Computer bullet logic operations
    computer_bullet_timer -= 1
    if computer_bullet_timer <= 0:
        # Shoot bullet
        computer_bullet = pygame.Rect(
            opponent_paddle.left - 10, opponent_paddle.centery - 2, 10, 20
        )
        computer_bullets.append(computer_bullet)
        # Reset timer
        computer_bullet_timer = 60

        # Bullet directions
    for bullet in bullets:
        bullet.x += BULLET_SPEED

    for computer_bullet in computer_bullets:
        computer_bullet.x -= BULLET_SPEED

    # Remove bullets that go off screen
    bullets = [bullet for bullet in bullets if bullet.right <= WIDTH]
    computer_bullets = [bullet for bullet in computer_bullets if bullet.left >= 0]

    # Ball directions
    ball.x += ball_direction[0] * BALL_SPEED
    ball.y += ball_direction[1] * BALL_SPEED

    # Ball and wall collision
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_direction[1] *= -1

    # check for ball leaving right side
    if ball.left > WIDTH:
        # Respawn ball in center with random direction
        ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        ball_direction = [random.choice([1, -1]), random.choice([1, -1])]
        # Player point
        player_score += 1
    elif ball.right < 0:
        # check for ball leaving left side
        ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        ball_direction = [random.choice([1, -1]), random.choice([1, -1])]
        # Opponent point
        opponent_score += 1

    # Ball and paddle collisions
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_direction[0] *= -1

    # Ball and bullet collisions
    for bullet in bullets:
        if ball.colliderect(bullet):
            # Change direction and add velocity
            bullet_direction = 1 if ball_direction[0] > 0 else -1
            ball_direction[0] = -ball_direction[0] + bullet_direction * BULLET_BALL_VELOCITY

            # Explosion for ball, smaller radius than paddle explosion
            explosion_position = (ball.centerx, ball.centery)
            explosion_radius = 10
            explosion_active = True

            bullets.remove(bullet)

    # Ball and computer bullet collisions
    for computer_bullet in computer_bullets:
        if ball.colliderect(computer_bullet):
            # Change direction and add velocity
            bullet_direction = 1 if ball_direction[0] > 0 else -1
            ball_direction[0] = -ball_direction[0] + bullet_direction * BULLET_BALL_VELOCITY

            # Explosion for ball, smaller radius than paddle explosion
            explosion_position = (ball.centerx, ball.centery)
            explosion_radius = 10
            explosion_active = True

            computer_bullets.remove(computer_bullet)

    for bullet in bullets:
        if opponent_paddle.colliderect(bullet):
            # Create explosion
            explosion_position = (opponent_paddle.centerx, opponent_paddle.centery)
            explosion_radius = 10
            explosion_active = True

            opponent_paddle_height -= 5  # Shorten height by 5
            opponent_paddle_height = max(75, opponent_paddle_height)  # Minimum height 75% of original, 75/100
            opponent_paddle_color = HIT  # Change paddle color
            if opponent_paddle_height == 75:
                opponent_paddle_color = LOW  # Change to dark red when smallest size
            opponent_paddle = pygame.Rect(opponent_paddle.x, opponent_paddle.y, opponent_paddle_width,
                                          opponent_paddle_height)

            bullets.remove(bullet)

    for computer_bullet in computer_bullets:
        if player_paddle.colliderect(computer_bullet):
            # Create explosion
            explosion_position = (player_paddle.centerx, player_paddle.centery)
            explosion_radius = 15
            explosion_active = True
            player_paddle_height -= 5  # Shorten height by 5
            player_paddle_height = max(75, player_paddle_height)  # Minimum height 75% of original, 75/100
            player_paddle_color = HIT  # Change paddle color
            if player_paddle_height == 75:
                player_paddle_color = LOW  # Change to dark red when smallest size
            player_paddle = pygame.Rect(player_paddle.x, player_paddle.y, player_paddle_width, player_paddle_height)

            computer_bullets.remove(computer_bullet)

    for computer_bullet in computer_bullets:
        for bullet in bullets:
            if bullet.colliderect(computer_bullet):  # If player bullet hits computer bullet and vice versa
                explosion_position = (bullet.centerx, bullet.centery)
                explosion_radius = 5
                explosion_active = True

                bullets.remove(bullet)
                computer_bullets.remove(computer_bullet)

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw paddles and ball
    pygame.draw.rect(screen, player_paddle_color, player_paddle)
    pygame.draw.rect(screen, opponent_paddle_color, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, GREEN, bullet)

    for computer_bullet in computer_bullets:
        pygame.draw.rect(screen, GREEN, computer_bullet)

    # Draw explosion
    if explosion_active:
        pygame.draw.circle(screen, ORANGE, explosion_position, explosion_radius)
        explosion_radius += 1
        if explosion_radius > 20:
            explosion_active = False

    # Draw scoreboard
    player_text = font.render("Player: " + str(player_score), True, WHITE)
    opponent_text = font.render("Opponent: " + str(opponent_score), True, WHITE)
    screen.blit(player_text, (20, 20))
    screen.blit(opponent_text, (WIDTH - opponent_text.get_width() - 20, 20))

    pygame.display.flip()

    pygame.time.Clock().tick(60)