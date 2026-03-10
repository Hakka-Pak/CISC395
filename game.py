import pygame
import random
import sys

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
DARK_BLUE = (0, 0, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
SHADOW = (100, 0, 0)
HIGHLIGHT = (255, 100, 100)
PURPLE_SHADOW = (50, 0, 50)
PURPLE_HIGHLIGHT = (200, 100, 200)

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
        self.foods = [] # List of (x, y, is_special)
        for _ in range(3):
            self.spawn_food()

    def spawn_food(self):
        while True:
            x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
            is_special = random.random() < 0.2 # 20% chance for special food
            if (x, y) not in self.snake and not any(f[0] == x and f[1] == y for f in self.foods):
                self.foods.append((x, y, is_special))
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
        eaten_food = None
        for food in self.foods:
            if new_head[0] == food[0] and new_head[1] == food[1]:
                eaten_food = food
                break

        if eaten_food:
            self.score += 50 if eaten_food[2] else 10
            self.foods.remove(eaten_food)
            self.spawn_food()
        else:
            self.snake.pop()

    def draw_3d_food(self, x, y, is_special):
        center = (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2)
        radius = GRID_SIZE // 2 - 2
        
        main_color = PURPLE if is_special else RED
        shadow_color = PURPLE_SHADOW if is_special else SHADOW
        highlight_color = PURPLE_HIGHLIGHT if is_special else HIGHLIGHT

        # Shadow
        pygame.draw.circle(self.screen, shadow_color, (center[0] + 2, center[1] + 2), radius)
        # Main body
        pygame.draw.circle(self.screen, main_color, center, radius)
        # Highlight
        pygame.draw.circle(self.screen, highlight_color, (center[0] - 2, center[1] - 2), radius // 2)

    def render(self):
        self.screen.fill(DARK_BLUE)

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            color = ORANGE if i == 0 else YELLOW
            pygame.draw.rect(self.screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

        # Draw food
        for x, y, is_special in self.foods:
            self.draw_3d_food(x, y, is_special)

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
            self.clock.tick(15)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
