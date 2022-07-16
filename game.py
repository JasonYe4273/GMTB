import math
from grid import Grid
from game_object import Object

# Import and initialize the pygame library
import pygame
pygame.init()

# Renders the grid and returns the unit length (half of a triangle side)
def render_grid(grid: Grid, screen: pygame.Surface) -> float:
    MARGIN = 200

    (screen_w, screen_h) = screen.get_size()
    (adj_w, adj_h) = (screen_w - MARGIN, screen_h - MARGIN)
    (grid_x, grid_y) = grid.shape()
    x = 2*grid_x + grid_y
    y = math.sqrt(3)*grid_y

    unit = min(adj_w / x, adj_h / y)
    grid_w = unit * x
    grid_h = unit * y

    print((adj_w, adj_h))
    print((grid_x, grid_y))
    print((x, y))
    print((grid_w, grid_h))

    bl = ((screen_w - grid_w) / 2, (screen_h + grid_h) / 2)

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

    # Draw long diagonals
    for i in range(grid_x+1):
        x_offset = 2*i*unit
        y_offset = grid_y*unit
        pygame.draw.line(
            screen,
            (0,0,0),
            (bl[0] + x_offset, bl[1]),
            (bl[0] + x_offset + y_offset, bl[1] - math.sqrt(3)*y_offset)
        )

    # Draw first half of cross diagonals
    for i in range(grid_x):
        offset = i*unit
        pygame.draw.line(
            screen,
            (0,0,0),
            (bl[0] + 2*offset, bl[1]),
            (bl[0] + offset, bl[1] - math.sqrt(3)*offset),
        )

    for i in range(grid_y):
        br = (bl[0] + 2*grid_x*unit, bl[1])
        tl = (bl[0] + grid_y*unit, bl[1] - math.sqrt(3)*grid_y*unit)

        offset = i*unit
        pygame.draw.line(
            screen,
            (0,0,0),
            (br[0] + offset, br[1] - math.sqrt(3)*offset),
            (tl[0] + 2*offset, tl[1]),
        )

    return unit


# Set up the drawing window
screen = pygame.display.set_mode([1600, 900])

# Run until the user asks to quit
running = True
grid = Grid(5,5)
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    unit = render_grid(grid, screen)

    # Display the screen
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
