import pygame
from cfg import std_cfg
import auxil

class UILayout:
    def __init__(self, screen_width, screen_height):
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
    
    def get_instruction_pos(self, index, text_width, total_instructions):
        """Get position for an instruction text, adjusted for total number of instructions"""
        # Calculate total height of all instructions
        total_height = total_instructions * self.instructions_spacing
        # Adjust starting Y position based on total instructions
        start_y = self.instructions_y - (total_height / 2)
        return (
            std_cfg.SCREEN_WIDTH // 2 - text_width // 2,
            start_y + index * self.instructions_spacing
        )
