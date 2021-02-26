# Import the pygame library and initialise the game engine
import pygame
from random import randint

pygame.init()

# Define some colors
WHITE = (255, 255, 255)
DARK_BLUE = (36, 90, 190)
LIGHT_BLUE = (0, 176, 240)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

total_score = 0
lives = 3

# Open a new window
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game by Amey")

# This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()


class Paddle(pygame.sprite.Sprite):
    # This class represents a paddle. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the paddle, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def move_left(self, pixels):
        self.rect.x -= pixels
        # Check that you are not going too far (off the screen)
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self, pixels):
        self.rect.x += pixels
        # Check that you are not going too far (off the screen)
        if self.rect.x > 700:
            self.rect.x = 700


# Create the Paddle
paddle = Paddle(LIGHT_BLUE, 100, 10)
paddle.rect.x = 350
paddle.rect.y = 560


class Ball(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the ball (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity = [randint(4, 8), randint(-8, 8)]

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8, 8)


# Create the ball sprite
ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195


class Brick(pygame.sprite.Sprite):
    # This class represents a brick. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the brick, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the brick (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()


all_bricks = pygame.sprite.Group()
for i in range(7):
    brick = Brick(RED, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(ORANGE, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(YELLOW, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)

# Add the paddle to the list of sprites
all_sprites_list.add(paddle)
all_sprites_list.add(ball)

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop

    # Moving the paddle when the use uses the arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move_left(5)
    if keys[pygame.K_RIGHT]:
        paddle.move_right(5)

    # --- Game logic should go here
    all_sprites_list.update()

    # Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x >= 790:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 590:
        ball.velocity[1] = -ball.velocity[1]
        lives -= 1
        if lives == 0:
            # Display Game Over Message for 3 seconds
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", 1, WHITE)
            screen.blit(text, (250, 300))
            pygame.display.flip()
            pygame.time.wait(3000)

            # Stop the Game
            carryOn = False

    if ball.rect.y < 40:
        ball.velocity[1] = -ball.velocity[1]

    # Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddle):
        ball.rect.x -= ball.velocity[0]
        ball.rect.y -= ball.velocity[1]
        ball.bounce()

    # Check if there is a car collision
    brick_collision_list = pygame.sprite.spritecollide(ball, all_bricks, False)
    for brick in brick_collision_list:
        ball.bounce()
        total_score += 1
        brick.kill()
        if len(all_bricks) == 0:
            # Display Level Complete Message for 3 seconds
            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL COMPLETE", 1, WHITE)
            screen.blit(text, (200, 300))
            pygame.display.flip()
            pygame.time.wait(3000)

            # Stop the Game
            carryOn = False

    # --- Drawing code should go here
    # First, clear the screen to dark blue.
    screen.fill(DARK_BLUE)
    pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

    # Display the score and the number of lives at the top of the screen
    font = pygame.font.Font(None, 34)
    text = font.render("Score: " + str(total_score), 1, WHITE)
    screen.blit(text, (20, 10))
    text = font.render("Lives: " + str(lives), 1, WHITE)
    screen.blit(text, (650, 10))

    # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()