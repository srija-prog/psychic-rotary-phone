import pygame
import sys
import random

#initialise pygame
pygame.init()

#screen size!
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Mama it's a snake!!!")

#colors
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)

#CLOCK FOR SPEED CONTROLL
clock = pygame.time.Clock()

#snake in making!
snake_block = 20
snake_speed = 10

#snake starting position
snake = [(100,50), (80,50),(60,50)]  #3 blocks long
snake_dir = "RIGHT"


def move_snake(snake, direction):
    x, y = snake[0]  # Head of snake
    if direction == "UP":       #the snake moves upward so y= y-snake block
        y -= snake_block
    elif direction == "DOWN":   #the snake moves downward so y+snake block
        y += snake_block
    elif direction == "LEFT":   #same thing as before , now just in the x axis
        x -= snake_block
    elif direction == "RIGHT":  #same thing!
        x += snake_block
    new_head = (x, y)
    snake.insert(0, new_head)  # Add new head
    snake.pop()  # Remove tail
    return snake

#food
food_x = random.randrange(0, WIDTH - snake_block, snake_block)
food_y = random.randrange(0, HEIGHT - snake_block, snake_block)
food = (food_x, food_y)            #creating a food item at random positions on the screen.
score = 0 


#main loop
running = True
while running:
    for event in pygame.event.get():    #if the player quits, then stop running.
        if event.type == pygame.QUIT:
            running = False

        # Control with arrow keys
        # here we have to prevent suicide cases, so if the snake is moving upwards then it can't go down all of a sudden!
        #same thing for right and left

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != "DOWN":
                snake_dir = "UP"
            elif event.key == pygame.K_DOWN and snake_dir != "UP":
                snake_dir = "DOWN"
            elif event.key == pygame.K_LEFT and snake_dir != "RIGHT":
                snake_dir = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_dir != "LEFT":
                snake_dir = "RIGHT"

    # Move snake
    snake = move_snake(snake, snake_dir)

    # to detect collisions
    head_x, head_y = snake[0]

    # Wall collision
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        running = False

    # Self collision
    if snake[0] in snake[1:]:
        running = False

# Snake got food!
    if snake[0] == food:  
        score += 1
        # Dont remove tail → Snake grows!
        snake.append(snake[-1])

        # New food location
        food_x = random.randrange(0, WIDTH - snake_block, snake_block)
        food_y = random.randrange(0, HEIGHT - snake_block, snake_block)
        food = (food_x, food_y)


    # Fill screen
    screen.fill(BLACK)

    # Draw snake
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], snake_block, snake_block))


    #draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], snake_block, snake_block))

    # Draw score
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))



    # Update screen
    pygame.display.flip()
    clock.tick(snake_speed)


# YOUR GAME IS OVER
font = pygame.font.SysFont("Arial", 36, bold=True)
game_over_text = font.render(f"SORRY! GAME OVER! Final Score: {score}", True, RED)
screen.blit(game_over_text, (WIDTH//2 - 200, HEIGHT//2 - 20))
pygame.display.flip()

pygame.time.wait(30000)  # Wait 30 seconds



pygame.quit()
sys.exit()
