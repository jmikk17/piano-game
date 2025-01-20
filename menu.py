import pygame
from cfg import std_cfg
import auxil
import json
import error
import os
from abc import ABC, abstractmethod
from assets import MenuAssets
import sys

from resource_path import resource_path

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
        """Get the rectangle for a menu item at given index"""
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
            centerx=std_cfg.SCREEN_WIDTH / 2,
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

class MainMenu(BaseMenu):
    def __init__(self,assets):
        super().__init__(assets)
        self.options = ["Play", "Options", "Exit"]

    def get_items(self):
        return self.options
    
    def draw(self, screen):
        if self.assets.background:
            screen.blit(self.assets.background, (0, 0))
        else:
            screen.fill(self.layout.colors['background'])

        self.draw_title(screen, "Music Game")
        
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
        
        self.draw_instructions(screen, ["↑↓: Select", "Enter: Choose", "Esc: Quit"])
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.current_selection = (self.current_selection - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.current_selection = (self.current_selection + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                selected = self.options[self.current_selection]
                if selected == "Play":
                    return ("SHOW_SONG_SELECT", None)
                elif selected == "Options":
                    return ("SHOW_OPTIONS", None)
                elif selected == "Exit":
                    return ("QUIT", None)
            elif event.key == pygame.K_ESCAPE:
                return ("QUIT", None)
        return (None, None)

class SongSelectMenu(BaseMenu):
    def __init__(self,assets):
        super().__init__(assets)
        self.songs = []
        self.load_available_songs()
    
    def load_available_songs(self):
        song_dir = resource_path("songs/")
        if not os.path.exists(song_dir):
            error.handle_error("Songs dir not found", "fatal")

        song_files = [f for f in os.listdir(song_dir) if f.endswith(".json")] 

        for file in song_files:
            with open(os.path.join(song_dir, file)) as f:
                song_data = json.load(f)
                self.songs.append({
                    "filename": file,
                    "title": song_data.get("title", file),
                    "difficulty": song_data.get("difficulty", "Normal"),
                    "bpm": song_data.get("bpm", std_cfg.BPM)
                })
    
    def draw(self, screen):
        screen.fill(self.layout.colors['background'])
        self.draw_title(screen, "Select Song")
        
        # Calculate visible range
        visible_items = self.get_visible_item_count()
        start_idx = self.scroll_offset
        end_idx = min(start_idx + visible_items, len(self.songs))
        
        # Draw visible items
        for i in range(start_idx, end_idx):
            relative_idx = i - start_idx
            item_rect = self.layout.get_item_rect(relative_idx)
            
            if i == self.current_selection:
                pygame.draw.rect(screen, self.layout.colors['selected'], item_rect)
            
            song = self.songs[i]
            text = f"{song['title']} - {song['difficulty']} - {song['bpm']} BPM"
            color = self.layout.colors['selected_text'] if i == self.current_selection else self.layout.colors['text']
            text_surface = self.font.render(text, True, color)
            text_pos = self.layout.get_item_text_pos(item_rect)
            text_rect = text_surface.get_rect(midleft=(item_rect.left + 10, text_pos[1]))
            screen.blit(text_surface, text_rect)
        
        self.draw_scrollbar(screen)
        
        instructions = ["↑↓: Select Song", "Enter: Start", "Esc: Back"]
        if self.get_scroll_position():
            instructions.insert(1, "PgUp/PgDn: Scroll")
        self.draw_instructions(screen, instructions)

    def get_items(self):
        return self.songs
    
    def handle_input(self, event):
       if event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_PAGEUP, pygame.K_PAGEDOWN):
            self.handle_scroll(event)
        elif event.key == pygame.K_RETURN:
            if self.songs:
                return ("START_GAME", self.songs[self.current_selection]["filename"])
        elif event.key == pygame.K_ESCAPE:
            return ("SHOW_MAIN_MENU", None)
       return (None, None)

class OptionsMenu(BaseMenu):
    def __init__(self,assets):
        super().__init__(assets)
        self.keybinds = self.load_keybinds()
        self.options = list(self.keybinds.keys())
        self.waiting_for_key = False
        self.selected_option = None
        
    def load_keybinds(self):
        default_keybinds = {
            "Pitch ↑": pygame.K_UP,
            "Pitch ↓": pygame.K_DOWN,
            "C": pygame.K_a,
            "C": pygame.K_a,
            "D": pygame.K_s,
            "E": pygame.K_d,
            "F": pygame.K_f,
            "G": pygame.K_g,
            "A": pygame.K_h,
            "H": pygame.K_j,
        }
        
        try:
            if os.path.exists(resource_path("keybinds.json")):
                with open(resource_path("keybinds.json"), "r") as f:
                    return json.load(f)
        except:
            pass
        return default_keybinds
    
    def save_keybinds(self):
        with open(resource_path("keybinds.json"), "w") as f:
            json.dump(self.keybinds, f)
    
    def get_items(self):
        return self.options
    
    def draw(self, screen):
        screen.fill(self.layout.colors['background'])
        self.draw_title(screen, "Options - Keybinds")
        
        # Calculate visible range
        visible_items = self.get_visible_item_count()
        start_idx = self.scroll_offset
        end_idx = min(start_idx + visible_items, len(self.options))
        
        # Draw visible items
        for i in range(start_idx, end_idx):
            # Calculate position relative to scroll
            relative_idx = i - start_idx
            item_rect = self.layout.get_item_rect(relative_idx)
            
            # Draw selection background
            if i == self.current_selection:
                pygame.draw.rect(screen, self.layout.colors['selected'], item_rect)
            
            # Get key name
            key_name = pygame.key.name(self.keybinds[self.options[i]])
            
            # If we're waiting for a key and this is the selected option
            if self.waiting_for_key and i == self.current_selection:
                text = f"{self.options[i]}: Press any key..."
            else:
                text = f"{self.options[i]}: {key_name}"
            
            color = self.layout.colors['selected_text'] if i == self.current_selection else self.layout.colors['text']
            text_surface = self.font.render(text, True, color)
            text_pos = self.layout.get_item_text_pos(item_rect)
            text_rect = text_surface.get_rect(midleft=(item_rect.left + 10, text_pos[1]))
            screen.blit(text_surface, text_rect)
        
        self.draw_scrollbar(screen)
        
        if self.waiting_for_key:
            instructions = ["Press any key to bind", "Esc: Cancel"]
        else:
            instructions = ["↑↓: Select", "Enter: Rebind", "Esc: Back", "S: Save"]
            if self.get_scroll_position:  # Add scrolling instruction if scrollbar is present
                instructions.insert(1, "PgUp/PgDn: Scroll")
        
        self.draw_instructions(screen, instructions)
    
    def handle_input(self, event):
        if self.waiting_for_key:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.waiting_for_key = False
                else:
                    # Assign the new key
                    self.keybinds[self.options[self.current_selection]] = event.key
                    self.waiting_for_key = False
            return (None, None)
            
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_PAGEUP, pygame.K_PAGEDOWN):
                self.handle_scroll(event)
            elif event.key == pygame.K_RETURN:
                self.waiting_for_key = True
            elif event.key == pygame.K_s:
                self.save_keybinds()
            elif event.key == pygame.K_ESCAPE:
                return ("SHOW_MAIN_MENU", None) 
        return (None, None)

