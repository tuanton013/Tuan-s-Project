import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 900, 600
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
wordBoxWidth = 60
wordBoxLength = 80

# Game variables
words = ["PYTHON", "JAVA", "JAVASCRIPT", "RUBY", "PHP", "HTML", "CSS"]
word = random.choice(words)
guessed = ["A"]
correct = 0
flag = 0
chances = len(word) + 3

label_x = 200

alphatbet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphaBoxX = 700
alphaBoxY = 20
alphaBoxWidth = 150
alphaBoxHeight = 200



alphaLetterBox = 20
alphaButtonGap = 6
total_box_width = 4 * alphaLetterBox + 3 * alphaButtonGap
total_box_length = 7 * alphaLetterBox + 6 * alphaButtonGap


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
    total_dashline_width = len(word) * wordBoxWidth + (len(word) - 1) * 15

    # Calculate starting x-coordinate to center the dashlines
    start_x = (WIDTH - total_dashline_width) / 2.0

    # Draw dashlines for each letter in the word
    for _ in word:
        pygame.draw.rect(screen, WHITE, (start_x, 400, wordBoxWidth, wordBoxLength))
        start_x += wordBoxWidth + 20  # Move to the next dashline position
        
    # display guessed letters
    label = font_small.render("Guessed: ", True, WHITE)
    screen.blit(label, (label_x, 550))
    text = font_small.render(" ".join(guessed), True, WHITE)
    screen.blit(text, (label_x + 100, 550))
    
    # Draw alphabet box
    pygame.draw.rect(screen, WHITE, (alphaBoxX, alphaBoxY, alphaBoxWidth, alphaBoxHeight))
    
    
    start_x_button = ((alphaBoxWidth - total_box_width) / 2.0) + alphaBoxX
    start_y_button = ((alphaBoxHeight - total_box_length) / 2.0) + alphaBoxY
    # Draw alphabet buttons
    for i in range(26):
        x = start_x_button + (i % 4) * (alphaLetterBox + alphaButtonGap)
        y = start_y_button + (i // 4) * (alphaLetterBox + alphaButtonGap)
        pygame.draw.rect(screen, BLACK, (x, y, alphaLetterBox, alphaLetterBox))
        letter = font_small.render(alphatbet[i], True, WHITE)
        screen.blit(letter, (x, y))
    

    # Update the display
    pygame.display.flip()


pygame.quit()