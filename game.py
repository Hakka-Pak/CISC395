import pygame
import random
import sys

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BRIGHT_GREEN = (50, 255, 50)
RED = (255, 0, 0)
SHADOW = (100, 0, 0)
HIGHLIGHT = (255, 100, 100)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.game_over_font = pygame.font.SysFont("Arial", 48)
        self.reset_game()

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.foods = []
        for _ in range(3):
            self.spawn_food()

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake and food not in self.foods:
                self.foods.append(food)
                break

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                else:
                    if event.key == pygame.K_w and self.direction != (0, 1):
                        self.direction = (0, -1)
                    elif event.key == pygame.K_s and self.direction != (0, -1):
                        self.direction = (0, 1)
                    elif event.key == pygame.K_a and self.direction != (1, 0):
                        self.direction = (-1, 0)
                    elif event.key == pygame.K_d and self.direction != (-1, 0):
                        self.direction = (1, 0)

    def update(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Check collisions
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.snake):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check food
        if new_head in self.foods:
            self.score += 10
            self.foods.remove(new_head)
            self.spawn_food()
        else:
            self.snake.pop()

    def draw_3d_food(self, x, y):
        center = (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2)
        radius = GRID_SIZE // 2 - 2
        # Shadow
        pygame.draw.circle(self.screen, SHADOW, (center[0] + 2, center[1] + 2), radius)
        # Main body
        pygame.draw.circle(self.screen, RED, center, radius)
        # Highlight
        pygame.draw.circle(self.screen, HIGHLIGHT, (center[0] - 2, center[1] - 2), radius // 2)

    def render(self):
        self.screen.fill(BLACK)

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            color = BRIGHT_GREEN if i == 0 else GREEN
            pygame.draw.rect(self.screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

        # Draw food
        for x, y in self.foods:
            self.draw_3d_food(x, y)

        # Draw UI
        score_surface = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_surface, (10, 10))
        food_count_surface = self.font.render(f"Food Items: {len(self.foods)}", True, WHITE)
        self.screen.blit(food_count_surface, (10, 40))

        if self.game_over:
            game_over_surface = self.game_over_font.render("GAME OVER", True, WHITE)
            restart_surface = self.font.render("Press R to Restart", True, WHITE)
            self.screen.blit(game_over_surface, (WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(restart_surface, (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 + 20))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(10)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
