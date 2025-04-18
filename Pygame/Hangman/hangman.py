import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (101, 167, 101)
PASTEL_BLUE = (186, 225, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)
TURQUOISE = (64, 224, 208)


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
chances = 5
PI = 3.14
# Main game loop
running = True


label_x = 200

# Alphabet letters
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# prize words
prize_words = ["Better Luck", "Letter +1",
               "Heart +1", "Heart -1", "Hint +1",  "Better Luck", "Letter +1", "Heart +1"]
# prize_words = ["0", "1",
#                "2", "3", "4"]
prize_words_index = [0, 1, 2, 3, 4, 0, 1, 2]

# Alphabet button
alphaLetterBox = 50
alphaButtonGap = 10
total_box_width = 7 * alphaLetterBox + 6 * alphaButtonGap
total_box_length = 4 * alphaLetterBox + 3 * alphaButtonGap
alphabet_button = {}

# wheel
wheelRadius = 200
wheelX = 250
wheelY = 230

rotation_angle = 0
rotation_speed = 20

# spinning wheel button
spinning = False
spin_start_time = 0
spin_duration = 0

font = pygame.font.SysFont("arial", 80)
font_small = pygame.font.SysFont("arial", 25)
font_small_bold = pygame.font.SysFont("arial", 15, True)

# heart object
heart_image = pygame.image.load("heart.png")
heart_image = pygame.transform.scale(heart_image, (50, 50))

# function to draw a circle with triangles


def draw_lines_in_circle(surface, center_x, center_y, radius, num_lines, color):
    angle_step = 360 / num_lines
    for i in range(num_lines):
        angle = angle_step * i
        rad = math.radians(angle)
        x = center_x + radius * math.cos(rad)
        y = center_y - radius * math.sin(rad)

        # Draw the line from the center to the edge of the circle
        pygame.draw.line(surface, color, (center_x, center_y), (x, y), 2)


def color_triangle(surface, center_x, center_y, radius, start_angle, end_angle, color):
    # Define the points for the triangle
    points = [(center_x, center_y)]  # Start at the center of the circle

    # Generate points along the arc from start_angle to end_angle
    for angle in range(start_angle, end_angle+1):  # Increment by 1 degree for smoothness
        rad = math.radians(angle)
        x = center_x + radius * math.cos(rad)
        # Subtract because Pygame's y-axis is inverted
        y = center_y - radius * math.sin(rad)
        points.append((x, y))

    # Add the last point on the arc
    points.append((center_x + radius * math.cos(rad),
                  center_y - radius * math.sin(rad)))

    # Draw the filled polygon
    pygame.draw.polygon(surface, color, points)


def draw_spinning_arrow(surface, center_x, center_y, radius, start_angle, end_angle, color):
    # Draw the small circle at the center of the big circle
    small_circle_radius = radius * 0.15
    pygame.draw.circle(surface, color, (center_x, center_y),
                       small_circle_radius)

    # Calculate the position of the arrow tip
    arrow_length = small_circle_radius * 2
    # Convert start_angle to radians
    arrow_angle_rad = math.radians(start_angle)
    arrow_tip_x = center_x + arrow_length * math.cos(arrow_angle_rad)
    arrow_tip_y = center_y - arrow_length * math.sin(arrow_angle_rad)

    # Draw the arrow as a small triangle
    arrow_base_length = small_circle_radius * 0.5
    arrow_height = small_circle_radius/2

    # Calculate the base points of the triangle
    base_point1_x = center_x - arrow_height * math.sin(arrow_angle_rad)
    base_point1_y = center_y - arrow_height * math.cos(arrow_angle_rad)

    base_point2_x = center_x + arrow_height * math.sin(arrow_angle_rad)
    base_point2_y = center_y + arrow_height * math.cos(arrow_angle_rad)

    # Draw the triangle
    pygame.draw.polygon(surface, color, [
        (arrow_tip_x, arrow_tip_y),
        (base_point1_x, base_point1_y),
        (base_point2_x, base_point2_y)
    ])

    # draw spin text in the middle of the wheel
    spin_text = font_small.render("Spin", True, WHITE)
    spin_text_rect = spin_text.get_rect(center=(center_x, center_y))
    surface.blit(spin_text, spin_text_rect)


def step_angle(num_lines):
    # Generate angles from start_angle to end_angle with a step
    angle = 360 / num_lines
    return angle

