import math
from grid import Grid
from game_object import Object

# Import and initialize the pygame library
import pygame
pygame.init()

def render_grid(grid: Grid, screen: pygame.Surface) -> None:
    (screen_w, screen_h) = screen.get_size()
    (grid_x, grid_y) = grid.shape()
    x = 2*grid_x + grid_y
    y = math.sqrt(3)*grid_y

    unit = min(screen_h / x, screen_w / y)
    grid_w = unit * x
    grid_h = unit * y

    bl = ((screen_w - grid_w) / 2, (screen_h + grid_h) / 2)

    # Draw diagonals
    for i in range(grid_x+1):
        x_offset = 2*i*unit
        y_offset = grid_y*unit
        pygame.draw.line(
            screen,
            (0,0,0),
            (bl[0] + x_offset, bl[1]),
            (bl[0] + x_offset + y_offset, bl[1] - math.sqrt(3)*y_offset)
        )

    # Draw horizontals
    for j in range(grid_y+1):
        x_offset = 2*grid_x*unit
        y_offset = j*unit
        pygame.draw.line(
            screen,
            (0,0,0),
            (bl[0] + y_offset, bl[1] - math.sqrt(3)*y_offset),
            (bl[0] + y_offset + x_offset, bl[1] - math.sqrt(3)*y_offset)
        )

    print("Rendered grid")


# Set up the drawing window
screen = pygame.display.set_mode([1600, 900])

# Run until the user asks to quit
running = True
grid = Grid(10,10)
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    print("Filled screen with white")

    render_grid(grid, screen)

    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
