import pygame
from cfg import std_cfg
import auxil

class UILayout:
    def __init__(self, screen_width, screen_height):
        self.colors = {
            'background': auxil.WHITE,
            'selected': (200, 200, 255),
            'text': auxil.BLACK,
            'selected_text': auxil.BLUE,
            'instructions': (100, 100, 100)
        }

        self.update_ui(screen_width, screen_height)

    def update_ui(self, screen_width, screen_height):
        self.y_unit = screen_height * 0.01
        self.x_unit = screen_width * 0.01

        self.x_center = screen_width / 2
        self.y_center = screen_height / 2

        self.title_y = self.y_unit * 10 
        self.content_start_y = self.y_unit * 25
        self.content_end_y = self.y_unit * 80
    
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
    def __init__(self, x, y, width, height, text='', font=std_cfg.FONT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = auxil.get_sysfont(font, 36)

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, outline=None):
        # outline is color of outline
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
