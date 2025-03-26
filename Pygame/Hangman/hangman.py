import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

# Objects
dashlineWidth = 100
dashlineHeight = 5

# Game variables
words = ["PYTHON", "JAVA", "JAVASCRIPT", "RUBY", "PHP", "HTML", "CSS"]
word = random.choice(words)
guessed = []
correct = 0
flag = 0
chances = len(word) + 3

font = pygame.font.SysFont("arial", 40)
font_small = pygame.font.SysFont("arial", 20)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            

    # Game logic here

    # Cap the frame rate
    clock.tick(FPS)
    
    # Drawing code here
    screen.fill(GREY)

    
    # Calculate total width of all dashlines and spaces
    total_dashline_width = len(word) * dashlineWidth + (len(word) - 1) * 15

    # Calculate starting x-coordinate to center the dashlines
    start_x = (WIDTH - total_dashline_width) // 2

    # Draw dashlines for each letter in the word
    for _ in word:
        pygame.draw.rect(screen, WHITE, (start_x, 500, dashlineWidth, dashlineHeight))
        start_x += dashlineWidth + 15  # Move to the next dashline position

    # Update the display
    pygame.display.flip()


pygame.quit()