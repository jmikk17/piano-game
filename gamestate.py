import sys

import pygame

import ui
from cfg import std_cfg
from game import Game
from menu import MenuManager

# TODO integrate with asset loading/deloading


class GameStateManager:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.mediator = ui.Mediator()
        self.layout = ui.UIAuxil(
            std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT, self.mediator
        )
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
                        (width, height), pygame.RESIZABLE
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

    def draw(self):
        if self.current_state == "MENU":
            self.menu_manager.draw(self.screen)
        elif self.current_state == "GAME":
            self.game.draw(self.screen)

    def handle_state_transition(self, action, data):
        if action == "START_GAME":
            # Transition from menu to game
            # TODO For now we force default size in game, since some of the layout is defined in absolute terms,
            # can in later version be changed to size from menu as:
            # width,height = self.screen.get_width(), self.screen.get_height()
            # self.screen = pygame.display.set_mode((width, height))
            self.screen = pygame.display.set_mode(
                (std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT),
            )
            self.layout.update_ui(
                std_cfg.SCREEN_WIDTH,
                std_cfg.SCREEN_HEIGHT,
                mediate=False,
            )
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
