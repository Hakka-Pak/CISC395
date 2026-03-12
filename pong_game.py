import pygame
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 40
BALL_SIZE = 9
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
WINNING_SCORE = 11

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class PongGame:
    """
    A classic Ping Pong game implemented using Pygame.
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Classic Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 40)
        self.large_font = pygame.font.SysFont("Arial", 72)
        
        self.reset_game()

    def reset_game(self):
        """Initializes or resets the game state."""
        self.p1_y = (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2
        self.p2_y = (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2
        self.p1_score = 0
        self.p2_score = 0
        self.winner = None
        self.reset_ball(random.choice([-1, 1]))

    def reset_ball(self, direction):
        """Resets the ball to the center and sets its initial direction."""
        self.ball_x = WINDOW_WIDTH // 2 - BALL_SIZE // 2
        self.ball_y = WINDOW_HEIGHT // 2 - BALL_SIZE // 2
        self.ball_dx = BALL_SPEED_X * direction
        self.ball_dy = BALL_SPEED_Y * random.choice([-1, 1])

    def handle_input(self):
        """Handles keyboard input for paddle movement and game restart."""
        keys = pygame.key.get_pressed()
        
        # Player 1 controls (W, S)
        if keys[pygame.K_w] and self.p1_y > 0:
            self.p1_y -= PADDLE_SPEED
        if keys[pygame.K_s] and self.p1_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
            self.p1_y += PADDLE_SPEED
            
        # Player 2 controls (Up, Down)
        if keys[pygame.K_UP] and self.p2_y > 0:
            self.p2_y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and self.p2_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
            self.p2_y += PADDLE_SPEED

        # Restart game
        if self.winner and keys[pygame.K_r]:
            self.reset_game()

    def update(self):
        """Updates the game state, including ball movement and collision detection."""
        if self.winner:
            return

        # Move the ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Wall collisions (top and bottom)
        if self.ball_y <= 0 or self.ball_y >= WINDOW_HEIGHT - BALL_SIZE:
            self.ball_dy *= -1

        # Paddle collisions
        ball_rect = pygame.Rect(self.ball_x, self.ball_y, BALL_SIZE, BALL_SIZE)
        p1_rect = pygame.Rect(20, self.p1_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        p2_rect = pygame.Rect(WINDOW_WIDTH - 20 - PADDLE_WIDTH, self.p2_y, PADDLE_WIDTH, PADDLE_HEIGHT)

        if ball_rect.colliderect(p1_rect):
            self.ball_dx = abs(self.ball_dx) # Ensure it moves right
            # Optional: Add influence based on where it hits the paddle
            self.ball_dy += (self.ball_y + BALL_SIZE/2 - (self.p1_y + PADDLE_HEIGHT/2)) * 0.1
            
        if ball_rect.colliderect(p2_rect):
            self.ball_dx = -abs(self.ball_dx) # Ensure it moves left
            # Optional: Add influence based on where it hits the paddle
            self.ball_dy += (self.ball_y + BALL_SIZE/2 - (self.p2_y + PADDLE_HEIGHT/2)) * 0.1

        # Scoring
        if self.ball_x < 0:
            self.p2_score += 1
            if self.p2_score >= WINNING_SCORE:
                self.winner = 2
            else:
                self.reset_ball(1) # Send towards player 2
                
        elif self.ball_x > WINDOW_WIDTH:
            self.p1_score += 1
            if self.p1_score >= WINNING_SCORE:
                self.winner = 1
            else:
                self.reset_ball(-1) # Send towards player 1

    def draw_net(self):
        """Draws a vertical dashed line in the center of the screen."""
        for y in range(0, WINDOW_HEIGHT, 40):
            pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH // 2 - 2, y + 10, 4, 20))

    def render(self):
        """Renders the game objects to the screen."""
        self.screen.fill(BLACK)
        
        # Draw net
        self.draw_net()
        
        # Draw paddles
        pygame.draw.rect(self.screen, WHITE, (20, self.p1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH - 20 - PADDLE_WIDTH, self.p2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        
        # Draw ball
        pygame.draw.rect(self.screen, WHITE, (self.ball_x, self.ball_y, BALL_SIZE, BALL_SIZE))
        
        # Draw scores
        p1_score_text = self.font.render(str(self.p1_score), True, WHITE)
        p2_score_text = self.font.render(str(self.p2_score), True, WHITE)
        self.screen.blit(p1_score_text, (WINDOW_WIDTH // 4, 20))
        self.screen.blit(p2_score_text, (3 * WINDOW_WIDTH // 4, 20))
        
        # Draw winner message
        if self.winner:
            win_text = self.large_font.render(f"Player {self.winner} Wins!", True, WHITE)
            restart_text = self.font.render("Press 'R' to Restart", True, WHITE)
            
            win_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            
            self.screen.blit(win_text, win_rect)
            self.screen.blit(restart_text, restart_rect)
            
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(60) # 60 FPS

        pygame.quit()

if __name__ == "__main__":
    game = PongGame()
    game.run()
