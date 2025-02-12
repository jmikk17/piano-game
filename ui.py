import pygame
from cfg import std_cfg
import auxil

class Mediator:
    def __init__(self):
        self.manager = None
        self.ui = None

    def set_manager(self,manager):
        self.manager = manager

    def set_ui(self,ui):
        self.ui = ui 

    def notify(self,ui):
        if self.manager:
            self.manager.update_manager_ui(ui)

class UIAuxil:
    def __init__(self, screen_width, screen_height, mediator):
        self.mediator = mediator
        mediator.set_ui(self)

        self.colors = {
            'background': auxil.WHITE,
            'selected': auxil.RED,
            'text': auxil.BLACK,
            'title': auxil.BLUE,
            'selected_text': auxil.BLUE,
            'instructions': (100, 100, 100)
        }

        # Set attributes, but dont mediate on construction 
        self.update_ui(screen_width, screen_height, False)

    def update_ui(self, screen_width, screen_height, mediate):
        self.y_unit = screen_height * 0.01
        self.x_unit = screen_width * 0.01

        self.x_center = screen_width / 2
        self.y_center = screen_height / 2

        self.title_y = self.y_unit * 10 
        self.content_start_y = self.y_unit * 25
        self.content_end_y = self.y_unit * 80

        self.pad_y = self.y_unit * 5

        if mediate:
            self.mediator.notify(self)
    
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
    def __init__(self, cen_x, y, color, hover_color, text='', font=std_cfg.FONT):
        self.cen_x = cen_x
        self.y = y
        self.text = text
        self.font = auxil.get_sysfont(font, 36)
        
        self.color = color
        self.hover_color = hover_color

        self.surface = self.font.render(self.text, True, self.color)
        self.hover_surface = self.font.render(self.text, True, self.hover_color)
        self.rect = self.surface.get_rect(
            centerx = self.cen_x,
            y = self.y
        )

    def update(self, new_cen_x, new_y):
        self.cen_x = new_cen_x
        self.y = new_y
        self.rect = self.surface.get_rect(
            centerx = self.cen_x,
            y = self.y
        )

    def draw(self, screen):
        # Move this out and give as argument, if needed by anything else
        pos = pygame.mouse.get_pos()

        hover = self.isOver(pos)

        if hover:
            screen.blit(self.hover_surface,self.rect)
        else:
            screen.blit(self.surface,self.rect)

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.rect.x and pos[0] < self.rect.x + self.rect.width:
            if pos[1] > self.rect.y and pos[1] < self.rect.y + self.rect.height:
                return True
            
        return False
