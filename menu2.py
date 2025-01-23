### Second attempt on some cleaner menu code
### Currently not called by anything
import pygame
from cfg import std_cfg
import auxil
import json
import error
import os
from abc import ABC, abstractmethod
from assets import MenuAssets
import sys
from ui import UILayout, Button

class BaseMenu(ABC):
    def __init__(self,assets):
        self.font = auxil.get_sysfont(std_cfg.FONT, 36)
        self.title_font = auxil.get_sysfont(std_cfg.FONT, 48)
        # TODO should be changed so all children refer to same ui guidelines, so we only need to update one
        self.layout = UILayout(std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT)
        self.assets = assets
        self.buttons = []
    
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
    
    def draw_title(self, screen, title):
        """Draws title of selected menu"""
        # Can be made abstract later if we need different titles
        title_surface = self.title_font.render(title, True, self.layout.colors['title'])
        title_rect = title_surface.get_rect(
            centerx=std_cfg.SCREEN_WIDTH / 2,
            y=self.layout.title_y
        )
        screen.blit(title_surface, title_rect)

class MainMenu(BaseMenu):
    def __init__(self, assets):
        super().__init__(assets)
        #self.options = ["Play", "Options", "Exit"]
        self.options = ["Play"]
        for i,name in enumerate(self.options):
            if i == 0:
                self.buttons.append(Button(self.layout.x_center,self.layout.content_start_y,name))
                new_y = self.buttons[i].rect.bottomy + self.layout.
            else:
                pass
            #TODO problematic we use y as center of button when we dont know the size of the button

    def draw(self, screen):
        if self.assets.background:
            screen.blit(self.assets.background, (0, 0))
        else:
            screen.fill(self.layout.colors['background'])

        super().draw_title(screen, "Piano game")

        for button in self.buttons:
            button.draw(screen, auxil.RED)
        
    def handle_input(self, event):
        return super().handle_input(event)
        
def main():
    pygame.init()
    screen = pygame.display.set_mode((std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT),pygame.RESIZABLE)
    menu_assets = MenuAssets()
    menu_assets.load()
    menu = MainMenu(menu_assets)
    while True:
        menu.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
        pygame.display.flip()

if __name__ == "__main__":
    main()
