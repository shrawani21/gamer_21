import pygame

# Constants defining various properties of the game window and cells
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
CELL_SIZE = 40
PADDING = 20
ROWS = COLS = (SCREEN_WIDTH - 4 * PADDING) // CELL_SIZE

# Initialize pygame
pygame.init()
win = pygame.display.set_mode(SCREEN_SIZE)
font = pygame.font.SysFont('cursive', 25)

WHITE = (255, 255, 255)
RED = (252, 91, 122)
BLUE = (78, 193, 246)
BLACK = (12, 12, 12)

# Define the Cell class to represent each cell in the grid
class Cell:
    def __init__(self, row, col):
        """
        Initialize a cell with its row and column coordinates.
        """
        self.row = row
        self.col = col
        self.index = self.row * ROWS + self.col
        # Create a rectangle representing the cell's area on the game window
        self.rect = pygame.Rect((self.col * CELL_SIZE + 2 * PADDING,
                                 self.row * CELL_SIZE + 3 * PADDING,
                                 CELL_SIZE, CELL_SIZE))
        # Define the edges of the cell for drawing lines around it
        self.edges = [
            [(self.rect.left, self.rect.top), (self.rect.right, self.rect.top)],
            [(self.rect.right, self.rect.top), (self.rect.right, self.rect.bottom)],
            [(self.rect.right, self.rect.bottom), (self.rect.left, self.rect.bottom)],
            [(self.rect.left, self.rect.bottom), (self.rect.left, self.rect.top)]
        ]
        self.sides = [False, False, False, False]  # Tracks whether each side of the cell is filled
        self.winner = None  # Stores the winner of the cell (if any)

    def check_win(self, winner):
        """
        Check if a player has won by filling all four sides of the cell.
        """
        if not self.winner:
            if self.sides == [True]*4:
                self.winner = winner
                return 1  # Indicate that the cell has been won
        return 0  # Indicate that the cell has not been won

    def update(self, surface):
        """
        Update the visual representation of the cell on the game window.
        """
        if self.winner:
            # Draw the cell with the winning player's color
            pygame.draw.rect(surface, GREEN if self.winner == 'X' else RED, self.rect)
        for index, side in enumerate(self.sides):
            if side:
                # Draw filled sides of the cell
                pygame.draw.line(surface, WHITE, self.edges[index][0], self.edges[index][1], 2)

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

    # Clear the screen
    win.fill(BLACK)

    # Draw the grid lines
    for r in range(ROWS + 1):
        for c in range(COLS + 1):
            pygame.draw.circle(win, WHITE, (c * CELL_SIZE + 2 * PADDING, r * CELL_SIZE + 3 * PADDING), 2)

    # Update and draw each cell in the grid
    for cell in cells:
        cell.update(win)

    pygame.display.update()

pygame.quit()
