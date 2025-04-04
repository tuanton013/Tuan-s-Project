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

    cursor_text = font.render(
        f"Cursor: {mouse_x}, {mouse_y}", True, (255, 0, 0))
    screen.blit(cursor_text, (mouse_x+10, mouse_y+10))

    # draw an triangle
    pygame.draw.polygon(screen, (0, 255, 0), [
        (150, 50), (150, 100), (200, 50)], 5)

    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
