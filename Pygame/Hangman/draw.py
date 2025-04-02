import math
import pygame
from math import pi

# Initialize pygame
pygame.init()

# Set the height and width of the screen
size = [400, 300]
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("arial", 25)

pygame.display.set_caption("Example code for the draw module")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()



while not done:
    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        
    # Clear the screen and set the screen background
    screen.fill("white")

    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    cursor_text = font.render(f"Cursor: {mouse_x}, {mouse_y}", True, (255, 0, 0))
    screen.blit(cursor_text, (mouse_x+10, mouse_y+10))
    
    for i in range(0, 360, 45):  # Loop through angles in 45-degree increments
        angle = i
        # Convert degrees to radians
        radians = angle * (pi / 180)
        
        # Calculate the new position of the text
        # center + radius * cos or sin
        x = 200 + 50 * math.cos(radians)
        y = 150 + 50 * math.sin(radians)
        
        # Render the text at the new position
        text_surface = font.render(f"{angle}°", True, (255, 0, 0))
        if angle > 90 and angle <= 270:
            adjusted_angle = angle - 180  # Flip the text
        else:
            adjusted_angle = angle
        rotated_text = pygame.transform.rotate(text_surface, -adjusted_angle)  # Rotate text to match angle
        text_rect = rotated_text.get_rect(center=(x, y))  # Center the text at the calculated position
        screen.blit(rotated_text, text_rect)
    

    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
