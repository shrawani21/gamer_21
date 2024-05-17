import pygame
import math

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
YELLOW=(255, 255, 0)
BLACK = (12, 12, 12)
CIRCLE_RADIUS = 2
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
            [(self.rect.left, self.rect.bottom), (self.rect.left, self.rect.top)]]
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
            pygame.draw.rect(surface, BLUE if self.winner == 'X' else RED, self.rect)
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
first_click = None
FONT_SIZE=24
win_p=""
cir_col = [[0 for _ in range(COLS+1)] for _ in range(ROWS+1)]
# Create the game grid
for r in range(ROWS):
    for c in range(COLS):
        cell = Cell(r, c)
        cells.append(cell)
font = pygame.font.Font(None, FONT_SIZE)
def are_adjacent(p1, p2):
    return (abs(p1[0] - p2[0]) == CELL_SIZE and p1[1] == p2[1]) or (abs(p1[1] - p2[1]) == CELL_SIZE and p1[0] == p2[0])

def handle_click(pos):
    r1=(pos[1]-(3 * PADDING))//CELL_SIZE 
    c1=(pos[0]-(2 * PADDING))//CELL_SIZE 
    global first_click, player, next_turn, p1_score, p2_score,turn,cir_col,cir_col,win_p
    cir_col[r1][c1]=1
    if first_click is None:
        first_click = pos
    else:
        if are_adjacent(first_click, pos):
            win_p=""
            # Find the corresponding cell and update the side
            for cell in cells:
                for index, edge in enumerate(cell.edges):
                    if (edge[0] == first_click and edge[1] == pos) or (edge[1] == first_click and edge[0] == pos):
                        if not cell.sides[index]:
                            cell.sides[index] = True
                            if cell.check_win(player):
                                if turn == 0:
                                    win_p="Its player 1's box!"
                                    p1_score += 1
                                else:
                                    win_p="Its player 2's box!"
                                    p2_score += 1
                                next_turn = False
                            else:
                                next_turn = True
                    else:
                        continue
        first_click = None
        cir_col = [[0 for _ in range(COLS+1)] for _ in range(ROWS+1)]
        if next_turn:
            turn = (turn + 1) % 2
            player = players[turn]
            next_turn = False
def is_within_circle(click_pos, circle_center, radius):
    dist = math.hypot(click_pos[0] - circle_center[0], click_pos[1] - circle_center[1])
    return dist <= radius

def render_text(text, pos, font, color=WHITE):
    text_surface = font.render(text, True, color)
    win.blit(text_surface, pos)
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for r in range(ROWS + 1):
                for c in range(COLS + 1):
                    circle_center = (c * CELL_SIZE + 2 * PADDING, r * CELL_SIZE + 3 * PADDING)
                    if is_within_circle(event.pos, circle_center, CIRCLE_RADIUS):
                        handle_click(circle_center)
                        break
    # Clear the screen
    win.fill(BLACK)
    render_text(f"{win_p} Player {turn+1}'s turn", (PADDING, PADDING), font)

    # Draw the grid lines
    for r in range(ROWS + 1):
        for c in range(COLS + 1):
            pygame.draw.circle(win, YELLOW if cir_col[r][c] else WHITE, (c * CELL_SIZE + 2 * PADDING, r * CELL_SIZE + 3 * PADDING), CIRCLE_RADIUS)
    # Update and draw each cell in the grid
    for cell in cells:
        cell.update(win)
    pygame.display.update()
pygame.quit()
