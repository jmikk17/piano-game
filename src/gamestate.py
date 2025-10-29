from __future__ import annotations

import sys

import pygame

import ui
from cfg import std_cfg
from game import Game
from menu import MenuManager


class GameStateManager:
    """Manages the state transitions and updates for the game.

    Todo:
        * Implement asset deloading on state transition.
        * Use layout guidelines in game and change transition screen size.
        * Add enum class in auxil for transitions and actions instead of using strings.

    """

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize the GameStateManager.

        Args:
            screen (pygame.Surface): The display surface for the game.

        """
        self.screen = screen
        self.mediator = ui.Mediator()
        self.layout = ui.UIAuxil(std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT, self.mediator)
        self.menu_manager = MenuManager(self.layout, self.mediator)
        self.current_state = "MENU"

    def update(self, dt: float) -> None:
        """Update the menu or game state based on input and elapsed time.

        Args:
            dt (float): Time passed since last frame in seconds

        """
        if self.current_state == "MENU":
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    # Using std. screen size as minimum for now
                    width = max(width, std_cfg.SCREEN_WIDTH)
                    height = max(height, std_cfg.SCREEN_HEIGHT)
                    self.screen = pygame.display.set_mode(
                        (width, height),
                        pygame.RESIZABLE,
                    )
                    self.layout.update_ui(width, height, mediate=True)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                action, data = self.menu_manager.handle_input(event)
                if action == "START_GAME":
                    self.handle_state_transition(action, data)

        elif self.current_state == "GAME":
            # In Game we need to update every frame without there being an input, so we handle quit inside
            if self.game:
                game_status = self.game.update(dt)
            if game_status == "QUIT_TO_MENU":
                self.handle_state_transition("RETURN_TO_MENU", None)

    def draw(self) -> None:
        """Draw the menu or game state to the screen."""
        if self.current_state == "MENU":
            self.menu_manager.draw(self.screen)
        elif self.current_state == "GAME" and self.game:
            self.game.draw(self.screen)

    def handle_state_transition(self, action: str, data: str | None) -> None:
        """Handle a state transition between menu and game.

        Starts a new game instance with the selected song from data when requested.
        Adjusts the screen size and layout to std. size when transitioning to game.
        Returns back to menu when requested from a game instance.

        Args:
            action (str): The action to perform ("START_GAME" or "RETURN_TO_MENU").
            data (str): The file path to the json file containing the song data

        """
        if action == "START_GAME":
            self.screen = pygame.display.set_mode((std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT))
            self.layout.update_ui(std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT, mediate=True)
            self.current_state = "GAME"
            # Instance of game starts the internal game clock, so we start a new "Game" when a song is picked
            if data:
                self.game = Game(data, self.layout)
        elif action == "RETURN_TO_MENU":
            width, height = self.screen.get_width(), self.screen.get_height()
            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            self.current_state = "MENU"
            self.game = None
