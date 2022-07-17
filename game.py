import math
import os
import json
from typing import List
from functools import partial
from pygame_button import Button

from level_ui import LevelUI
from styles import BUTTON_STYLE, WHITE, GREY, RED

# Import and initialize the pygame library
import pygame
pygame.init()

class Game:
    screen: pygame.Surface
    levels: dict
    buttons: List[Button]

    running: bool
    paused: bool
    state: str

    level_ui: LevelUI

    def __init__(self):
        pygame.init()

        # Set up the drawing window
        self.screen = pygame.display.set_mode([1600, 900])
        #self.screen.set_caption('Thunder Bolt')
        self.level_ui = LevelUI(self.screen)

        # Load all the levels
        self.load_levels()

        self.paused = False
        self.state = "menu"

        # Render the menu
        self.render_menu()

    # Load all levels from the 'levels' directory
    def load_levels(self) -> None:
        self.levels = dict()
        level_dir = os.path.join(os.getcwd(), 'levels')
        for filename in os.listdir(level_dir):
            if filename.endswith('.json'):
                f = open(os.path.join(level_dir, filename))
                l = json.load(f)
                self.levels[l["name"]] = l
                f.close()

    # Clear the screen and buttons
    def clear_screen(self) -> None:
        self.screen.fill(WHITE)
        self.buttons = []

    # Render a given level
    def render_level(self, level_name: str) -> None:
        self.clear_screen()
        self.state = level_name

        level_spec = self.levels[level_name]

        self.level_ui.load_level_spec(level_spec)

    # Render the menu
    def render_menu(self) -> None:
        self.clear_screen()
        self.state = "menu"

        # Make a button for each level
        for level_name in self.levels:
            self.buttons.append(Button(
                (500, 200 + 50*self.levels[level_name]["level"], 600, 50),
                GREY,
                partial(self.render_level, level_name),
                text=level_name,
                **BUTTON_STYLE
            ))

    # Quit
    def quit(self) -> None:
        self.running = False

    # Unpause
    def unpause(self) -> None:
        self.paused = False
        if self.state == "menu":
            self.render_menu()
        elif self.state in self.levels:
            self.render_level(self.state)

    # Render pause screen
    def render_pause(self) -> None:
        self.clear_screen()
        self.paused = True

        self.buttons.append(Button(
            (500, 300, 600, 50),
            GREY,
            self.unpause,
            text="Unpause",
            **BUTTON_STYLE
        ))
        self.buttons.append(Button(
            (500, 350, 600, 50),
            GREY,
            self.render_menu,
            text="Quit to main menu",
            **BUTTON_STYLE
        ))
        self.buttons.append(Button(
            (500, 400, 600, 50),
            RED,
            self.quit,
            text="Quit",
            **BUTTON_STYLE
        ))


    def run(self) -> None:
        # Run until the user asks to quit
        self.running = True
        while self.running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not self.paused:
                            self.render_pause()
                        else:
                            self.unpause()
                    if self.state in self.levels and not self.paused:
                        if event.key == pygame.K_u:
                            self.level_ui.grid.undo()
                        elif event.key == pygame.K_r:
                            self.level_ui.grid.reset()

                if event.type == pygame.MOUSEBUTTONDOWN and self.state in self.levels and not self.paused:
                    self.level_ui.handle_click(pygame.mouse.get_pos())

                for b in self.buttons:
                    b.check_event(event)

            for b in self.buttons:
                b.update(self.screen)

            if self.state in self.levels and not self.paused:
                self.clear_screen()
                self.level_ui.render_all(pygame.mouse.get_pos())

            # Display the screen
            pygame.display.update()

        # Done! Time to quit.
        pygame.quit()

Game().run()