# draw text prize in each section of the wheel


def draw_text_prize(surface, center_x, center_y, radius, num_lines, color, text, text_index):
    # Adjust the angle to keep the text readable
    step = step_angle(num_lines)
    # Loop through angles in 45-degree increments
    for i in range(num_lines):
        angle = -(i * step + step/2)  # Center the text in the section
        # Convert degrees to radians
        radians = math.radians(angle)

        text_radius = radius * 0.70

        x = center_x + text_radius * math.cos(radians)
        y = center_y + text_radius * math.sin(radians)

        prize_word = text[text_index[i]]
        text_surface = font_small_bold.render(
            prize_word, True, color)

        if 90 < abs(angle) < 270:
            adjusted_angle = angle + 180   # Flip the text
        else:
            adjusted_angle = angle

        # Rotate the text to match the angle of the line
        rotated_text = pygame.transform.rotate(text_surface, -adjusted_angle)
        # Center the text at the calculated position
        text_rect = rotated_text.get_rect(center=(x, y))
        # Draw the text on the surface
        surface.blit(rotated_text, text_rect)


# Function to draw word boxes
def draw_word_boxes(screen, word, clicked_buttons, font, box_color, text_color, box_width, box_height, start_x, start_y):
    for i, letter in enumerate(word):
        x = start_x + i * (box_width + 15)  # Add spacing between boxes
        y = start_y
        rect = pygame.Rect(x, y, box_width, box_height)
        pygame.draw.rect(screen, box_color, rect, border_radius=5)
        pygame.draw.rect(screen, text_color, rect, 2, border_radius=5)

        # If the letter has been guessed, grey it out
        if letter in clicked_buttons:
            text_surface = font.render(letter, True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)


def show_remaining_lives(WIDTH, screen, chances, heart_image):
    heart_x = WIDTH/2 - (chances * heart_image.get_width()) / 2
    heart_y = 50
    for i in range(chances):
        screen.blit(heart_image, (heart_x + i *
                    heart_image.get_width(), heart_y))


def draw_alphabet_buttons(screen, WHITE, BLACK, GREY, clicked_buttons, alphabet, alphaLetterBox, alphaButtonGap, alphabet_button, font_small, start_x_button, start_y_button):
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


def draw_game_over_message(screen, message, font, color):
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text_surface, text_rect)


# Function to reset the game
def reset_game():
    global word, clicked_buttons, chances
    word = random.choice(words)
    clicked_buttons.clear()
    chances = 5


def draw_color_triangles(screen, RED, DARK_GREEN, ORANGE, PINK, PURPLE, wheelRadius, wheelX, wheelY, color_triangle):
    fix_angle = 45
    color_triangle(screen, wheelX, wheelY, wheelRadius,
                   fix_angle + 45, fix_angle + 90, DARK_GREEN)
    color_triangle(screen, wheelX, wheelY, wheelRadius,
                   fix_angle + 90, fix_angle + 135, RED)
    color_triangle(screen, wheelX, wheelY, wheelRadius,
                   fix_angle-45, fix_angle, PINK)
    color_triangle(screen, wheelX, wheelY, wheelRadius,
                   fix_angle + 135, fix_angle + 180, PURPLE)
    color_triangle(screen, wheelX, wheelY, wheelRadius,
                   fix_angle + 180, fix_angle + 225, PINK)
    color_triangle(screen, wheelX, wheelY, wheelRadius,
                   fix_angle, fix_angle + 45, ORANGE)
    color_triangle(screen, wheelX, wheelY, wheelRadius,
                   fix_angle + 225, fix_angle + 270, ORANGE)
    color_triangle(screen, wheelX, wheelY, wheelRadius,
                   fix_angle + 270, fix_angle + 315, DARK_GREEN)


def get_arrow_angle(rotation_angle, num_sections):
    # Normalize the angle to be between 0 and 360 degrees
    # Negate to handle clockwise rotation
    normalized_angle = rotation_angle % 360

    # Calculate the angle per section
    section_angle = 360 / num_sections

    # Determine the section the arrow is pointing to
    section_index = int(normalized_angle // section_angle)

    return section_index


def open_one_letter(word, clicked_buttons):
    # Open one letter in the word
    for letter in word:
        if letter not in clicked_buttons:
            clicked_buttons.append(letter)
            break


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 1):
                pygame.mixer.pause()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the mouse is within the spin button
                if (wheelX - (wheelRadius*0.15) < mouse_x < wheelX + (wheelRadius*0.15) and
                        wheelY - (wheelRadius*0.15) < mouse_y < wheelY + (wheelRadius*0.15)):
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
                                # display game over message on screen
                                draw_game_over_message(
                                    screen, "Game Over!", font, RED)
                                pygame.display.flip()
                                pygame.time.delay(2000)  # Pause for 2 seconds
                                reset_game()

                        break

