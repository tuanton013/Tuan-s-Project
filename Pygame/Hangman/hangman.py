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
guessed = []
correct = 0
flag = 0
chances = 3

label_x = 200

# Alphabet box
alphatbet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphaBoxX = 700
alphaBoxY = 20
alphaBoxWidth = 150
alphaBoxHeight = 200

# Alphabet button
alphaLetterBox = 20
alphaButtonGap = 6
total_box_width = 4 * alphaLetterBox + 3 * alphaButtonGap
total_box_length = 7 * alphaLetterBox + 6 * alphaButtonGap
alphabet_button = {}

# wheel
wheelRadius = 100
wheelX = 150
wheelY = 150


font = pygame.font.SysFont("arial", 80)
font_small = pygame.font.SysFont("arial", 20)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(event.button == 1):
                pygame.mixer.pause()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letter, rect in alphabet_button.items():
                    if rect.collidepoint(mouse_x, mouse_y):
                        print(f"Cliked on {letter}")
                        if letter in guessed:
                            continue
                        if letter in word:
                            guessed.append(letter)
                        else:
                            guessed.append(letter)
                            chances -= 1
                            print(f"Chances left: {chances}")
                            if chances == 0:
                                print("You lost")
                                running = False
                        break
                        
                    
            

    # Game logic here
    

    # Cap the frame rate
    clock.tick(FPS)
    
    # Drawing code here
    screen.fill(GREY)

    
    # Calculate total width of all boxes and spaces
    total_dashline_width = len(word) * wordBoxWidth + (len(word) - 1) * 15

    # Calculate starting x-coordinate to center the boxes
    start_x = (WIDTH - total_dashline_width) / 2.0

    # Draw box for each letter in the word
    for box in word:
        pygame.draw.rect(screen, WHITE, (start_x, 400, wordBoxWidth, wordBoxLength))
        if box in guessed:
            text = font.render(box, True, BLACK)
            screen.blit(text, (start_x+2.5, 400))
        start_x += wordBoxWidth + 20  # Move to the next box position
        
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
        rect = pygame.Rect(x, y, alphaLetterBox, alphaLetterBox)
        alphabet_button[alphatbet[i]] = rect
        pygame.draw.rect(screen, BLACK, rect)
        letter = font_small.render(alphatbet[i], True, WHITE)
        screen.blit(letter, (x, y))
        
    # Draw wheel
    pygame.draw.circle(screen, BLACK, (wheelX, wheelY), wheelRadius)
    

    # Update the display
    pygame.display.flip()


pygame.quit()