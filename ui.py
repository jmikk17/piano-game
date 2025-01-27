import pygame
from cfg import std_cfg
import auxil

class Mediator:
    def __init__(self):
        self.menu = None
        self.ui = None

    def set_menu(self,menu):
        self.menu = menu

    def set_ui(self,ui):
        self.ui = ui 

    def notify(self,ui):
            self.menu.handle_ui_event(ui)

class UILayout:
    def __init__(self, screen_width, screen_height, mediator):
        self.mediator = mediator
        self.colors = {
            'background': auxil.WHITE,
            'selected': (200, 200, 255),
            'text': auxil.BLACK,
            'title': auxil.BLUE,
            'selected_text': auxil.BLUE,
            'instructions': (100, 100, 100)
        }

        self.update_ui(screen_width, screen_height, False)
        # cant initilize with update, now that it calls mediator

    def update_ui(self, screen_width, screen_height, mediate):
        self.y_unit = screen_height * 0.01
        self.x_unit = screen_width * 0.01

        self.x_center = screen_width / 2
        self.y_center = screen_height / 2

        self.title_y = self.y_unit * 10 
        self.content_start_y = self.y_unit * 25
        self.content_end_y = self.y_unit * 80

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
    def __init__(self, cen_x, y, text='', font=std_cfg.FONT):
        self.cen_x = cen_x
        self.y = y
        self.text = text
        self.font = auxil.get_sysfont(font, 36)
        
        self.color = auxil.BLUE

        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(
            centerx = self.cen_x,
            y = self.y
        )

    def draw(self, screen, outline=None):
        #pygame.draw.rect(screen,auxil.BLACK,self.rect)
        screen.blit(self.surface,self.rect)

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
