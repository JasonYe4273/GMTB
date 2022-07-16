import math
from grid import Grid
from game_object import Object

# Import and initialize the pygame library
import pygame
pygame.init()


# Set up the drawing window
screen = pygame.display.set_mode([1600, 900])

# Fill the background with white
screen.fill((255, 255, 255))

# Initialize and render grid
grid = Grid(5,5)
grid.render_all(screen)

# Run until the user asks to quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display the screen
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