class MenuManager:
    def __init__(self):
        """
        Class that controls menus. Handles swapping (internally), input from player and drawing to screen (through specific menu class)
        ----------
        Attributes:
        current_menu : menu object (child of BaseMenu)
            currently selected menu
        ----------
        Methods:
        TODO
        """
        # When menu is first created we must load assets
        self.menu_assets = MenuAssets()
        self.menu_assets.load()

        # Instansiate the three different menus
        self.menus = {
            "main": MainMenu(self.menu_assets),
            "song_select": SongSelectMenu(self.menu_assets),
            "options": OptionsMenu(self.menu_assets)
        }

        # Initilize to main menu when menu manager is first instansiated
        self.show_menu("main")
    
    def show_menu(self, menu_name):
        """Change reference of current_menu to a specified menu"""
        self.current_menu = self.menus[menu_name]
    
    def draw(self, screen):
        """Draw the menu through its own drawing function"""
        if self.current_menu:
            self.current_menu.draw(screen)
    
    def handle_input(self, event):
        """Handle input through the menus own function"""
        # Returns action, data as "START_GAME",song_name if a song is selected, which indicates we need a state swap
        # Also handles quit and menu swap if requested
        if self.current_menu:
            action, data = self.current_menu.handle_input(event)
            if action:
                if action == "START_GAME":
                    return action, data
                elif action == "SHOW_MAIN_MENU":
                    self.show_menu("main")
                elif action == "SHOW_SONG_SELECT":
                    self.show_menu("song_select")
                elif action == "SHOW_OPTIONS":
                    self.show_menu("options")
                elif action == "QUIT":
                    pygame.quit()
                    sys.exit()
        return (None,None)
    
    def cleanup_menu_assets(self):
        """Cleanup menu assets when transitioning to game"""
        if self.menu_assets:  
            # Check if assets exist before unloading
            self.menu_assets.unload()
            self.menu_assets = None
            self.current_menu = None
            self.menus = {}
 
    
    def reinitialize_menus(self):
        """Reinitialize menus when returning from game"""
        if self.menu_assets is None:
            self.menu_assets = MenuAssets()
            self.menu_assets.load()
            
            self.menus = {
                "main": MainMenu(self.menu_assets),
                "song_select": SongSelectMenu(self.menu_assets),
                "options": OptionsMenu(self.menu_assets)
            }
            self.show_menu("main")
    
    def __del__(self):
        # Custom destructor, called when all references to MenuManager is destroyed
        """Make sure that assets are not still in memory when MenuManager is destroyed"""
        if self.menu_assets is not None:
            self.cleanup_menu_assets()
            self.menu_assets = None
