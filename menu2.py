### Second attempt on some cleaner menu code
### Currently not called by anything, tested by run as main
import pygame
from cfg import std_cfg
import auxil
import json
import error
import os
from abc import ABC, abstractmethod
from assets import MenuAssets
import sys
#from ui import UILayout, Button
import ui

class BaseMenu(ABC):
    def __init__(self,assets,layout,mediator):
        self.font = auxil.get_sysfont(std_cfg.FONT, 36)
        self.title_font = auxil.get_sysfont(std_cfg.FONT, 48)
        # TODO should be changed so all children refer to same ui guidelines, so we only need to update one
        #self.layout = UILayout(std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT)
        self.layout = layout 
        self.assets = assets
        self.buttons = []
        self.mediator = mediator
    
    @abstractmethod
    def draw(self, screen):
        pass
    
    @abstractmethod
    def handle_input(self, event):
        pass

#   @abstractmethod
#   def get_items(self):
#       """Return the list of items to be displayed"""
#       pass
    
    def draw_title(self, screen, x_pos, y_pos, title):
        """Draws title of selected menu"""
        # Can be made abstract later if we need different titles
        title_surface = self.title_font.render(title, True, self.layout.colors['title'])
        title_rect = title_surface.get_rect(
            centerx=x_pos,
            y=y_pos
        )
        screen.blit(title_surface, title_rect)

class MainMenu(BaseMenu):
    def __init__(self, assets, layout, mediator):
        super().__init__(assets, layout, mediator)
        mediator.set_menu(self)
        #self.options = ["Play", "Options", "Exit"]
        self.options = ["Play"]
        for i,name in enumerate(self.options):
            if i == 0:
                self.buttons.append(ui.Button(self.layout.x_center,self.layout.content_start_y,name))
                #new_y = self.buttons[i].rect.bottomy + self.layout.
            else:
                pass
            #TODO problematic we use y as center of button when we dont know the size of the button

    def draw(self, screen):
        if self.assets.background:
            screen.blit(self.assets.background, (0, 0))
        else:
            screen.fill(self.layout.colors['background'])

        self.draw_title(screen, self.layout.x_center, self.layout.title_y,"Piano game")

        for button in self.buttons:
            button.draw(screen, auxil.RED)
        
    def handle_input(self, event):
        return super().handle_input(event)

    def handle_ui_event(self, ui):
        self.layout = ui 
        # TODO update buttons here
        
def main():
    pygame.init()
    screen = pygame.display.set_mode((std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT),pygame.RESIZABLE)
    mediator = ui.Mediator()
    # UI called should be changed to get screen size when returning to menu from game
    layout = ui.UIAuxil(std_cfg.SCREEN_WIDTH,std_cfg.SCREEN_HEIGHT,mediator)
    menu_assets = MenuAssets()
    menu_assets.load()
    menu = MainMenu(menu_assets,layout,mediator)
    while True:
        menu.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                layout.update_ui(width,height,True)
            
        pygame.display.flip()

# TODO extend to MenuManager
#   create mediator with manager instead, 
#   and have the manager "handle_ui_event" call a menu function like the current handle_ui event.
#   Or maybe create the mediator inside menumanager? And then make the notifier call all 3 menu updates?

if __name__ == "__main__":
    main()
