import pygame
import sys
import math
import random

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

# Wall variables
walls = []  # List to store wall objects
wall_width = 80
wall_spawn_timer = 0
wall_spawn_delay = 180  # Spawn a wall every 3 seconds at 60 FPS
wall_color = (150, 75, 0)  # Brown color for walls

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
    """Create a new wall with a gap for the player to pass through"""
    gap_size = 150  # Size of the gap
    gap_position = random.randint(gap_size, WIDTH - gap_size)  # Random gap position
    
    # Create left wall segment
    left_wall = {
        'x': 0,
        'y': -50,  # Start above screen
        'width': gap_position - gap_size // 2,
        'height': 50
    }
    
    # Create right wall segment
    right_wall = {
        'x': gap_position + gap_size // 2,
        'y': -50,  # Start above screen
        'width': WIDTH - (gap_position + gap_size // 2),
        'height': 50
    }
    
    return [left_wall, right_wall]

def update_walls():
    """Update wall positions and remove walls that are off screen"""
    global walls
    
    # Move all walls down
    for wall_pair in walls:
        for wall in wall_pair:
            wall['y'] += scroll_speed
    
    # Remove walls that are completely off screen
    walls = [wall_pair for wall_pair in walls if wall_pair[0]['y'] < HEIGHT + 100]

def draw_walls(surface):
    """Draw all walls on the screen"""
    for wall_pair in walls:
        for wall in wall_pair:
            if wall['width'] > 0:  # Only draw if wall has width
                pygame.draw.rect(surface, wall_color, (wall['x'], wall['y'], wall['width'], wall['height']))
                # Add a darker border for better visibility
                pygame.draw.rect(surface, (100, 50, 0), (wall['x'], wall['y'], wall['width'], wall['height']), 2)

def check_wall_collision(player_x, player_y, player_size):
    """Check if the player collides with any wall"""
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    
    for wall_pair in walls:
        for wall in wall_pair:
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
    global square_x, square_y, walls, bg_y1, bg_y2, wall_spawn_timer, game_state
    square_x = (WIDTH - square_size) // 2
    square_y = (HEIGHT - square_size) // 2
    walls.clear()
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
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            square_y += square_speed
        
        # Keep square within screen boundaries
        square_x = max(0, min(square_x, WIDTH - square_size))
        square_y = max(0, min(square_y, HEIGHT - square_size))

        # Game logic goes here
        
        # Wall spawning logic
        wall_spawn_timer += 1
        if wall_spawn_timer >= wall_spawn_delay:
            walls.append(create_wall())
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