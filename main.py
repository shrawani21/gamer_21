import pygame
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
CELL_SIZE = 40
PADDING = 20
ROWS = COLS = (SCREEN_WIDTH - 4 * PADDING) // CELL_SIZE

WHITE = (255, 255, 255)
RED = (252, 91, 122)
BLUE = (78, 193, 246)
GREEN = (0, 255, 0)
BLACK = (12, 12, 12)
DARK_GRAY = (30, 30, 30)
LIGHT_GRAY = (100, 100, 100)


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Game with Replay and Quit")

font = pygame.font.SysFont('cursive', 25)

# buttons
button_width = 200
button_height = 50

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

def reset_game():
    
    return create_cells(), 0, 0, 0, ['X', 'O'], 'X', False, False

def draw_button(text, color, x, y, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    pygame.draw.rect(screen, color, (x, y, button_width, button_height))
    if x + button_width > mouse[0] > x and y + button_height > mouse[1] > y and click[0] == 1 and action:
        action()

    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + button_width / 2, y + button_height / 2))
    screen.blit(text_surf, text_rect)

def replay_game():
    global cells, fill_count, p1_score, p2_score, players, current_player, game_over, next_turn
    cells, fill_count, p1_score, p2_score, players, current_player, game_over, next_turn = reset_game()

def quit_game():
    pygame.quit()
    sys.exit()

def main():
    global cells, fill_count, p1_score, p2_score, players, current_player, game_over, next_turn

    clock = pygame.time.Clock()
    cells, fill_count, p1_score, p2_score, players, current_player, game_over, next_turn = reset_game()

    running = True
    pos, current_cell = None, None
    up, right, bottom, left = False, False, False, False

    while running:
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
                    replay_game()
                elif not game_over:
                    if event.key == pygame.K_UP:
                        up = True
                    elif event.key == pygame.K_RIGHT:
                        right = True
                    elif event.key == pygame.K_DOWN:
                        bottom = True
                    elif event.key == pygame.K_LEFT:
                        left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up = False
                elif event.key == pygame.K_RIGHT:
                    right = False
                elif event.key == pygame.K_DOWN:
                    bottom = False
                elif event.key == pygame.K_LEFT:
                    left = False

        screen.fill(DARK_GRAY)

        for r in range(ROWS + 1):
            for c in range(COLS + 1):
                pygame.draw.circle(screen, WHITE, (c * CELL_SIZE + 2 * PADDING, r * CELL_SIZE + 3 * PADDING), 2)

        for cell in cells:
            cell.update(screen)
            if pos and cell.rect.collidepoint(pos):
                current_cell = cell

        draw_button("Replay", BLUE, SCREEN_WIDTH // 4 - button_width // 2, SCREEN_HEIGHT // 2, replay_game)
        draw_button("Quit", RED, 3 * SCREEN_WIDTH // 4 - button_width // 2, SCREEN_HEIGHT // 2, quit_game)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
