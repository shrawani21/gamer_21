import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)  # Changed color to green
# Game variables
GRID_SIZE = 3
DOT_RADIUS = 5
MARGIN = 50
CELL_SIZE = (WIDTH - 2 * MARGIN) // GRID_SIZE

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dots and Boxes")

# Fonts
font = pygame.font.SysFont(None, 36)

# Game state
grid = [[{'top': False, 'right': False, 'bottom': False, 'left': False, 'owner': None} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
turn = 'X'
score = {'X': 0, 'O': 0}
game_over = False
is_single_player = True

def draw_grid():
    screen.fill(WHITE)
    for i in range(GRID_SIZE + 1):
        for j in range(GRID_SIZE + 1):
            pygame.draw.circle(screen, BLACK, (MARGIN + j * CELL_SIZE, MARGIN + i * CELL_SIZE), DOT_RADIUS)
    
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell = grid[i][j]
            x, y = MARGIN + j * CELL_SIZE, MARGIN + i * CELL_SIZE
            if cell['top']:
                pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)
            if cell['right']:
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
            if cell['bottom']:
                pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
            if cell['left']:
                pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE), 2)
            if cell['owner']:
                color = BLUE if cell['owner'] == 'X' else GREEN  # Changed color to green
                pygame.draw.rect(screen, color, (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))

    score_text = font.render(f"X: {score['X']}  O: {score['O']}", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    if game_over:
        game_over_text = font.render("Game Over", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

    pygame.display.flip()

def check_game_over():
    return all(all(cell['owner'] is not None for cell in row) for row in grid)

def get_available_moves():
    moves = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if not grid[i][j]['top']:
                moves.append((i, j, 'top'))
            if not grid[i][j]['right']:
                moves.append((i, j, 'right'))
            if not grid[i][j]['bottom']:
                moves.append((i, j, 'bottom'))
            if not grid[i][j]['left']:
                moves.append((i, j, 'left'))
    return moves

def ai_make_move():
    available_moves = get_available_moves()
    if available_moves:
        i, j, side = random.choice(available_moves)
        make_move(i, j, side, 'O')

def make_move(i, j, side, player):
    global turn, score, game_over

    if side == 'top' and not grid[i][j]['top']:
        grid[i][j]['top'] = True
    elif side == 'right' and not grid[i][j]['right']:
        grid[i][j]['right'] = True
    elif side == 'bottom' and not grid[i][j]['bottom']:
        grid[i][j]['bottom'] = True
    elif side == 'left' and not grid[i][j]['left']:
        grid[i][j]['left'] = True
    else:
        return

    completed_box = False

    if side == 'top' and i > 0 and all(grid[i-1][j][s] for s in ['top', 'right', 'bottom', 'left']):
        grid[i-1][j]['owner'] = player
        score[player] += 1
        completed_box = True
    if side == 'right' and j < GRID_SIZE - 1 and all(grid[i][j+1][s] for s in ['top', 'right', 'bottom', 'left']):
        grid[i][j+1]['owner'] = player
        score[player] += 1
        completed_box = True
    if side == 'bottom' and i < GRID_SIZE - 1 and all(grid[i+1][j][s] for s in ['top', 'right', 'bottom', 'left']):
        grid[i+1][j]['owner'] = player
        score[player] += 1
        completed_box = True
    if side == 'left' and j > 0 and all(grid[i][j-1][s] for s in ['top', 'right', 'bottom', 'left']):
        grid[i][j-1]['owner'] = player
        score[player] += 1
        completed_box = True

    if all(grid[i][j][s] for s in ['top', 'right', 'bottom', 'left']):
        grid[i][j]['owner'] = player
        score[player] += 1
        completed_box = True

    if not completed_box:
        turn = 'O' if turn == 'X' else 'X'

    if check_game_over():
        game_over = True

def handle_mouse_click(pos):
    x, y = pos
    if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
        col = (x - MARGIN) // CELL_SIZE
        row = (y - MARGIN) // CELL_SIZE
        rel_x = (x - MARGIN) % CELL_SIZE
        rel_y = (y - MARGIN) % CELL_SIZE

        if rel_y < DOT_RADIUS * 2:
            make_move(row, col, 'top', turn)
        elif rel_y > CELL_SIZE - DOT_RADIUS * 2:
            make_move(row, col, 'bottom', turn)
        elif rel_x < DOT_RADIUS * 2:
            make_move(row, col, 'left', turn)
        elif rel_x > CELL_SIZE - DOT_RADIUS * 2:
            make_move(row, col, 'right', turn)

def main():
    global turn, game_over

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                handle_mouse_click(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    restart_game()
                elif event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()

        if not game_over and turn == 'O' and is_single_player:
            ai_make_move()

        draw_grid()
        clock.tick(30)

def restart_game():
    global grid, turn, score, game_over
    grid = [[{'top': False, 'right': False, 'bottom': False, 'left': False, 'owner': None} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    turn = 'X'
    score = {'X': 0, 'O': 0}
    game_over = False

if __name__ == "__main__":
    main()

