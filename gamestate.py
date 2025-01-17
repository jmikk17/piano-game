import pygame
from cfg import std_cfg
from menu import MenuManager
from game import Game

### TODO need to implement game before cleanup and reinitialize can be tested!
# Structure of cleanup might be problematic if we dont load a frame of e.g. game before cleaning menu assets
# Unless we always load with an "if asset:" statement, then we would just get a blank screen for 1 frame
class GameStateManager:
    def __init__(self):
        self.menu_manager = MenuManager()
        self.current_state = "MENU"

    def handle_state_transition(self, action, data):
        if action == "START_GAME":
            # Transition from menu to game
            self.current_state = "GAME"
            self.game = Game(data) #game instance here, use data to start song
            self.menu_manager.cleanup_menu_assets()
        elif action == "RETURN_TO_MENU":
            # Transition from game to menu
            self.current_state = "MENU"
            self.menu_manager.reinitialize_menus()
            self.game = None
            # self.game cleanup!
    
    def update(self,dt):
        if self.current_state == "MENU":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                action, data = self.menu_manager.handle_input(event)
                if action:
                    if action == "START_GAME":
                        self.handle_state_transition(action, data)
            
        elif self.current_state == "GAME":
        # In Game we might need to update without there being an input, so we handle quit inside
            game_status = self.game.update(dt)
            if game_status == "QUIT_TO_MENU":
                self.handle_state_transition("RETURN_TO_MENU", None)
    
    def draw(self,screen):
        if self.current_state == "MENU":
            self.menu_manager.draw(screen)
        elif self.current_state == "GAME":
            self.game.draw(screen)
