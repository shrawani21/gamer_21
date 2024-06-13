import pygame

# Constants defining various properties of the game window and cells
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 300, 350  # Increased height to accommodate buttons
CELL_SIZE = 40
PADDING = 20
ROWS = COLS = (SCREEN_WIDTH - 4 * PADDING) // CELL_SIZE

# Initialize pygame
pygame.init()
win = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Dot and Line")
font = pygame.font.SysFont('cursive', 25)

WHITE = (255, 255, 255)
RED = (252, 91, 122)
BLUE = (78, 193, 246)
BLACK = (12, 12, 12)
GREEN = (0, 255, 0)

# Define button dimensions and colors
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 40
BUTTON_PADDING = 10
BUTTON_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = WHITE

# Define the Cell class to represent each cell in the grid
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
                return 1
        return 0

    def update(self, surface):
        if self.winner:
            pygame.draw.rect(surface, GREEN if self.winner == 'X' else RED, self.rect)
        for index, side in enumerate(self.sides):
            if side:
                pygame.draw.line(surface, WHITE, self.edges[index][0], self.edges[index][1], 2)

def draw_game():
    win.fill(BLACK)
    for r in range(ROWS + 1):
        for c in range(COLS + 1):
            pygame.draw.circle(win, WHITE, (c * CELL_SIZE + 2 * PADDING, r * CELL_SIZE + 3 * PADDING), 2)
    for cell in cells:
        cell.update(win)

def draw_buttons(p1_score, p2_score):
    p1_button_rect = pygame.Rect(PADDING, SCREEN_HEIGHT - BUTTON_HEIGHT - BUTTON_PADDING, BUTTON_WIDTH, BUTTON_HEIGHT)
    p2_button_rect = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - PADDING, SCREEN_HEIGHT - BUTTON_HEIGHT - BUTTON_PADDING, BUTTON_WIDTH, BUTTON_HEIGHT)

    pygame.draw.rect(win, BUTTON_COLOR, p1_button_rect)
    pygame.draw.rect(win, BUTTON_COLOR, p2_button_rect)

    p1_text = font.render(f'Player 1: {p1_score}', True, BUTTON_TEXT_COLOR)
    p2_text = font.render(f'Player 2: {p2_score}', True, BUTTON_TEXT_COLOR)

    win.blit(p1_text, (p1_button_rect.centerx - p1_text.get_width() // 2, p1_button_rect.centery - p1_text.get_height() // 2))
    win.blit(p2_text, (p2_button_rect.centerx - p2_text.get_width() // 2, p2_button_rect.centery - p2_text.get_height() // 2))

# Initialize game variables
cells = []
game_over = False
turn = 0
players = ['X', 'O']
player = players[turn]
next_turn = False
fill_count = 0
p1_score = 0
p2_score = 0
ccell = None
up = right = bottom = left = False

# Create the game grid
for r in range(ROWS):
    for c in range(COLS):
        cell = Cell(r, c)
        cells.append(cell)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            for cell in cells:
                if cell.rect.collidepoint(x, y):
                    for i, edge in enumerate(cell.edges):
                        if not cell.sides[i] and pygame.Rect(edge[0], (edge[1][0] - edge[0][0], edge[1][1] - edge[0][1])).inflate(5, 5).collidepoint(x, y):
                            cell.sides[i] = True
                            if cell.check_win(player):
                                if player == 'X':
                                    p1_score += 1
                                else:
                                    p2_score += 1
                            else:
                                turn = (turn + 1) % 2
                                player = players[turn]
                            break

    draw_game()
    draw_buttons(p1_score, p2_score)
    pygame.display.update()

pygame.quit()
