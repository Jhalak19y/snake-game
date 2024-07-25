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
        self.direction = (0, 0)  # Start with no movement
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
        if self.collision_with_self():
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = (0, 0)  # Reset direction
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
        head_x, head_y = self.get_head_position()
        return head_x >= SCREEN_WIDTH or head_x < 0 or head_y >= SCREEN_HEIGHT or head_y < 0

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

    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()

    # Start Screen
    start_screen = True
    while start_screen:
        screen.fill(WHITE)
        start_text = FONT.render("Press any key to Start", True, BLACK)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                start_screen = False  # Exit start screen

    start_time = time.time()
    game_over = False

    while not game_over:
        snake.handle_keys()  # Handle user input

        # Check time limit (10 seconds)
        elapsed_time = time.time() - start_time
        if elapsed_time >= 10:
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
        clock.tick(10)  # Control the frame rate

    # Game over screen
    screen.fill(WHITE)
    game_over_text = FONT.render(f"Game Over! Final Score: {snake.get_score()}", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    pygame.display.update()
    time.sleep(3)  # Display game over screen for 3 seconds before quitting
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
