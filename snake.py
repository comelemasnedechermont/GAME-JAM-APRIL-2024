import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 1000, 600
CELL_SIZE = 20

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.body = [(WIDTH / 2, HEIGHT / 2)]
        self.direction = RIGHT

    def move(self):
        new_head = (self.body[0][0] + self.direction[0] * CELL_SIZE, self.body[0][1] + self.direction[1] * CELL_SIZE)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    def check_collision(self, walls):
        head_rect = pygame.Rect(self.body[0][0], self.body[0][1], CELL_SIZE, CELL_SIZE)
        for wall in walls:
            if head_rect.colliderect(wall.rect):
                return True
        return False

class Food:
    def __init__(self, walls):
        self.position = self.generate_position(walls)

    def generate_position(self, walls):
        while True:
            position = (random.randint(1, WIDTH // CELL_SIZE - 2) * CELL_SIZE, random.randint(1, HEIGHT // CELL_SIZE - 2) * CELL_SIZE)
            if not any(wall.rect.collidepoint(position) for wall in walls):
                return position

    def respawn(self, walls):
        self.position = self.generate_position(walls)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))

def draw_score(surface, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    surface.blit(text, (10, 579))

def startSnake():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Open')
    snake = Snake()
    walls = pygame.sprite.Group()
    walls.add(Wall(0, 0, WIDTH, CELL_SIZE))
    walls.add(Wall(0, 0, CELL_SIZE, HEIGHT))
    walls.add(Wall(0, HEIGHT - CELL_SIZE, WIDTH, CELL_SIZE))
    walls.add(Wall(WIDTH - CELL_SIZE, 0, CELL_SIZE, HEIGHT))
    food = Food(walls)
    clock = pygame.time.Clock()
    score = 0
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
        if score >= 10:
            font = pygame.font.Font(None, 60)
            text = font.render("Voici un morceau du mot de passe 'zP1qR8'", True, WHITE)
            text2 = font.render("Appuyez sur ESC pour revenir au menu", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            text_rect2 = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            screen.blit(text, text_rect)
            screen.blit(text2, text_rect2)
            pygame.display.update()
        else:
            snake.move()
            if snake.body[0] == food.position:
                snake.grow()
                food.respawn(walls)
                score += 1
            if snake.check_collision(walls):
                running = False
            snake.draw(screen)
            food.draw(screen)
            walls.draw(screen)
            draw_score(screen, score)
            pygame.display.update()
            clock.tick(10)

