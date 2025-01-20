import pygame
from cfg import std_cfg
import auxil

class UILayout:
    def __init__(self, screen_width, screen_height):
        # Maybe wrap all of this in an update function, which can be called on screen-resize?
        # Base unit for scaling (1% of screen height)
        self.unit = screen_height * 0.01
        
        # Calculate positions relative to screen size
        self.title_y = screen_height * 0.1  # 10% from top
        self.content_start_y = screen_height * 0.25  # 25% from top
        self.content_end_y = screen_height * 0.8  # 80% from top (where content area ends)
        
        # Item sizing (relative to screen height)
        self.item_height = self.unit * 7  # 7% of screen height
        self.item_padding = self.unit * 1.5  # 1.5% of screen height
        
        # Width calculations
        self.content_width = screen_width * 0.8  # 80% of screen width
        self.content_x = screen_width * 0.1  # 10% from left
        
        # Instructions positioning
        self.instructions_y = screen_height * 0.85  # 85% from top
        self.instructions_spacing = self.unit * 4  # 4% of screen height
        
        # Scrollbar
        self.scrollbar_width = self.unit * 2  # 2% of screen height
        self.scrollbar_padding = self.unit  # 1% of screen height
        
        # Common colors
        self.colors = {
            'background': auxil.WHITE,
            'selected': (200, 200, 255),
            'text': auxil.BLACK,
            'selected_text': auxil.BLUE,
            'instructions': (100, 100, 100)
        }
    
    def get_item_rect(self, index):
        """Get the rectangle for a menu item at given index in list"""
        y = self.content_start_y + (self.item_height + self.item_padding) * index
        return pygame.Rect(
            self.content_x,
            y,
            self.content_width,
            self.item_height
        )
    
    def get_item_text_pos(self, item_rect):
        """Get the centered position for text within an item rectangle"""
        return (
            item_rect.centerx,
            item_rect.centery
        )
    
class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)