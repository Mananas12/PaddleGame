import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
FPS = 60
PADDLE_SPEED = 8
BALL_SPEED_X = 4
BALL_SPEED_Y = -4

# Full-screen dimensions
info_object = pygame.display.Info()
SCREEN_WIDTH = info_object.current_w
SCREEN_HEIGHT = info_object.current_h

# Adjusted constants for sizes
PADDLE_WIDTH = SCREEN_WIDTH // 5  # Paddle width is 1/5th of the screen width
PADDLE_HEIGHT = 30  # Paddle height increased
BALL_SIZE = 30  # Diameter of the ball
BRICK_WIDTH = SCREEN_WIDTH // 18  # 10 bricks per row, with some padding
BRICK_HEIGHT = 40  # Brick height
ROWS_OF_BRICKS = 8  # Adjusted for more gameplay complexity
COLS_OF_BRICKS = SCREEN_WIDTH // BRICK_WIDTH - 2  # Calculated based on the screen width

# Set up full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Brick Breaker")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
DARK_GRAY = (105, 105, 105)
BLUE = (0, 50, 200)

# Load images
BACKGROUND_IMAGE = pygame.image.load('background.jpg')
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to screen size
PADDLE_IMAGE = pygame.image.load('paddle.png')
PADDLE_IMAGE = pygame.transform.scale(PADDLE_IMAGE, (PADDLE_WIDTH, PADDLE_HEIGHT))  # Resize paddle image
BALL_IMAGE = pygame.image.load('ball.png')
BALL_IMAGE = pygame.transform.scale(BALL_IMAGE, (BALL_SIZE, BALL_SIZE))  # Resize ball image

# Load brick images and scale to smaller size (adjusted to the new brick dimensions)
BRICK_IMAGES = [
    pygame.transform.scale(pygame.image.load('brick_red.png'), (BRICK_WIDTH, BRICK_HEIGHT)),
    pygame.transform.scale(pygame.image.load('brick_green.png'), (BRICK_WIDTH, BRICK_HEIGHT)),
    pygame.transform.scale(pygame.image.load('brick_blue.png'), (BRICK_WIDTH, BRICK_HEIGHT)),
    pygame.transform.scale(pygame.image.load('brick_yellow.png'), (BRICK_WIDTH, BRICK_HEIGHT)),
    pygame.transform.scale(pygame.image.load('brick_cyan.png'), (BRICK_WIDTH, BRICK_HEIGHT)),
    pygame.transform.scale(pygame.image.load('brick_magenta.png'), (BRICK_WIDTH, BRICK_HEIGHT)),
    pygame.transform.scale(pygame.image.load('brick_orange.png'), (BRICK_WIDTH, BRICK_HEIGHT))
]

# Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PADDLE_IMAGE  # Use image for the paddle
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PADDLE_SPEED

        # Keep paddle within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = BALL_IMAGE  # Use image for the ball
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off the walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

        # Bounce off the paddle
        if pygame.sprite.collide_rect(self, paddle):
            # If the ball hits the paddle, reverse the vertical speed and adjust the ball's position
            self.speed_y = -self.speed_y
            # Adjust ball's position slightly to ensure no sticking to the paddle
            self.rect.bottom = paddle.rect.top

        # Ball falls off the screen
        if self.rect.bottom > SCREEN_HEIGHT:
            return True  # Return True if ball falls off the screen
        return False

# Brick class
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, brick_type):
        super().__init__()
        self.image = BRICK_IMAGES[brick_type]  # Select a random brick image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Function to display messages on the screen
def display_message(text, color):
    font = pygame.font.SysFont(None, 150)
    message = font.render(text, True, color)
    message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(message, message_rect)
    pygame.display.flip()
    pygame.time.delay(2000)  # Pause for 2 seconds

# Draw the buttons at the top right of the screen
def draw_buttons():
    # Button positions and sizes
    button_width = 120
    button_height = 40
    exit_button = pygame.Rect(SCREEN_WIDTH - button_width - 10, 10, button_width, button_height)
    minimize_button = pygame.Rect(SCREEN_WIDTH - 2 * button_width - 25, 10, button_width, button_height)

    # Draw buttons
    pygame.draw.rect(screen, BLUE, exit_button)
    pygame.draw.rect(screen, BLUE , minimize_button)

    # Draw button text
    font = pygame.font.SysFont(None, 36)
    exit_text = font.render("Exit", True, WHITE)
    minimize_text = font.render("Minimize", True, WHITE)
    screen.blit(exit_text, (exit_button.x + 30, exit_button.y + 5))
    screen.blit(minimize_text, (minimize_button.x + 10, minimize_button.y + 5))

    return exit_button, minimize_button

# Main Game Loop
def main():
    # Create paddle and ball objects
    global paddle
    paddle = Paddle()
    ball = Ball()

    # Create brick group and add bricks
    all_bricks = pygame.sprite.Group()

    # Adjusted brick placement and spacing
    BRICK_PADDING = 10  # Padding between bricks
    BRICK_X_OFFSET = (SCREEN_WIDTH - (COLS_OF_BRICKS * (BRICK_WIDTH + BRICK_PADDING))) // 2  # Center bricks horizontally
    BRICK_Y_OFFSET = 100  # Start bricks from a height of 100 pixels
    
    for row in range(ROWS_OF_BRICKS):
        for col in range(COLS_OF_BRICKS):
            brick_type = random.randint(0, len(BRICK_IMAGES) - 1)  # Random brick type
            x = BRICK_X_OFFSET + col * (BRICK_WIDTH + BRICK_PADDING)
            y = BRICK_Y_OFFSET + row * (BRICK_HEIGHT + BRICK_PADDING)
            brick = Brick(x, y, brick_type)
            all_bricks.add(brick)

    # Groups for all sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle)
    all_sprites.add(ball)
    all_sprites.add(*all_bricks)

    score = 0
    running = True
    while running:
        screen.fill(BLACK)

        # Draw background image
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        # Draw buttons
        exit_button, minimize_button = draw_buttons()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if Exit button is clicked
                if exit_button.collidepoint(mouse_pos):
                    running = False
                # Check if Minimize button is clicked
                if minimize_button.collidepoint(mouse_pos):
                    pygame.display.iconify()

        # Update all sprites
        ball_falls = ball.update()
        if ball_falls:
            display_message("GAME OVER", WHITE)
            print(f"Game Over! Final Score: {score}")
            running = False
            continue

        # Check for collisions between ball and bricks
        bricks_hit = pygame.sprite.spritecollide(ball, all_bricks, True)
        score += len(bricks_hit)

        # Update paddle and ball
        all_sprites.update()

        # Draw all sprites
        all_sprites.draw(screen)

        # Display score
        font = pygame.font.SysFont(None, 50)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Check if all bricks are destroyed
        if len(all_bricks) == 0:
            display_message("YOU WIN", WHITE)
            print(f"You Win! Final Score: {score}")
            running = False

        # Update the screen
        pygame.display.flip()

        # Control frame rate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
