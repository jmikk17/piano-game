import pygame
from cfg import std_cfg
from menu import MenuManager
from game import Game
import sys
import ui

# TODO integrate with asset loading/deloading

class GameStateManager:
    def __init__(self,screen):
        self.screen = screen
        self.mediator = ui.Mediator()
        self.layout = ui.UIAuxil(std_cfg.SCREEN_WIDTH,std_cfg.SCREEN_HEIGHT,self.mediator)
        self.menu_manager = MenuManager(self.layout,self.mediator)
        self.current_state = "MENU"

    def update(self,dt):
        if self.current_state == "MENU":
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    # using std. size as minimum for now
                    if width < std_cfg.SCREEN_WIDTH:
                        width = std_cfg.SCREEN_WIDTH
                    if height < std_cfg.SCREEN_HEIGHT:
                        height = std_cfg.SCREEN_HEIGHT
                    self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    self.layout.update_ui(width,height,True)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                action, data = self.menu_manager.handle_input(event)
                if action == "START_GAME":
                    self.handle_state_transition(action, data)
            
        elif self.current_state == "GAME":
        # In Game we need to update without there being an input, so we handle quit inside
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
            width,height = self.screen.get_width(), self.screen.get_height()
            self.screen = pygame.display.set_mode((width, height))
            self.current_state = "GAME"
            # Instance of game starts the internal clock, so we start a new "Game" when a song is picked
            self.game = Game(data,self.layout) 
            self.mediator.set_manager(self.game)
        elif action == "RETURN_TO_MENU":
            # Transition from game to menu
            width,height = self.screen.get_width(), self.screen.get_height()
            self.screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
            self.current_state = "MENU"
            self.mediator.set_manager(self.menu_manager)
            self.game = None
