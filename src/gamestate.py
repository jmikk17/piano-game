import sys

import pygame

import ui
from cfg import std_cfg
from game import Game
from menu import MenuManager

# TODO(jmikk): integrate with asset loading/deloading


class GameStateManager:
    """Manages the state transitions and updates for the game.

    Attributes:
        screen (pygame.Surface): The display surface for the game.
        mediator (ui.Mediator): Mediator for UI interactions.
        layout (ui.UIAuxil): Layout manager for UI components.
        menu_manager (MenuManager): Manager for handling menu interactions.
        current_state (str): The current state of the game ("MENU" or "GAME").
        game (Game, optional): Instance of the game, initialized when transitioning to the game state.

    Methods:
        update(dt: float) -> None:
            Updates the current state based on user input and elapsed time.
        draw() -> None:
            Draws the current state to the screen.
        handle_state_transition(action: str, data: Any) -> None:
            Handles transitions between different game states.

    """

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.mediator = ui.Mediator()
        self.layout = ui.UIAuxil(std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT, self.mediator)
        self.menu_manager = MenuManager(self.layout, self.mediator)
        self.current_state = "MENU"

    def update(self, dt: float) -> None:
        if self.current_state == "MENU":
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    # using std. size as minimum for now
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
            game_status = self.game.update(dt)
            if game_status == "QUIT_TO_MENU":
                self.handle_state_transition("RETURN_TO_MENU", None)

    def draw(self) -> None:
        if self.current_state == "MENU":
            self.menu_manager.draw(self.screen)
        elif self.current_state == "GAME":
            self.game.draw(self.screen)

    def handle_state_transition(self, action, data) -> None:
        if action == "START_GAME":
            # Transition from menu to game
            # TODO(jmikk) For now we force default size in game, since some of the layout is defined in absolute terms,
            # can in later version be changed to size from menu as:
            # width,height = self.screen.get_width(), self.screen.get_height()
            # self.screen = pygame.display.set_mode((width, height))
            self.screen = pygame.display.set_mode((std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT))
            self.layout.update_ui(std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT, mediate=True)
            self.current_state = "GAME"
            # Instance of game starts the internal clock,
            # so we start a new "Game" when a song is picked
            self.game = Game(data, self.layout)
        elif action == "RETURN_TO_MENU":
            # Transition from game to menu
            width, height = self.screen.get_width(), self.screen.get_height()
            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            self.current_state = "MENU"
            self.game = None
