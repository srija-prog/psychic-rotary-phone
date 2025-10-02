import pygame
import random
from collections import deque
import os

#initialising the game
pygame.init()

#screen dimensions
WIDTH, HEIGHT = 800,600
CELL_SIZE = 40
ROWS, COLS = HEIGHT//CELL_SIZE,WIDTH//CELL_SIZE
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("maze runner sprites")


#variables for the game
player_pos = [0, 0]
player_pixel = [0,0]
enemy_pos = [ROWS-1,COLS-1]
enemy_pixel = [enemy_pos[1]*CELL_SIZE, enemy_pos[0]*CELL_SIZE]
PLAYER_SPEED = 8
ENEMY_SPEED = 4
score = 0
treasures = [(random.randint(0, ROWS-1), random.randint(0, COLS-1)) for _ in range(20)]  # Increased to 20 treasures
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


#maze with more vertical walls, no big center block
maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
# Add vertical walls in columns format (less frequent)
for col in range(3, COLS, 6):  # every 6th column starting from 3
    for row in range(3, ROWS-3):
        maze[row][col] = 1
# Add horizontal walls in rows format (less frequent)
for row in range(6, ROWS, 8):  # every 8th row starting from 6
    for col in range(2, COLS-2):
        maze[row][col] = 1

def load_sprites(folder, count):
    images = []
    script_dir = os.path.dirname(__file__)
    for i in range(1, count+1):
        full_path = os.path.join(script_dir, folder, f"{i}.png")
        img = pygame.image.load(full_path).convert_alpha()  # preserve transparency
        img = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
        images.append(img)
    return images

player_sprites = load_sprites("player", 1)     # folder "player" with 1.png, 2.png
enemy_sprites = load_sprites("enemy", 2)       # folder "enemy" with 1.png, 2.png
treasure_sprites = load_sprites("treasure", 1) # folder "treasure" with 1.png, 2.png

BACKGROUND_COLOR = (0, 0, 0)  # Black
# Animation frames
player_frame = 0
enemy_frame = 0
treasure_frame = 0
ANIMATION_SPEED = 10
frame_count = 0

# BFS Pathfinding for enemy
def bfs(start, goal, maze):
    queue = deque([start])
    visited = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        r, c = current
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] == 0 and (nr,nc) not in visited:
                visited[(nr,nc)] = current
                queue.append((nr,nc))
    path = []
    current = goal
    while current != start:
        if current not in visited:
            return []
        path.append(current)
        current = visited[current]
    path.reverse()
    return path

def pixel_to_grid(pixel_pos):
    return [pixel_pos[1]//CELL_SIZE, pixel_pos[0]//CELL_SIZE]

# Game loop
running = True
while running:
    dt = clock.tick(60)
    frame_count += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    r, c = pixel_to_grid(player_pixel)
    if keys[pygame.K_LEFT] and c > 0 and maze[r][c-1] == 0:
        player_pixel[0] -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and c < COLS-1 and maze[r][c+1] == 0:
        player_pixel[0] += PLAYER_SPEED
    if keys[pygame.K_UP] and r > 0 and maze[r-1][c] == 0:
        player_pixel[1] -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and r < ROWS-1 and maze[r+1][c] == 0:
        player_pixel[1] += PLAYER_SPEED

    player_pos = pixel_to_grid(player_pixel)

    # Treasure collection
    if tuple(player_pos) in treasures:
        treasures.remove(tuple(player_pos))
        score += 1

    # Enemy AI (BFS chase)
    path = bfs(tuple(enemy_pos), tuple(player_pos), maze)
    if path:
        next_cell = path[0]
        target_x = next_cell[1]*CELL_SIZE
        target_y = next_cell[0]*CELL_SIZE
        if enemy_pixel[0] < target_x:
            enemy_pixel[0] += ENEMY_SPEED
        elif enemy_pixel[0] > target_x:
            enemy_pixel[0] -= ENEMY_SPEED
        if enemy_pixel[1] < target_y:
            enemy_pixel[1] += ENEMY_SPEED
        elif enemy_pixel[1] > target_y:
            enemy_pixel[1] -= ENEMY_SPEED
        if abs(enemy_pixel[0]-target_x) < ENEMY_SPEED and abs(enemy_pixel[1]-target_y) < ENEMY_SPEED:
            enemy_pos = list(next_cell)

    # Collision
    if player_pos == enemy_pos:
        print("Caught by enemy! Final Score:", score)
        # Show final score on screen for 2 seconds before closing
        screen.fill((0, 0, 0))
        final_text = font.render(f"Caught! Final Score: {score}", True, (255, 0, 0))
        screen.blit(final_text, (WIDTH//2 - final_text.get_width()//2, HEIGHT//2 - final_text.get_height()//2))
        pygame.display.flip()
        pygame.time.delay(2000)  # 2 seconds
        running = False

    # Update animation frames
    if frame_count % ANIMATION_SPEED == 0:
        player_frame = (player_frame + 1) % len(player_sprites)
        enemy_frame = (enemy_frame + 1) % len(enemy_sprites)
        treasure_frame = (treasure_frame + 1) % len(treasure_sprites)

    # Draw maze
    screen.fill(BACKGROUND_COLOR)
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == 1:
                pygame.draw.rect(screen, (139, 69, 19), (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Brown

    # Draw treasures
    for t in treasures:
        screen.blit(treasure_sprites[treasure_frame], (t[1]*CELL_SIZE, t[0]*CELL_SIZE))

    # Draw player and enemy
    screen.blit(player_sprites[player_frame], (player_pixel[0], player_pixel[1]))
    screen.blit(enemy_sprites[enemy_frame], (enemy_pixel[0], enemy_pixel[1]))

    # Draw scoreboard with brown gradient
    gradient_rect = pygame.Rect(0, 0, 180, 50)
    for i in range(gradient_rect.height):
        # Gradient from light brown to dark brown
        r = 205 - int(i * (205-139)/gradient_rect.height)
        g = 133 - int(i * (133-69)/gradient_rect.height)
        b = 63 - int(i * (63-19)/gradient_rect.height)
        pygame.draw.rect(screen, (r, g, b), (gradient_rect.x, gradient_rect.y + i, gradient_rect.width, 1))
    # Score text in dark brown
    score_text = font.render(f"Score: {score}", True, (101, 67, 33))
    screen.blit(score_text, (20, 10))

    pygame.display.flip()

pygame.quit()
