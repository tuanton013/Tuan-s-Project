import pygame
import sys
import math
import random
import sympy as sp
from sympy import symbols, expand, factor, solve, simplify


# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 1050
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Template")

# Set up clock for FPS
clock = pygame.time.Clock()
FPS = 60

# Background scrolling variables
bg_y1 = 0  # First background position
bg_y2 = -HEIGHT  # Second background position (starts above screen)
scroll_speed = 5  # Speed of scrolling (pixels per frame)

# Square player variables
square_size = 80
square_x = (WIDTH - square_size) // 2  # Start at center
square_y = (HEIGHT - square_size) // 2  # Start at center
square_speed = 5  # Speed of square movement

# Wall variables
walls = []  # List to store wall objects
wall_width = 80
wall_spawn_timer = 0
wall_spawn_delay = 120  # Spawn a wall every 2 seconds at 60 FPS
wall_color = (150, 75, 0)  # Brown color for walls

# hints variables  
hints = []  # List to store hints or messages

# gaps
gaps = []


# Game state
game_state = "playing"  # "playing", "game_over"

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

def create_wall():
    """Create a new wall with three rectangles and two gaps for the player to pass through"""
    gap_size = int(square_size * 1.5)  # Size of each gap
    
    # Calculate positions for 3 rectangles with 2 gaps between them
    # [Rect1] [Gap1] [Rect2] [Gap2] [Rect3]
    
    # Calculate rectangle widths (equal width for all 3 rectangles)
    rect_width = (WIDTH - 2 * gap_size) // 3
    
    # Rectangle 1: Left side (starts from 0)
    rect1_start = 0
    rect1_end = rect_width
    
    # Gap 1: Between rect1 and rect2
    gap1_start = rect1_end
    gap1_end = gap1_start + gap_size
    
    # Rectangle 2: Middle
    rect2_start = gap1_end
    rect2_end = rect2_start + rect_width
    
    # Gap 2: Between rect2 and rect3
    gap2_start = rect2_end
    gap2_end = gap2_start + gap_size
    
    # Rectangle 3: Right side (goes to the end)
    rect3_start = gap2_end
    rect3_end = WIDTH
    
    walls_segments = []
    
    # Create left rectangle
    if rect1_end > rect1_start:
        left_rect = {
            'x': rect1_start,
            'y': -50,  # Start above screen
            'width': rect1_end - rect1_start,
            'height': 50
        }
        walls_segments.append(left_rect)
    
    # Create middle rectangle
    if rect2_end > rect2_start:
        middle_rect = {
            'x': rect2_start,
            'y': -50,  # Start above screen
            'width': rect2_end - rect2_start,
            'height': 50
        }
        walls_segments.append(middle_rect)
    
    # Create right rectangle
    if rect3_end > rect3_start:
        right_rect = {
            'x': rect3_start,
            'y': -50,  # Start above screen
            'width': rect3_end - rect3_start,
            'height': 50
        }
        walls_segments.append(right_rect)
        
    # create rectangle for first gap
    if gap1_end > gap1_start:
        gap1_rect = {
            'x': gap1_start,
            'y': -50,
            'width': gap_size,
            'height': 25,
        }
        gaps.append(gap1_rect)
        
    # create rectangle for second gap
    if gap2_end > gap2_start:
        gap2_rect = {
            'x': gap2_start,
            'y': -50,
            'width': gap_size,
            'height': 25
        }
        gaps.append(gap2_rect)

    # Generate a math question for this wall
    question, answer = generate_simple_math_question()
    
    # Create wall data structure with text
    wall_data = {
        'segments': walls_segments,
        'text': question,
        'answer': answer,
        'text_y': -80  # Position text above the wall initially
    }
    
    return wall_data

def update_walls():
    """Update wall positions and remove walls that are off screen"""
    global walls, gaps
    
    # Move all walls down
    for wall_data in walls:
        for wall in wall_data['segments']:
            wall['y'] += scroll_speed
        # Move the text with the wall
        wall_data['text_y'] += scroll_speed
    
    # Move all gaps down
    for gap in gaps:
        gap['y'] += scroll_speed
    
    # Remove walls that are completely off screen
    walls = [wall_data for wall_data in walls if wall_data['segments'][0]['y'] < HEIGHT + 100]
    
    # Remove gaps that are completely off screen
    gaps = [gap for gap in gaps if gap['y'] < HEIGHT + 100]

