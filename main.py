import pygame

# Constants
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
CELL_SIZE = 40
PADDING = 20
ROWS = COLS = (SCREEN_WIDTH - 4 * PADDING) // CELL_SIZE
WHITE = (255, 255, 255)
RED = (252, 91, 122)
BLUE = (78, 193, 246)
GREEN = (0, 255, 0)
BLACK = (12, 12, 12)

# Initialize pygame
pygame.init()
win = pygame.display.set_mode(SCREEN_SIZE, pygame.NOFRAME)
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
        self.sides = [False, False, False, False]
        self.winner = None

    def check_win(self, winner):
        if not self.winner:
            if self.sides == [True] * 4:
                self.winner = winner
                self.color = GREEN if winner == 'X' else RED
                self.text = font.render(self.winner, True, WHITE)
                return 1
        return 0

    def update(self, surface):
        if self.winner:
            pygame.draw.rect(surface, self.color, self.rect)
            surface.blit(self.text, (self.rect.centerx - 5, self.rect.centery - 7))

        for index, side in enumerate(self.sides):
            if side:
                pygame.draw.line(surface, WHITE, self.edges[index][0], self.edges[index][1], 2)

ccell = None
def create_cells():
    cells = []
    for row in range(ROWS):
        for col in range(COLS):
            cell = Cell(row, col)
            cells.append(cell)
    return cells


cells = []  # initialize cells as a global variable

def reset_game_state():
    global cells, game_over, turn, players, player, next_turn, fill_count, p1_score, p2_score
    cells = create_cells()  # initialize cells
    game_over = False
    turn = 0
    players = ['X', 'O']
    player = players[turn]
    next_turn = False
    fill_count = 0
    p1_score = 0
    p2_score = 0

def handle_input_events():
    global game_over, next_turn, ccell
    up = right = bottom = left = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                return False

            if event.key == pygame.K_r:
                reset_game_state()

            if not game_over:
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_DOWN:
                    bottom = True
                if event.key == pygame.K_LEFT:
                    left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up = False
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_DOWN:
                bottom = False
            if event.key == pygame.K_LEFT:
                left = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                mouse_pos = pygame.mouse.get_pos()
                for cell in cells:
                    if cell.rect.collidepoint(mouse_pos):
                        ccell = cell
                        break
        # Minimize the window
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            pygame.display.iconify()
    return up, right, bottom, left


def update_game_state(up, right, bottom, left):
    global next_turn, fill_count, p1_score, p2_score, ccell, player, turn
    if ccell:
        index = ccell.index
        if not ccell.winner:
            pygame.draw.circle(win, RED, (ccell.rect.centerx, ccell.rect.centery), 2)

        if up and not ccell.sides[0]:
            ccell.sides[0] = True
            if index - ROWS >= 0:
                cells[index - ROWS].sides[2] = True
                next_turn = True

        if right and not ccell.sides[1]:
            ccell.sides[1] = True
            if (index + 1) % COLS > 0:
                cells[index + 1].sides[3] = True
                next_turn = True

        if bottom and not ccell.sides[2]:
            ccell.sides[2] = True
            if index + ROWS < len(cells):
                cells[index + ROWS].sides[0] = True
                next_turn = True

        if left and not ccell.sides[3]:
            ccell.sides[3] = True
            if (index % COLS) > 0:
                cells[index - 1].sides[1] = True
                next_turn = True

        res = ccell.check_win(player)
        if res:
            fill_count += res
            if player == 'X':
                p1_score += 1
            else:
                p2_score += 1
            if fill_count == ROWS * COLS:
                print(p1_score, p2_score)
                game_over = True

        if next_turn:
            turn = (turn + 1) % len(players)
            player = players[turn]
            next_turn = False

def draw_game():
    global cells, ccell  # access cells and ccell as global variables
    win.fill(BLACK)
    pygame.draw.rect(win, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 2, border_radius=10)

    for r in range(ROWS + 1):
        for c in range(COLS + 1):
            pygame.draw.circle(win, WHITE, (c * CELL_SIZE + 2 * PADDING,
                                             r * CELL_SIZE + 3 * PADDING), 2)

    for cell in cells:
        if cell == ccell:
            pygame.draw.rect(win, RED, cell.rect, 2)  # Draw a border around the selected cell
        cell.update(win)

    if game_over:
        rect = pygame.Rect((50, 100, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200))
        pygame.draw.rect(win, BLACK, rect)
        pygame.draw.rect(win, RED, rect, 2)

        over = font.render('Game Over', True, WHITE)
        win.blit(over, (rect.centerx - over.get_width() / 2, rect.y + 10))

        winner = '1' if p1_score > p2_score else '2'
        winner_img = font.render(f'Player {winner} Won', True, GREEN)
        win.blit(winner_img, (rect.centerx - winner_img.get_width() / 2, rect.centery - 10))

        msg = 'Press r:restart, q:'

reset_game_state()  # call reset_game_state() before draw_game()
draw_game()

running = True
while running:
    up, right, bottom, left = handle_input_events()

    # Update game state based on keyboard input
    update_game_state(up, right, bottom, left)

    # Draw the game
    draw_game()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