# Spinning the wheel
    if (spinning):
        draw_spinning_arrow(
            screen, wheelX, wheelY, wheelRadius, rotation_angle, rotation_angle + 45, GREEN)
        rotation_angle = (rotation_angle + rotation_speed) % 360
        # Decrease the speed gradually
        rotation_speed = max(rotation_speed-0.1, 0)
        spin_duration -= clock.get_time() / 1000
        if spin_duration <= 0:
            spinning = False
            section = get_arrow_angle(rotation_angle, 8)

            # prize logic here
            if (prize_words[section] == "Better Luck"):
                print("Better Luck")
            if (prize_words[section] == "Letter +1"):
                open_one_letter(word, clicked_buttons)
                print("Letter +1")
            if (prize_words[section] == "Heart +1"):
                chances += 1
                print("Heart +1")
            if (prize_words[section] == "Heart -1"):
                chances -= 1
                print("Heart -1")
            if (prize_words[section] == "Hint +1"):
                print("Hint +1")

                # Game logic here

                # Cap the frame rate
    clock.tick(FPS)

    # Drawing code here
    screen.fill(PASTEL_BLUE)

    # Calculate total width of all boxes and spaces
    total_word_width = len(word) * wordBoxWidth + (len(word) - 1) * 15

    # Calculate starting x-coordinate to center the boxes
    start_x = (WIDTH - total_word_width) / 2.0
    # start_y euqal to 20% of the screen height from the bottom
    start_y = HEIGHT - (0.2 * HEIGHT) - wordBoxLength

    draw_word_boxes(screen, word, clicked_buttons, font, WHITE,
                    BLACK, wordBoxWidth, wordBoxLength, start_x, start_y)

    # Draw alphabet buttons
    start_x_button = (
        WIDTH / 2 + (WIDTH / 2 - total_box_width) / 2) + alphaLetterBox
    start_y_button = 100
    draw_alphabet_buttons(screen, WHITE, BLACK, GREY, clicked_buttons, alphabet, alphaLetterBox,
                          alphaButtonGap, alphabet_button, font_small, start_x_button, start_y_button)

    # Draw wheel
    pygame.draw.circle(screen, BLACK, (wheelX, wheelY), wheelRadius)
    # I want to draw an arc for this circle
    pygame.draw.circle(screen, WHITE, (wheelX, wheelY),
                       wheelRadius, draw_top_right=1)

    # Draw the spin button
    # pygame.draw.rect(screen, BLACK, (wheelX - spinButtonWidth/2, wheelY + wheelRadius + spinButtonHeight/2,
    #                  spinButtonWidth, spinButtonHeight), border_radius=10)
    # spinButtonText = font_small.render("Spin", True, WHITE)
    # spinButtonText_rect = spinButtonText.get_rect(
    #     center=(wheelX, wheelY + wheelRadius + spinButtonHeight))
    # screen.blit(spinButtonText, spinButtonText_rect)

    # Draw the rotated quadrant
    pygame.draw.circle(screen, BLACK, (wheelX, wheelY), wheelRadius)

    draw_color_triangles(screen, RED, DARK_GREEN, ORANGE, PINK,
                         PURPLE, wheelRadius, wheelX, wheelY, color_triangle)

    # Draw the heart representing the chances left
    show_remaining_lives(WIDTH, screen, chances, heart_image)

    # Draw the lines to divide sections in the circle
    draw_lines_in_circle(screen, wheelX, wheelY, wheelRadius, 8, WHITE)
    # Draw the spinning arrow
    draw_spinning_arrow(screen, wheelX, wheelY, wheelRadius,
                        rotation_angle, rotation_angle + 45, GREY)
    # Draw the text in each section of the wheel
    draw_text_prize(screen, wheelX, wheelY, wheelRadius,
                    8, WHITE, prize_words, prize_words_index)

    pygame.display.flip()


pygame.quit()
