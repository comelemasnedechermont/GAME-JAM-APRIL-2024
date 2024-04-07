import pygame
import random

# Paramètres du jeu
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
FPS = 15  # Changer cette valeur pour ajuster la vitesse du jeu

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Formes possibles
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6],
     [6, 6]],

    [[0, 7, 0, 0],
     [0, 7, 0, 0],
     [0, 7, 0, 0],
     [0, 7, 0, 0]]
]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.score = 0
        self.game_over = False

    def new_piece(self):
        shape = random.choice(SHAPES)
        piece = {'shape': shape,
                 'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
                 'y': 0,
                 'color': random.choice([CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED])}
        return piece

    def draw_block(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.screen, BLACK, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] != 0:
                    self.draw_block(x, y, self.grid[y][x])

    def draw_piece(self):
        shape = self.current_piece['shape']
        color = self.current_piece['color']
        x, y = self.current_piece['x'], self.current_piece['y']
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col] != 0:
                    self.draw_block(x + col, y + row, color)

    def check_collision(self):
        shape = self.current_piece['shape']
        x, y = self.current_piece['x'], self.current_piece['y']
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col] != 0:
                    if x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT or self.grid[y + row][x + col] != 0:
                        return True
        return False

    def lock_piece(self):
        shape = self.current_piece['shape']
        x, y = self.current_piece['x'], self.current_piece['y']
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col] != 0:
                    self.grid[y + row][x + col] = self.current_piece['color']

    def check_lines(self):
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_clear.append(y)
        if lines_to_clear:
            self.score += len(lines_to_clear) * 100
            for y in lines_to_clear:
                del self.grid[y]
                self.grid.insert(0, [0] * GRID_WIDTH)

    def draw_score(self):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def game_over_screen(self):
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("GAME OVER", True, WHITE)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                          SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece['x'] -= 1
                        if self.check_collision():
                            self.current_piece['x'] += 1
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece['x'] += 1
                        if self.check_collision():
                            self.current_piece['x'] -= 1
                    elif event.key == pygame.K_DOWN:
                        self.current_piece['y'] += 1
                        if self.check_collision():
                            self.current_piece['y'] -= 1
                    elif event.key == pygame.K_SPACE:
                        self.rotate_piece()

            self.current_piece['y'] += 1
            if self.check_collision():
                self.current_piece['y'] -= 1
                self.lock_piece()
                self.check_lines()
                self.current_piece = self.new_piece()
                if self.check_collision():
                    self.game_over = True

            self.draw_grid()
            self.draw_piece()
            self.draw_score()
            if self.game_over:
                self.game_over_screen()
            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()

    def rotate_piece(self):
        shape = self.current_piece['shape']
        rotated_shape = [[shape[j][i] for j in range(len(shape))] for i in range(len(shape[0]) - 1, -1, -1)]
        if self.current_piece['x'] + len(rotated_shape[0]) > GRID_WIDTH or self.current_piece['y'] + len(rotated_shape) > GRID_HEIGHT:
            return
        self.current_piece['shape'] = rotated_shape

if __name__ == "__main__":
    game = Tetris()
    game.run()
