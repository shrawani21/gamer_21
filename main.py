import pygame
import math

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
win = pygame.display.set_mode(SCREEN_SIZE)  # Set up the game window
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

ccell = None
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
    """
    Handle user input events.
    """
    global game_over, next_turn, ccell, up, right, bottom, left
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

        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            pygame.display.iconify()

    return True

def update_game_state():
    """
    Update the game state based on user input.
    """
    global next_turn, fill_count, p1_score, p2_score, player, turn
    if up:
        if ccell and ccell.row != 0:
            ncell = cells[ccell.index - COLS]
            ccell.sides[0] = True
            ncell.sides[2] = True
            fill_count += ccell.check_win(player)
            next_turn = True
    elif right:
        if ccell and ccell.col != COLS - 1:
            ncell = cells[ccell.index + 1]
            ccell.sides[1] = True
            ncell.sides[3] = True
            fill_count += ccell.check_win(player)
            next_turn = True
    elif bottom:
        if ccell and ccell.row != ROWS - 1:
            ncell = cells[ccell.index + COLS]
            ccell.sides[2] = True
            ncell.sides[0] = True
            fill_count += ccell.check_win(player)
            next_turn = True
    elif left:
        if ccell and ccell.col != 0:
            ncell = cells[ccell.index - 1]
            ccell.sides[3] = True
            ncell.sides[1] = True
            fill_count += ccell.check_win(player)
            next_turn = True

    if next_turn:
        turn = (turn + 1) % 2
        player = players[turn]
        next_turn = False

def draw_game():
    """
    Draw the game grid and current game state.
    """
    win.fill(BLACK)  # Clear the screen
    for cell in cells:
        cell.update(win)

    # Display scores
    score_text = font.render(f'Player 1: {p1_score}   Player 2: {p2_score}', True, WHITE)
    win.blit(score_text, (10, 10))

    if ccell:
        pygame.draw.rect(win, BLUE, ccell.rect, 3)

    pygame.display.update()  # Update the display

def main():
    """
    Main game loop.
    """
    global game_over, fill_count, p1_score, p2_score
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)  # Cap the frame rate at 60 FPS

        if not handle_input_events():
            break

        if not game_over:
            update_game_state()

        if fill_count == ROWS * COLS:
            # Game over when all cells are filled
            game_over = True
            if p1_score > p2_score:
                print("Player 1 wins!")
            elif p1_score < p2_score:
                print("Player 2 wins!")
            else:
                print("It's a tie!")

        draw_game()

    pygame.quit()  # Clean up resources
