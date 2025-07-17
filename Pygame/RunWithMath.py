import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Template")

# Set up clock for FPS
clock = pygame.time.Clock()
FPS = 60

# Background scrolling variables
bg_y1 = 0  # First background position
bg_y2 = -HEIGHT  # Second background position (starts above screen)
scroll_speed = 2  # Speed of scrolling (pixels per frame)

# Square player variables
square_size = 100
square_x = (WIDTH - square_size) // 2  # Start at center
square_y = (HEIGHT - square_size) // 2  # Start at center
square_speed = 5  # Speed of square movement

# Function to draw background pattern
def draw_background_pattern(surface, y_offset):
    """Draw a repeating background pattern at the given y_offset"""
    # Create a grid pattern
    grid_size = 50
    grid_color = (50, 50, 50)  # Slightly lighter than background
    
    # Draw vertical lines
    for x in range(0, WIDTH, grid_size):
        pygame.draw.line(surface, grid_color, (x, y_offset), (x, y_offset + HEIGHT), 1)
    
    # Draw horizontal lines
    for y in range(0, HEIGHT + grid_size, grid_size):
        pygame.draw.line(surface, grid_color, (0, y + y_offset), (WIDTH, y + y_offset), 1)
    
    # Add some decorative elements
    for i in range(0, HEIGHT + 100, 150):  # Every 150 pixels
        # Draw small rectangles as decorative elements
        rect_x = WIDTH // 4
        rect_y = i + y_offset
        if -50 <= rect_y <= HEIGHT + 50:  # Only draw if visible
            pygame.draw.rect(surface, (60, 60, 60), (rect_x, rect_y, 20, 40))
            pygame.draw.rect(surface, (60, 60, 60), (WIDTH - rect_x - 20, rect_y + 75, 20, 40))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle continuous key presses for smooth movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        square_x -= square_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        square_x += square_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        square_y -= square_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        square_y += square_speed
    
    # Keep square within screen boundaries
    square_x = max(0, min(square_x, WIDTH - square_size))
    square_y = max(0, min(square_y, HEIGHT - square_size))

    # Game logic goes here
    
    # Update background scrolling
    bg_y1 += scroll_speed
    bg_y2 += scroll_speed
    
    # Reset background positions when they go off screen
    if bg_y1 >= HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 >= HEIGHT:
        bg_y2 = -HEIGHT

    # Drawing code goes here
    screen.fill((30, 30, 30))  # Fill the screen with a dark color

    # Draw scrolling background pattern
    draw_background_pattern(screen, bg_y1)
    draw_background_pattern(screen, bg_y2)

    # Draw the movable square
    square_color = (255, 100, 100)  # Brighter red color for better visibility
    pygame.draw.rect(screen, square_color, (square_x, square_y, square_size, square_size))
    
    # Add a white border around the square to make it more visible
    pygame.draw.rect(screen, (255, 255, 255), (square_x, square_y, square_size, square_size), 3)
    
    # Display controls
    font = pygame.font.Font(None, 36)
    controls_text = font.render("WASD or Arrow Keys to move", True, (255, 255, 255))
    screen.blit(controls_text, (10, 10))
    pygame.display.flip()
    clock.tick(FPS)
    

pygame.quit()
sys.exit()