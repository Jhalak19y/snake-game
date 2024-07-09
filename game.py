import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.Font(None, 36)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.color = GREEN
        self.score = 0
        self.direction_queue = []  # Queue to store direction changes

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        # Allow only valid turns
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        elif len(self.direction_queue) > 0 and (point[0] * -1, point[1] * -1) == self.direction_queue[0]:
            return
        else:
            self.direction_queue.append(point)

    def move(self):
        # Process direction queue
        if len(self.direction_queue) > 0:
            self.direction = self.direction_queue.pop(0)

        # Move snake
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)

        # Check collisions
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.score = 0
        self.direction_queue = []

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    self.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.turn((1, 0))

    def collision_with_boundaries(self):
        return self.get_head_position()[0] >= SCREEN_WIDTH or self.get_head_position()[0] < 0 or self.get_head_position()[1] >= SCREEN_HEIGHT or self.get_head_position()[1] < 0

    def collision_with_self(self):
        return any([block == self.get_head_position() for block in self.positions[1:]])

    def get_score(self):
        return self.score

    def increase_score(self):
        self.score += 1
        self.length += 1

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, BLACK, r, 1)

# Main function
def main():
    global SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH, GRID_HEIGHT

    # Set screen size based on current screen dimensions
    infoObject = pygame.display.Info()
    SCREEN_WIDTH = infoObject.current_w // 2
    SCREEN_HEIGHT = infoObject.current_h // 2
    GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
    GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()

    start_time = time.time()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    snake.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.turn((1, 0))

        # Check time limit
        elapsed_time = time.time() - start_time
        if elapsed_time >= 60:
            game_over = True

        snake.move()
        if snake.get_head_position() == food.position:
            snake.increase_score()
            food.randomize_position()

        screen.fill(WHITE)
        snake.draw(surface)
        food.draw(surface)

        # Display score
        score_text = FONT.render(f"Score: {snake.get_score()}", True, BLACK)
        surface.blit(score_text, (10, 10))

        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(10)

    # Game over screen
    screen.fill(WHITE)
    game_over_text = FONT.render(f"Game Over! Final Score: {snake.get_score()}", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
    pygame.display.update()
    time.sleep(3)  # Display game over screen for 3 seconds before quitting
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
