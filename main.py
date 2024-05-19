import pygame

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
CELL_SIZE = 40
PADDING = 20
ROWS = COLS = (SCREEN_WIDTH - 4 * PADDING) // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
RED = (252, 91, 122)
BLUE = (78, 193, 246)
GREEN = (0, 255, 0)
BLACK = (12, 12, 12)
DARK_GRAY = (30, 30, 30)
LIGHT_GRAY = (100, 100, 100)

# Initialize Pygame
pygame.init()

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont('cursive', 25)

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.index = self.row * ROWS + self.col
        self.rect = pygame.Rect((self.col * CELL_SIZE + 2 * PADDING,
                                 self.row * CELL_SIZE + 3 * PADDING,
                                 CELL_SIZE, CELL_SIZE))
        self.edges = [
            [(self.rect.left, self.rect.top), (self.rect.right, self.rect.top)],
            [(self.rect.right, self.rect.top), (self.rect.right, self.rect.bottom)],
            [(self.rect.right, self.rect.bottom), (self.rect.left, self.rect.bottom)],
            [(self.rect.left, self.rect.bottom), (self.rect.left, self.rect.top)]
        ]

        self.sides = [False] * 4
        self.winner = None

    def check_win(self, winner):
        if not self.winner and all(self.sides):
            self.winner = winner
            self.color = GREEN if winner == 'X' else RED
            self.text = font.render(self.winner, True, WHITE)
            return 1
        return 0

    def update(self, win):
        if self.winner:
            pygame.draw.rect(win, self.color, self.rect)
            win.blit(self.text, (self.rect.centerx - 5, self.rect.centery - 7))

        for index, side in enumerate(self.sides):
            if side:
                pygame.draw.line(win, WHITE, self.edges[index][0], self.edges[index][1], 2)

def create_cells():
    cells = []
    for r in range(ROWS):
        for c in range(COLS):
            cell = Cell(r, c)
            cells.append(cell)
    return cells

def reset_cells():
    return None, None, False, False, False, False

def reset_score():
    return 0, 0, 0

def reset_player():
    return 0, ['X', 'O'], 'X', False

# Game variables initialization
game_over = False
cells = create_cells()
pos, current_cell, up, right, bottom, left = reset_cells()
fill_count, p1_score, p2_score = reset_score()
turn, players, current_player, next_turn = reset_player()

# Main game loop
running = True
while running:

    win.fill(DARK_GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                game_over = False
                cells = create_cells()
                pos, current_cell, up, right, bottom, left = reset_cells()
                fill_count, p1_score, p2_score = reset_score()
                turn, players, current_player, next_turn = reset_player()

    # Drawing grid
    for r in range(ROWS + 1):
        for c in range(COLS + 1):
            pygame.draw.circle(win, WHITE, (c * CELL_SIZE + 2 * PADDING, r * CELL_SIZE + 3 * PADDING), 2)

    # Update and draw cells
    for cell in cells:
        cell.update(win)
        if pos and cell.rect.collidepoint(pos):
            current_cell = cell

    # Determine which cell was clicked and fill all sides if not already filled
    if current_cell and pos:
        index = current_cell.index
        if not current_cell.winner:
            sides_filled = 0
            for i in range(4):
                if not current_cell.sides[i]:
                    current_cell.sides[i] = True
                    sides_filled += 1
                    if i == 0 and index - ROWS >= 0:
                        cells[index - ROWS].sides[2] = True
                    elif i == 1 and (index + 1) % COLS > 0:
                        cells[index + 1].sides[3] = True
                    elif i == 2 and index + ROWS < len(cells):
                        cells[index + ROWS].sides[0] = True
                    elif i == 3 and (index % COLS) > 0:
                        cells[index - 1].sides[1] = True

            # Check for win condition
            res = current_cell.check_win(current_player)
            if res:
                fill_count += res
                if current_player == 'X':
                    p1_score += 1
                else:
                    p2_score += 1
                if fill_count == ROWS * COLS:
                    game_over = True

            # Always switch players after a mouse click
            turn = (turn + 1) % len(players)
            current_player = players[turn]

    # Display scores and current player
    p1_img = font.render(f'{p1_score}', True, BLUE)
    p2_img = font.render(f'{p2_score}', True, BLUE)

    # Render player texts with appropriate positions    
    p1_text = font.render('Player 1:', True, BLUE)
    p2_text = font.render('Player 2:', True, BLUE)

    # Calculate positions for player texts and scores
    p1_text_pos = (2 * PADDING, 15)
    p1_img_pos = (p1_text_pos[0] + p1_text.get_width() + 5, 15)
    p2_img_pos = (SCREEN_WIDTH - 2 * PADDING - p2_img.get_width(), 15)
    p2_text_pos = (p2_img_pos[0] - p2_text.get_width() - 5, 15)

    # Blit the player texts and scores
    win.blit(p1_text, p1_text_pos)
    win.blit(p1_img, p1_img_pos)
    win.blit(p2_text, p2_text_pos)
    win.blit(p2_img, p2_img_pos)

    # Highlight current player's turn
    if not game_over:
        if turn == 0:  # Player 1's turn
            pygame.draw.rect(win, BLUE, (p1_text_pos[0], p1_text_pos[1] + font.get_height() + 2, p1_text.get_width() + p1_img.get_width() + 5, 2), 0)
        else:  # Player 2's turn
            pygame.draw.rect(win, BLUE, (p2_text_pos[0], p2_text_pos[1] + font.get_height() + 2, p2_text.get_width() + p2_img.get_width() + 5, 2), 0)

    if game_over:
        # Display game over message
        over_img = font.render('Game Over', True, WHITE)
        winner_img = font.render(f'Player {1 if p1_score > p2_score else 2} Won', True, WHITE)
        msg_img = font.render('Press R to restart, Q or ESC to quit', True, RED)
        win.blit(over_img, ((SCREEN_WIDTH - over_img.get_width()) / 2, 100))
        win.blit(winner_img, ((SCREEN_WIDTH - winner_img.get_width()) / 2, 150))
        win.blit(msg_img, ((SCREEN_WIDTH - msg_img.get_width()) / 2, 200))

    # Draw border
    pygame.draw.rect(win, LIGHT_GRAY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 2, border_radius=10)

    pygame.display.update()

pygame.quit()
