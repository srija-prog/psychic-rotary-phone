import pygame,sys, math

#initia pygame
pygame.init()


#screen setup!
CELL_SIZE = 150
GRID_SIZE = 3
WIDTH, HEIGHT = CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

#colors
PINK_LIGHT = (255, 182, 193)   # light pink
PINK_DARK = (255, 105, 180)    # darker pink
LINE_COLOR = (200, 50, 120)
CIRCLE_COLOR = (239, 231, 200)
X_COLOR = (84, 84, 84)

#board setup
board = [["" for _ in range(3)] for _ in range(3)]
human = 'X'
ai = 'O'
current_player = human
game_over = False
winner_line = None

#drawing functions
def draw_background():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            base_color = PINK_LIGHT if (row + col) % 2 == 0 else PINK_DARK
            # Draw base color
            pygame.draw.rect(SCREEN, base_color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            # Gradient overlay: blend base color to a darker version vertically
            dark_color = tuple(max(0, c - 40) for c in base_color)
            for y in range(CELL_SIZE):
                ratio = y / CELL_SIZE
                r = int(base_color[0] * (1 - ratio) + dark_color[0] * ratio)
                g = int(base_color[1] * (1 - ratio) + dark_color[1] * ratio)
                b = int(base_color[2] * (1 - ratio) + dark_color[2] * ratio)
                pygame.draw.line(
                    SCREEN,
                    (r, g, b),
                    (col * CELL_SIZE, row * CELL_SIZE + y),
                    (col * CELL_SIZE + CELL_SIZE - 1, row * CELL_SIZE + y)
                )

def draw_grid_lines():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(SCREEN, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 5)
        pygame.draw.line(SCREEN, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 5)

def draw_marks():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 'O':
                pygame.draw.circle(SCREEN, CIRCLE_COLOR, (col * CELL_SIZE + CELL_SIZE//2, row * CELL_SIZE + CELL_SIZE//2), CELL_SIZE//2 - 10, 15)
            elif board[row][col] == 'X':
                pygame.draw.line(SCREEN, X_COLOR, (col * CELL_SIZE + 30, row * CELL_SIZE + 30), (col * CELL_SIZE + CELL_SIZE - 30, row * CELL_SIZE + CELL_SIZE - 30), 15)
                pygame.draw.line(SCREEN, X_COLOR, (col * CELL_SIZE + CELL_SIZE - 30, row * CELL_SIZE + 30), (col * CELL_SIZE + 30, row * CELL_SIZE + CELL_SIZE - 30), 15)


#game logic functions
def check_winner():
    global winner_line
    # Check rows and columns
    for i in range(GRID_SIZE):
        if board[i][0] == board[i][1] == board[i][2] != "":
            winner_line = ('row', i)
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            winner_line = ('col', i)
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "":
        winner_line = ('diag1', None)
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        winner_line = ('diag2', None)
        return board[0][2]
    # Check for tie
    if all(board[row][col] != "" for row in range(3) for col in range(3)):
        return "Tie"
    return None
        # (already checked above)


def draw_winner_line():
    if not winner_line:
        return
    kind, i = winner_line
    sparkle_color = (255, 215, 0)  # gold
    sparkle_radius = 10
    sparkle_count = 12
    if kind == 'row':
        y = i * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.line(SCREEN, (255,0,0), (20, y), (WIDTH - 20, y), 8)
        # Add sparkles along the row
        for s in range(sparkle_count):
            x = 20 + s * (WIDTH - 40) // (sparkle_count - 1)
            pygame.draw.circle(SCREEN, sparkle_color, (x, y), sparkle_radius)
    elif kind == 'col':
        x = i * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.line(SCREEN, (255,0,0), (x, 20), (x, HEIGHT - 20), 8)
        # Add sparkles along the column
        for s in range(sparkle_count):
            y = 20 + s * (HEIGHT - 40) // (sparkle_count - 1)
            pygame.draw.circle(SCREEN, sparkle_color, (x, y), sparkle_radius)
    elif kind == 'diag1':
        pygame.draw.line(SCREEN, (255,0,0), (20, 20), (WIDTH - 20, HEIGHT - 20), 8)
        # Add sparkles along the diagonal
        for s in range(sparkle_count):
            x = 20 + s * (WIDTH - 40) // (sparkle_count - 1)
            y = 20 + s * (HEIGHT - 40) // (sparkle_count - 1)
            pygame.draw.circle(SCREEN, sparkle_color, (x, y), sparkle_radius)
    elif kind == 'diag2':
        pygame.draw.line(SCREEN, (255,0,0), (WIDTH - 20, 20), (20, HEIGHT - 20), 8)
        # Add sparkles along the anti-diagonal
        for s in range(sparkle_count):
            x = WIDTH - 20 - s * (WIDTH - 40) // (sparkle_count - 1)
            y = 20 + s * (HEIGHT - 40) // (sparkle_count - 1)
            pygame.draw.circle(SCREEN, sparkle_color, (x, y), sparkle_radius)
        if kind == 'row':
            y = i * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.line(SCREEN, (255,0,0), (20, y), (WIDTH - 20, y), 8)
        elif kind == 'col':
            x = i * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.line(SCREEN, (255,0,0), (x, 20), (x, HEIGHT - 20), 8)
        elif kind == 'diag1':
            pygame.draw.line(SCREEN, (255,0,0), (20, 20), (WIDTH - 20, HEIGHT - 20), 8)
        elif kind == 'diag2':
            pygame.draw.line(SCREEN, (255,0,0), (WIDTH - 20, 20), (20, HEIGHT - 20), 8)
    


def show_game_over(winner):
    font = pygame.font.SysFont("arial", 36, bold=True)
    if winner == "Tie":
        text = font.render("It's a Tie!", True, (0,0,0))
    else:
        text = font.render(f"{winner} Wins!", True, (0,0,0))
    SCREEN.blit(text, (75,130))


def restart_game():
    global board, current_player, game_over, winner_line
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = human
    game_over = False
    winner_line = None

#AI logic;

def minimax(is_maximizing):
    winner = check_winner()
    if winner == ai:
        return 1
    elif winner == human:
        return -1
    elif winner == "Tie":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = ai
                    score = minimax(False)
                    board[row][col] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = human
                    score = minimax(True)
                    board[row][col] = ""
                    best_score = min(score, best_score)
        return best_score


def ai_move():
    best_score = -math.inf
    move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = ai
                score = minimax(False)
                board[row][col] = ""
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move:
        board[move[0]][move[1]] = ai

#main loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            # Check for restart button click
            button_width, button_height = 200, 50
            button_x = WIDTH // 2 - button_width // 2
            button_y = HEIGHT - button_height - 20
            restart_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            if restart_button_rect.collidepoint(mouseX, mouseY):
                restart_game()
                winner = None
                game_over = False
            elif not game_over:
                clicked_row = mouseY // CELL_SIZE
                clicked_col = mouseX // CELL_SIZE
                if 0 <= clicked_row < GRID_SIZE and 0 <= clicked_col < GRID_SIZE:
                    if board[clicked_row][clicked_col] == "":
                        board[clicked_row][clicked_col] = current_player
                        winner = check_winner()
                        if winner:
                            game_over = True
                        else:
                            current_player = ai
                            ai_move()
                            winner = check_winner()
                            if winner:
                                game_over = True
                            else:
                                current_player = human
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                winner = None
                game_over = False

    winner = check_winner()
    if winner and not game_over:
        game_over = True

    if not game_over and current_player==ai:
        ai_move()
        current_player = human

    #redraw everything
    SCREEN.fill((255,255,255))
    draw_background()
    draw_grid_lines()
    draw_marks()

    # Show winner line and message if someone wins
    if winner and winner != "Tie":
        draw_winner_line()
        show_game_over(winner)

    # Show tie message in a red gradient box if game is a tie
    if winner == "Tie":
        font_tie = pygame.font.SysFont("arial", 48, bold=True)
        tie_text = font_tie.render("Tie", True, (255, 255, 255))
        box_width, box_height = tie_text.get_width() + 40, tie_text.get_height() + 40
        box_x = WIDTH // 2 - box_width // 2
        box_y = HEIGHT // 2 - box_height // 2
        # Gradient from light red to dark red
        light_red = (255, 100, 100)
        dark_red = (180, 0, 0)
        for y in range(box_height):
            ratio = y / box_height
            r = int(light_red[0] * (1 - ratio) + dark_red[0] * ratio)
            g = int(light_red[1] * (1 - ratio) + dark_red[1] * ratio)
            b = int(light_red[2] * (1 - ratio) + dark_red[2] * ratio)
            pygame.draw.rect(
                SCREEN,
                (r, g, b),
                (box_x, box_y + y, box_width, 1),
                border_radius=0
            )
        # Draw rounded border on top
        pygame.draw.rect(SCREEN, (180, 0, 0), (box_x, box_y, box_width, box_height), 4, border_radius=16)
        SCREEN.blit(tie_text, (WIDTH // 2 - tie_text.get_width() // 2, HEIGHT // 2 - tie_text.get_height() // 2))

    # Draw restart button at the bottom
    button_width, button_height = 200, 50
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT - button_height - 20
    restart_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    PURPLE = (128, 0, 128)
    pygame.draw.rect(SCREEN, PURPLE, restart_button_rect, border_radius=12)
    font_btn = pygame.font.SysFont("arial", 32, bold=True)
    restart_text = font_btn.render("Restart", True, (255, 255, 255))
    SCREEN.blit(restart_text, (button_x + button_width // 2 - restart_text.get_width() // 2, button_y + button_height // 2 - restart_text.get_height() // 2))

    pygame.display.update()

    # Handle restart button click in main event loop

pygame.quit()
sys.exit()
