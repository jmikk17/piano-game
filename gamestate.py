import pygame
from cfg import std_cfg
from menu import MenuManager
from game import Game
import sys
import ui

### TODO need to implement game before cleanup and reinitialize can be tested!
# Structure of cleanup might be problematic if we dont load a frame of e.g. game before cleaning menu assets
# Unless we always load with an "if asset:" statement, then we would just get a blank screen for 1 frame
class GameStateManager:
    def __init__(self):
        mediator = ui.Mediator()
        layout = ui.UIAuxil(std_cfg.SCREEN_WIDTH,std_cfg.SCREEN_HEIGHT,mediator)
        self.menu_manager = MenuManager(layout,mediator)
        self.current_state = "MENU"

    def update(self,dt):
        #print('Menu refs:')
        #print(sys.getrefcount(self.menu_manager))

        if self.current_state == "MENU":
            for event in pygame.event.get():
                #if event.type == pygame.VIDEORESIZE:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                action, data = self.menu_manager.handle_input(event)
                if action == "START_GAME":
                    self.handle_state_transition(action, data)
            
        elif self.current_state == "GAME":
        # In Game we need to update without there being an input, so we handle quit inside
            game_status = self.game.update(dt)
            if game_status == "QUIT_TO_MENU":
                self.handle_state_transition("RETURN_TO_MENU", None)
    
    def draw(self,screen):
        if self.current_state == "MENU":
            self.menu_manager.draw(screen)
        elif self.current_state == "GAME":
            self.game.draw(screen)

    def handle_state_transition(self, action, data):
        if action == "START_GAME":
            # Transition from menu to game
            self.current_state = "GAME"
            self.game = Game(data) #game instance here, use data to start song
            self.menu_manager.cleanup_menu_assets()
            # we have a cleanup call in the destructor, so we could just set it to none and then it would be handled?
            #self.menu_manager = None
        elif action == "RETURN_TO_MENU":
            # Transition from game to menu
            self.current_state = "MENU"
            self.menu_manager.reinitialize_menus()
            self.game = None
            # self.game cleanup!
