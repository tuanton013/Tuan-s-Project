import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PASTEL_BLUE = (186,225, 255)

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

# Objects
wordBoxWidth = 60
wordBoxLength = 80

# Game variables
words = ["PYTHON", "JAVAA", "JAVASCRIPT", "RUBY", "PHP", "HTML", "CSS"]
word = random.choice(words)
clicked_buttons = []
correct = 0
flag = 0
chances = 3
PI = 3.14

label_x = 200

# Alphabet letters
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Alphabet button
alphaLetterBox = 50
alphaButtonGap = 10
total_box_width = 7 * alphaLetterBox + 6 * alphaButtonGap
total_box_length = 4 * alphaLetterBox + 3 * alphaButtonGap
alphabet_button = {}

# wheel
wheelRadius = 100
wheelX = 150
wheelY = 150

rotation_angle = 0
rotation_speed = 20

# spinning wheel button
spinButtonX = 100
spinButtonY = 280
spinButtonWidth = 100
spinButtonHeight = 50
spinning = False
spin_start_time = 0
spin_duration = 0

font = pygame.font.SysFont("arial", 80)
font_small = pygame.font.SysFont("arial", 25)

# heart object
heart_image = pygame.image.load("heart.png")
heart_image = pygame.transform.scale(heart_image, (50, 50))

# function to draw a circle with triangles


def draw_top_right_quadrant(surface, center_x, center_y, radius, start_angle, end_angle, color):

    start_angle = int(start_angle)
    end_angle = int(end_angle)
    # Define the points for the filled top-right quadrant
    points = [(center_x, center_y)]  # Start at the center of the circle

    # Generate points along the arc from 0 to 90 degrees
    for angle in range(start_angle, end_angle+1):  # Increment by 1 degree for smoothness
        rad = math.radians(angle)
        x = center_x + radius * math.cos(rad)
        # Subtract because Pygame's y-axis is inverted
        y = center_y - radius * math.sin(rad)
        print(f"Angle: {angle}, X: {x}, Y: {y}")
        points.append((x, y))

    # Add the last point on the arc
    points.append((center_x + radius * math.cos(rad),
                  center_y - radius * math.sin(rad)))

    # Draw the filled polygon
    pygame.draw.polygon(surface, color, points)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 1):
                pygame.mixer.pause()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the mouse is within the spin button
                if (spinButtonX <= mouse_x <= spinButtonX + spinButtonWidth and
                        spinButtonY <= mouse_y <= spinButtonY + spinButtonHeight):
                    print("Spin button clicked")
                    # Spin the wheel
                    spinning = True
                    rotation_speed = 20  # Set the initial speed of rotation
                    spin_start_time = pygame.time.get_ticks()
                    spin_duration = random.uniform(
                        2, 5)  # Spin for 2 to 5 seconds

                for letter, rect in alphabet_button.items():
                    if rect.collidepoint(mouse_x, mouse_y):
                        if letter in clicked_buttons:
                            continue
                        
                        clicked_buttons.append(letter)
                        
                        if letter in word:
                            clicked_buttons.append(letter)
                        else:
                            clicked_buttons.append(letter)
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
    screen.fill(PASTEL_BLUE)

    # Calculate total width of all boxes and spaces
    total_word_width = len(word) * wordBoxWidth + (len(word) - 1) * 15

    # Calculate starting x-coordinate to center the boxes
    start_x = (WIDTH - total_word_width) / 2.0
    start_y = 450

    # Draw box for each letter in the word
    for box in word:
        pygame.draw.rect(screen, WHITE, (start_x, start_y,
                         wordBoxWidth, wordBoxLength),border_radius=10)
        if box in clicked_buttons:
            text = font.render(box, True, BLACK)
            text_box_width, text_box_height = text.get_size()
            # Center the letter in the box
            x_box = start_x + (wordBoxWidth - text_box_width) / 2
            y_box = start_y + (wordBoxLength - text_box_height) / 2
            screen.blit(text, (x_box, y_box))
        start_x += wordBoxWidth + 20  # Move to the next box position


    start_x_button = (WIDTH / 2 + (WIDTH / 2 - total_box_width) / 2) + alphaLetterBox
    start_y_button = 100
    # Draw alphabet buttons
    for i in range(26):
        x = start_x_button + (i % 7) * (alphaLetterBox + alphaButtonGap)
        y = start_y_button + (i // 7) * (alphaLetterBox + alphaButtonGap)
        rect = pygame.Rect(x, y, alphaLetterBox, alphaLetterBox)
        alphabet_button[alphabet[i]] = rect
        
        # check if the button has been clicked
        if alphabet[i] in clicked_buttons:
            transparent_surface = pygame.Surface(
                            (alphaLetterBox, alphaLetterBox), pygame.SRCALPHA)

            # Draw the button with transparency
            pygame.draw.rect(transparent_surface, GREY, (0, 0,
                            alphaLetterBox, alphaLetterBox), border_radius=10)
            # Draw the letter inside the button
            letter = font_small.render(alphabet[i], True, WHITE)
            text_width, text_height = letter.get_size()
            # Center the letter in the box
            x = (alphaLetterBox - text_width) / 2
            y = (alphaLetterBox - text_height) / 2
            # Draw the letter
            transparent_surface.blit(letter, (x, y))
            # Draw the transparent surface on the screen
            screen.blit(transparent_surface, (rect.x, rect.y))
        else: 
            pygame.draw.rect(screen, BLACK, rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
        
        # Draw the letter inside the button
        letter = font_small.render(alphabet[i], True, WHITE)
        text_width, text_height = letter.get_size()
        # Center the letter in the box
        x = rect.x + (alphaLetterBox - text_width) / 2
        y = rect.y + (alphaLetterBox - text_height) / 2
        # Draw the letter
        screen.blit(letter, (x, y))
        

    # Draw wheel
    pygame.draw.circle(screen, BLACK, (wheelX, wheelY), wheelRadius)
    # I want to draw an arc for this circle
    pygame.draw.circle(screen, WHITE, (wheelX, wheelY),
                       wheelRadius, draw_top_right=1)

    # Draw the spin button
    pygame.draw.rect(screen, BLACK, (spinButtonX, spinButtonY,
                     spinButtonWidth, spinButtonHeight), border_radius=10)
    spinButtonText = font_small.render("Spin", True, WHITE)
    screen.blit(spinButtonText, (spinButtonX + 10, spinButtonY + 10))

    # Draw the rotated quadrant
    pygame.draw.circle(screen, BLACK, (wheelX, wheelY), wheelRadius)

    draw_top_right_quadrant(screen, wheelX, wheelY, wheelRadius,
                            rotation_angle, rotation_angle + 45, GREEN)

    if (spinning):
        draw_top_right_quadrant(
            screen, wheelX, wheelY, wheelRadius, rotation_angle, rotation_angle + 45, GREEN)
        rotation_angle = (rotation_angle + rotation_speed) % 360
        # Decrease the speed gradually
        rotation_speed = max(rotation_speed-0.1, 0)
        spin_duration -= clock.get_time() / 1000
        if spin_duration <= 0:
            spinning = False
            # Here you can add logic to determine the result of the spin
            # For example, you can check which section of the wheel was landed on
            # and update the game state accordingly.
            print("Spin finished")

    # Draw the heart representing the chances left
    heart_x = WIDTH/2 - (chances * heart_image.get_width()) / 2
    heart_y = 50
    for i in range(chances):
        screen.blit(heart_image, (heart_x + i *
                    heart_image.get_width(), heart_y))
        # Update the display
    pygame.display.flip()


pygame.quit()
