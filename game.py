import pygame
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Pygame!")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Clock for controlling FPS
clock = pygame.time.Clock()

# Player setup
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Keys for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Fill background
    screen.fill(WHITE)

    # Draw player (rectangle)
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))

    # Update display
    pygame.display.flip()

    # FPS
    clock.tick(60)