def draw_walls(surface):
    """Draw all walls on the screen"""
    for wall_data in walls:
        # Draw wall segments
        for wall in wall_data['segments']:
            if wall['width'] > 0:  # Only draw if wall has width
                pygame.draw.rect(surface, wall_color, (wall['x'], wall['y'], wall['width'], wall['height']))
                # Add a darker border for better visibility
                pygame.draw.rect(surface, (100, 50, 0), (wall['x'], wall['y'], wall['width'], wall['height']), 2)
        
        # Draw text below the wall
        if wall_data['text_y'] > -50 and wall_data['text_y'] < HEIGHT + 50:  # Only draw if visible
            font = pygame.font.Font(None, 36)
            text_surface = font.render(wall_data['text'], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(WIDTH // 2, wall_data['text_y']))
            surface.blit(text_surface, text_rect)
                
    # Draw gaps with different colors based on type
    for gap in gaps:
        if gap['width'] > 0:
            pygame.draw.rect(surface, (30, 30, 30), (gap['x'], gap['y'], gap['width'], gap['height']))
            # Add a lighter border for better visibility
            pygame.draw.rect(surface, (200, 200, 200), (gap['x'], gap['y'], gap['width'], gap['height']), 2)

def check_wall_collision(player_x, player_y, player_size):
    """Check if the player collides with any wall"""
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    
    for wall_data in walls:
        for wall in wall_data['segments']:
            if wall['width'] > 0:  # Only check collision if wall has width
                wall_rect = pygame.Rect(wall['x'], wall['y'], wall['width'], wall['height'])
                if player_rect.colliderect(wall_rect):
                    return True
    return False

def game_over():
    """Handle game over state"""
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    
    font_small = pygame.font.Font(None, 48)
    choice_text = font_small.render("Press C to Continue or Q to Quit", True, (255, 255, 255))
    choice_rect = choice_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    
    screen.blit(game_over_text, game_over_rect)
    screen.blit(choice_text, choice_rect)
    
def reset_game():
    """Reset game state to initial values"""
    global square_x, square_y, walls, gaps, bg_y1, bg_y2, wall_spawn_timer, game_state
    square_x = (WIDTH - square_size) // 2
    square_y = (HEIGHT - square_size) // 2
    walls.clear()
    gaps.clear()
    bg_y1 = 0
    bg_y2 = -HEIGHT
    wall_spawn_timer = 0
    game_state = "playing"
    
def user_choice():
    """Wait for user to choose to continue or quit"""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    waiting = False  # Continue the game
                    reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        
        # Display choice message
        screen.fill((30, 30, 30))  # Clear screen
        font = pygame.font.Font(None, 48)
        text = font.render("Press C to Continue or Q to Quit", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(FPS)
        
def generate_simple_math_question():
    # Choose two random integers
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    # Randomly choose an operation
    operation = random.choice(['+', '-', '*', '/'])
    if operation == '+':
        question = f"{a} + {b} = ?"
        answer = a + b
    elif operation == '-':
        question = f"{a} - {b} = ?"
        answer = a - b
    elif operation == '*':
        question = f"{a} * {b} = ?"
        answer = a * b
    else:  # division, ensure no division by zero and integer result
        # Make sure b divides a for integer division
        a = a * b
        question = f"{a} / {b} = ?"
        answer = a // b
    return question, answer

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif game_state == "game_over":
                if event.key == pygame.K_c:
                    reset_game()
                elif event.key == pygame.K_q:
                    running = False

    if game_state == "playing":
        # Handle continuous key presses for smooth movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            square_x -= square_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            square_x += square_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            square_y -= square_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            if square_y + square_size + square_speed <= HEIGHT:
                square_y += square_speed
            else:
                square_y = HEIGHT - square_size
        
        # Keep square within screen boundaries
        square_x = max(0, min(square_x, WIDTH - square_size))
        square_y = max(0, min(square_y, HEIGHT - square_size))
        # Game logic goes here
        
        # Wall spawning logic
        wall_spawn_timer += 1
        if wall_spawn_timer >= wall_spawn_delay:
            new_wall = create_wall()
            walls.append(new_wall)
            wall_spawn_timer = 0
        
        # Update walls
        update_walls()
        
        # Check for wall collision
        if check_wall_collision(square_x, square_y, square_size):
            game_state = "game_over"
            square_color = (255, 0, 0)  # Change to red when hitting wall
        else:
            square_color = (255, 100, 100)  # Normal color
        
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

    # Show mouse cursor position (x, y)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    font = pygame.font.Font(None, 28)
    mouse_pos_text = font.render(f"Mouse: ({mouse_x}, {mouse_y})", True, (200, 200, 0))
    screen.blit(mouse_pos_text, (WIDTH - 200, 10))
    
    # Draw scrolling background pattern
    draw_background_pattern(screen, bg_y1)
    draw_background_pattern(screen, bg_y2)

    # Draw walls
    draw_walls(screen)

    # Draw the movable square
    if game_state == "playing":
        square_color = (255, 100, 100)  # Normal color
    else:
        square_color = (255, 0, 0)  # Red when game over
    
    pygame.draw.rect(screen, square_color, (square_x, square_y, square_size, square_size))
    
    # Add a white border around the square to make it more visible
    pygame.draw.rect(screen, (255, 255, 255), (square_x, square_y, square_size, square_size), 3)
    
    # Display controls or game over message
    if game_state == "playing":
        font = pygame.font.Font(None, 36)
        controls_text = font.render("WASD or Arrow Keys to move", True, (255, 255, 255))
        screen.blit(controls_text, (10, 10))
    elif game_state == "game_over":
        game_over()
    
    pygame.display.flip()
    clock.tick(FPS)
    

pygame.quit()
sys.exit()