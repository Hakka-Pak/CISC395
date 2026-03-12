import pygame
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 40
BALL_SIZE = 9
PADDLE_SPEED = 4
BALL_SPEED_X = 3
BALL_SPEED_Y = 3
WINNING_SCORE = 9

# Colors
NAVY_BLUE = (0, 0, 128)
GOLD = (239, 191, 4)

# Difficulty Constants (AI Speed/Accuracy)
DIFFICULTY_SETTINGS = {
    "Easy": {"speed": 2, "error_margin": 20},
    "Medium": {"speed": 3, "error_margin": 10},
    "Hard": {"speed": 4, "error_margin": 0}
}

class PongGame:
    """
    A classic Ping Pong game implemented using Pygame with 1P/2P modes and difficulty settings.
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Classic Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 40)
        self.large_font = pygame.font.SysFont("Arial", 72)
        
        self.state = "MENU" # MENU, PLAYING, GAME_OVER
        self.mode = "1P" # 1P or 2P
        self.difficulty = "Medium"
        
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
        """Handles keyboard input based on the current game state."""
        keys = pygame.key.get_pressed()
        
        if self.state == "MENU":
            # Menu Navigation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.mode = "1P"
                        self.state = "DIFFICULTY_SELECT"
                    if event.key == pygame.K_2:
                        self.mode = "2P"
                        self.state = "PLAYING"
                        self.reset_game()

        elif self.state == "DIFFICULTY_SELECT":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.difficulty = "Easy"
                        self.state = "PLAYING"
                        self.reset_game()
                    if event.key == pygame.K_m:
                        self.difficulty = "Medium"
                        self.state = "PLAYING"
                        self.reset_game()
                    if event.key == pygame.K_h:
                        self.difficulty = "Hard"
                        self.state = "PLAYING"
                        self.reset_game()

        elif self.state == "PLAYING":
            # Player 1 controls (W, S) - Only if 2P mode
            if self.mode == "2P":
                if keys[pygame.K_w] and self.p1_y > 0:
                    self.p1_y -= PADDLE_SPEED
                if keys[pygame.K_s] and self.p1_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
                    self.p1_y += PADDLE_SPEED
            
            # Player 2 controls (Up, Down) - Always human
            if keys[pygame.K_UP] and self.p2_y > 0:
                self.p2_y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and self.p2_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
                self.p2_y += PADDLE_SPEED

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        elif self.state == "GAME_OVER":
            if keys[pygame.K_r]:
                self.state = "MENU"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def update_ai(self):
        """Updates the computer-controlled paddle (Player 1) in 1P mode."""
        if self.mode == "1P":
            settings = DIFFICULTY_SETTINGS[self.difficulty]
            ai_speed = settings["speed"]
            error_margin = settings["error_margin"]
            
            # Only move if the ball is moving towards the AI side
            if self.ball_dx < 0:
                # Target the center of the paddle with a bit of randomness/error
                target_y = self.ball_y + BALL_SIZE // 2
                
                # Apply error margin (AI is less precise on lower difficulties)
                if abs(self.p1_y + PADDLE_HEIGHT // 2 - target_y) > error_margin:
                    if self.p1_y + PADDLE_HEIGHT // 2 < target_y:
                        self.p1_y += ai_speed
                    else:
                        self.p1_y -= ai_speed
            
            # Constrain to screen
            if self.p1_y < 0: self.p1_y = 0
            if self.p1_y > WINDOW_HEIGHT - PADDLE_HEIGHT: self.p1_y = WINDOW_HEIGHT - PADDLE_HEIGHT

    def update(self):
        """Updates the game state, including ball movement and collision detection."""
        if self.state != "PLAYING":
            return

        # Update AI if in 1P mode
        self.update_ai()

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
            self.ball_dx = abs(self.ball_dx)
            self.ball_dy += (self.ball_y + BALL_SIZE/2 - (self.p1_y + PADDLE_HEIGHT/2)) * 0.1
            
        if ball_rect.colliderect(p2_rect):
            self.ball_dx = -abs(self.ball_dx)
            self.ball_dy += (self.ball_y + BALL_SIZE/2 - (self.p2_y + PADDLE_HEIGHT/2)) * 0.1

        # Scoring
        if self.ball_x < 0:
            self.p2_score += 1
            if self.p2_score >= WINNING_SCORE:
                self.winner = 2
                self.state = "GAME_OVER"
            else:
                self.reset_ball(1)
                
        elif self.ball_x > WINDOW_WIDTH:
            self.p1_score += 1
            if self.p1_score >= WINNING_SCORE:
                self.winner = 1
                self.state = "GAME_OVER"
            else:
                self.reset_ball(-1)

    def draw_net(self):
        """Draws a vertical dashed line in the center of the screen."""
        for y in range(0, WINDOW_HEIGHT, 40):
            pygame.draw.rect(self.screen, GOLD, (WINDOW_WIDTH // 2 - 2, y + 10, 4, 20))

    def render_menu(self):
        """Renders the main menu."""
        self.screen.fill(NAVY_BLUE)
        title_text = self.large_font.render("PONG", True, GOLD)
        p1_text = self.font.render("Press '1' for 1 Player (CPU)", True, GOLD)
        p2_text = self.font.render("Press '2' for 2 Players", True, GOLD)
        
        self.screen.blit(title_text, title_text.get_rect(center=(WINDOW_WIDTH // 2, 150)))
        self.screen.blit(p1_text, p1_text.get_rect(center=(WINDOW_WIDTH // 2, 300)))
        self.screen.blit(p2_text, p2_text.get_rect(center=(WINDOW_WIDTH // 2, 380)))
        
        pygame.display.flip()

    def render_difficulty_select(self):
        """Renders the difficulty selection screen."""
        self.screen.fill(NAVY_BLUE)
        title_text = self.font.render("Select Difficulty", True, GOLD)
        easy_text = self.font.render("Press 'E' for Easy", True, GOLD)
        med_text = self.font.render("Press 'M' for Medium", True, GOLD)
        hard_text = self.font.render("Press 'H' for Hard", True, GOLD)
        
        self.screen.blit(title_text, title_text.get_rect(center=(WINDOW_WIDTH // 2, 150)))
        self.screen.blit(easy_text, easy_text.get_rect(center=(WINDOW_WIDTH // 2, 280)))
        self.screen.blit(med_text, med_text.get_rect(center=(WINDOW_WIDTH // 2, 340)))
        self.screen.blit(hard_text, hard_text.get_rect(center=(WINDOW_WIDTH // 2, 400)))
        
        pygame.display.flip()

    def render_game(self):
        """Renders the gameplay screen."""
        self.screen.fill(NAVY_BLUE)
        self.draw_net()
        
        pygame.draw.rect(self.screen, GOLD, (20, self.p1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(self.screen, GOLD, (WINDOW_WIDTH - 20 - PADDLE_WIDTH, self.p2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(self.screen, GOLD, (self.ball_x, self.ball_y, BALL_SIZE, BALL_SIZE))
        
        p1_label = "CPU" if self.mode == "1P" else "P1"
        p1_score_text = self.font.render(f"{p1_label}: {self.p1_score}", True, GOLD)
        p2_score_text = self.font.render(f"P2: {self.p2_score}", True, GOLD)
        self.screen.blit(p1_score_text, (WINDOW_WIDTH // 4 - 50, 20))
        self.screen.blit(p2_score_text, (3 * WINDOW_WIDTH // 4 - 50, 20))

        if self.mode == "1P":
            diff_text = self.font.render(f"Difficulty: {self.difficulty}", True, GOLD)
            self.screen.blit(diff_text, diff_text.get_rect(center=(WINDOW_WIDTH // 2, 50)))

        if self.state == "GAME_OVER":
            win_label = "CPU" if self.winner == 1 and self.mode == "1P" else f"Player {self.winner}"
            win_text = self.large_font.render(f"{win_label} Wins!", True, GOLD)
            restart_text = self.font.render("Press 'R' for Menu", True, GOLD)
            self.screen.blit(win_text, win_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40)))
            self.screen.blit(restart_text, restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)))
            
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        running = True
        while running:
            self.handle_input()
            self.update()
            
            if self.state == "MENU":
                self.render_menu()
            elif self.state == "DIFFICULTY_SELECT":
                self.render_difficulty_select()
            else:
                self.render_game()
                
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = PongGame()
    game.run()
