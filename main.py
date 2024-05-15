import pygame  # Import the pygame library for game development

# Constants defining various properties of the game window and cells
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
win = pygame.display.set_mode(SCREEN_SIZE, pygame.NOFRAME)  # Set up the game window
font = pygame.font.SysFont('cursive', 25)  # Define a font for text rendering

# Global variables
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
            if self.sides == [True] * 4:
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


def create_cells():
    """
    Create a list of Cell objects to represent the game grid.
    """
    cells = []
    for row in range(ROWS):
        for col in range(COLS):
            cell = Cell(row, col)
            cells.append(cell)
    return cells


def reset_game_state():
    """
    Reset the game state to its initial conditions.
    """
    global cells, game_over, turn, players, player, next_turn, fill_count, p1_score, p2_score
    cells = create_cells()
    game_over = False
    turn = 0
    players = ['X', 'O']
    player = players[turn]
    next_turn = False
    fill_count = 0
    p1_score = 0
    p2_score = 0


def handle_input_events():
    """
    Handle user input events.
    """
    global game_over, next_turn
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

    return True


def update_game_state():
    """
    Update the game state based on user input.
    """
    global next_turn, fill_count, p1_score, p2_score
    if ccell:
        index = ccell.index
        if not ccell.winner:
            # Draw red circle on current cell if it's not won
            pygame.draw.circle(win, RED, (ccell.rect.centerx, ccell.rect.centery), 2)

        if up and not ccell.sides[0]:
            # If 'up' key is pressed and top side of cell is not drawn, draw it
            ccell.sides[0] = True
            if index - ROWS >= 0:
                cells[index - ROWS].sides[2] = True
                next_turn = True
        if right and not ccell.sides[1]:
            # Similar for 'right' key
            ccell.sides[1] = True
            if (index + 1) % COLS > 0:
                cells[index + 1].sides[3] = True
                next_turn = True
        if bottom and not ccell.sides[2]:
            # Similar for 'bottom' key
            ccell.sides[2] = True
            if index + ROWS < len(cells):
                cells[index + ROWS].sides[0] = True
                next_turn = True
        if left and not ccell.sides[3]:
            # Similar for 'left' key
            ccell.sides[3] = True
            if (index % COLS) > 0:
                cells[index - 1].sides[1] = True
                next_turn = True

        res = ccell.check_win(player)
        if res:
            # Check if current cell has been won
            fill_count += res
            if player == 'X':
                p1_score += 1
            else:
                p2_score += 1
            if fill_count == ROWS * COLS:
                # Check if all cells are filled
                print(p1_score, p2_score)
                game_over = True

        if next_turn:
            # Switch player turn if next_turn is True
            turn = (turn + 1) % len(players)
            player = players[turn]
            next_turn = False


def draw_game():
    """
    Draw the game window and its components.
    """
    win.fill(BLACK)  # Fill the game window with a black background
    pygame.draw.rect(win, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 2, border_radius=10)  # Draw the game border
    # Draw grid lines
    for r in range(ROWS + 1):
        for c in range(COLS + 1):
            # Draw circles to represent intersection points
            pygame.draw.circle(win, WHITE, (c * CELL_SIZE + 2 * PADDING,
                                             r * CELL_SIZE + 3 * PADDING), 2)

    # Update and draw each cell
    for cell in cells:
        cell.update(win)  # Update the visual representation of each cell

    # Display game over message if game is over
    if game_over:
        # Draw a message indicating the game is over
        rect = pygame.Rect((50, 100, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200))
        pygame.draw.rect(win, BLACK, rect)
        pygame.draw.rect(win, RED, rect, 2)

        over = font.render('Game Over', True, WHITE)
        win.blit(over, (rect.centerx - over.get_width() / 2, rect.y + 10))

        winner = '1' if p1_score > p2_score else '2'
        winner_img = font.render(f'Player {winner} Won', True, GREEN)
        win.blit(winner_img, (rect.centerx - winner_img.get_width() / 2, rect.centery - 10))

        # Display restart and quit instructions
        msg = 'Press r:restart, q:quit'

# Main game loop
reset_game_state()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_input_events()
    update_game_state()
    draw_game()

    pygame.display.update()

pygame.quit()
