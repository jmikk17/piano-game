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
from ui import UILayout

class BaseMenu(ABC):
    def __init__(self,assets):
        self.font = auxil.get_sysfont(std_cfg.FONT, 36)
        self.title_font = auxil.get_sysfont(std_cfg.FONT, 48)
        self.layout = UILayout(std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT)
        self.assets = assets
    
    @abstractmethod
    def draw(self, screen):
        pass
    
    @abstractmethod
    def handle_input(self, event):
        pass

    @abstractmethod
    def get_items(self):
        """Return the list of items to be displayed"""
        pass
    
    def draw_title(self, screen, title):
        """Draws title of selected menu"""
        # Can be made abstract later if we need different titles
        title_surface = self.title_font.render(title, True, self.layout.colors['text'])
        title_rect = title_surface.get_rect(
            centerx=std_cfg.SCREEN_WIDTH / 2,
            y=self.layout.title_y
        )
        screen.blit(title_surface, title_rect)

class MainMenu(BaseMenu):
    def __init__(self, assets):
        super().__init__(assets)
        self.options = ["Play", "Options", "Exit"]

    def draw(self, screen):
        if self.assets.background:
            screen.blit(self.assets.background, (0, 0))
        else:
            screen.fill(self.layout.colors['background'])

        self.draw_title(screen, "Piano game")
        
        for i, option in enumerate(self.options):
            item_rect = self.layout.get_item_rect(i)
            
            # Draw selection background
            if i == self.current_selection:
                pygame.draw.rect(screen, self.layout.colors['selected'], item_rect)
            
            # Draw text
            color = self.layout.colors['selected_text'] if i == self.current_selection else self.layout.colors['text']
            text_surface = self.font.render(option, True, color)
            text_pos = self.layout.get_item_text_pos(item_rect)
            text_rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, text_rect)
        