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
        self.current_selection = 0
        self.font = auxil.get_sysfont(std_cfg.FONT, 36)
        self.title_font = auxil.get_sysfont(std_cfg.FONT, 48)
        self.layout = UILayout(std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT)
        self.scroll_offset = 0
        self.assets = assets
    
    @abstractmethod
    def draw(self, screen):
        pass
    
    @abstractmethod
    def handle_input(self, event):
        pass
    
    def draw_title(self, screen, title):
        title_surface = self.title_font.render(title, True, self.layout.colors['text'])
        title_rect = title_surface.get_rect(
            centerx=std_cfg.SCREEN_WIDTH // 2,
            y=self.layout.title_y
        )
        screen.blit(title_surface, title_rect)
    
    def draw_instructions(self, screen, instructions):
        total_instructions = len(instructions)
        for i, instruction in enumerate(instructions):
            text_surface = self.font.render(instruction, True, self.layout.colors['instructions'])
            pos = self.layout.get_instruction_pos(i, text_surface.get_width(), total_instructions)
            screen.blit(text_surface, pos)

    def get_visible_item_count(self):
        """Calculate how many items can be displayed at once"""
        content_height = self.layout.content_end_y - self.layout.content_start_y
        return int(content_height / (self.layout.item_height + self.layout.item_padding))

    def get_scroll_position(self):
        """Calculate scrollbar position and size"""
        visible_items = self.get_visible_item_count()
        total_items = len(self.get_items()) 
        
        if total_items <= visible_items:
            return None  # No scrollbar needed
            
        # Calculate scrollbar metrics
        content_height = self.layout.content_end_y - self.layout.content_start_y
        scrollbar_height = (visible_items / total_items) * content_height
        scrollbar_pos = (self.scroll_offset / total_items) * content_height
        
        return {
            'x': self.layout.content_x + self.layout.content_width + self.layout.scrollbar_padding,
            'y': self.layout.content_start_y + scrollbar_pos,
            'width': self.layout.scrollbar_width,
            'height': scrollbar_height
        }

    def handle_scroll(self, event):
        """Handle scroll-related input events"""
        visible_items = self.get_visible_item_count()
        total_items = len(self.get_items())
        max_scroll = max(0, total_items - visible_items)
        
        if event.key == pygame.K_UP:
            if self.current_selection > 0:
                self.current_selection -= 1
                # Scroll up if selection is above visible area
                if self.current_selection < self.scroll_offset:
                    self.scroll_offset = self.current_selection
        elif event.key == pygame.K_DOWN:
            if self.current_selection < total_items - 1:
                self.current_selection += 1
                # Scroll down if selection is below visible area
                if self.current_selection >= self.scroll_offset + visible_items:
                    self.scroll_offset = min(max_scroll, self.current_selection - visible_items + 1)
        elif event.key == pygame.K_PAGEUP:
            # Scroll up by visible_items
            self.scroll_offset = max(0, self.scroll_offset - visible_items)
            # Adjust selection if it's now outside visible area
            self.current_selection = max(self.scroll_offset, self.current_selection)
        elif event.key == pygame.K_PAGEDOWN:
            # Scroll down by visible_items
            self.scroll_offset = min(max_scroll, self.scroll_offset + visible_items)
            # Adjust selection if it's now outside visible area
            self.current_selection = min(self.scroll_offset + visible_items - 1, self.current_selection)

    @abstractmethod
    def get_items(self):
        """Return the list of items to be displayed"""
        pass

    def draw_scrollbar(self, screen):
        """Draw the scrollbar if needed"""
        scroll_pos = self.get_scroll_position()
        if scroll_pos:
            pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(
                scroll_pos['x'],
                scroll_pos['y'],
                scroll_pos['width'],
                scroll_pos['height']
            ))
