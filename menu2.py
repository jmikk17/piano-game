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
        self.options = ["Play", "Options", "Exit"]

        self.scaled_background = None

        self.buttons = []
        button_y = self.layout.content_start_y
        for i,name in enumerate(self.options):
            self.buttons.append(ui.Button(self.layout.x_center,button_y,
                                          self.layout.colors['text'],self.layout.colors['selected'],name))
            button_y = self.buttons[i].rect.bottom + self.layout.pad_y

    def draw(self, screen):
        if self.scaled_background:
            screen.blit(self.scaled_background, (0, 0))
        elif self.assets.background:
            screen.blit(self.assets.background, (0, 0))
        else:
            screen.fill(self.layout.colors['background'])

        self.draw_title(screen, self.layout.x_center, self.layout.title_y,"Piano game")

        for button in self.buttons:
            button.draw(screen, auxil.RED)
        
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.isOver(pos):
                    # return button.text to menumanager here
                    if button.text == "Exit":
                        pygame.quit()
                        sys.exit()
                    else: 
                        print(button.text)

    def handle_ui_event(self, ui):
        # Get new scaled ui guides
        self.layout = ui 

        # Update buttons
        button_y = self.layout.content_start_y
        for i,button in enumerate(self.buttons):
            button.update(self.layout.x_center, button_y)
            button_y = self.buttons[i].rect.bottom + self.layout.pad_y

        # Scale background
        self.scaled_background = pygame.transform.scale(self.assets.background, (self.layout.x_unit*100, self.layout.y_unit*100))
        
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
            menu.handle_input(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
