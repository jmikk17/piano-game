from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

import auxil
from cfg import std_cfg

if TYPE_CHECKING:
    from game import Game
    from menu import MenuManager


class Mediator:
    """Mediator class for managing communication between UI and menumanager."""

    def __init__(self) -> None:
        """Initialize the Mediator class."""
        self.manager = None
        self.ui = None

    def set_manager(self, manager: MenuManager | Game) -> None:
        """Set the manager for the mediator.

        Args:
            manager (MenuManager | Game): The manager object to set.

        """
        self.manager = manager

    def set_ui(self, ui: UIAuxil) -> None:
        """Set the UI for the mediator.

        Args:
            ui (UIAuxil): The UI object to set.

        """
        self.ui = ui

    def notify(self, ui: UIAuxil) -> None:
        """Notify the manager of UI updates.

        Args:
            ui (UIAuxil): The UI object that has changed.

        """
        if self.manager:
            self.manager.update_manager_ui(ui)


class UIAuxil:
    """UI class for managing the layout and appearance of the game."""

    def __init__(self, screen_width: float, screen_height: float, mediator: Mediator) -> None:
        """Initialize the UI class.

        Args:
            screen_width (float): The width of the screen.
            screen_height (float): The height of the screen.
            mediator (Mediator): The mediator object for communication.

        """
        self.mediator = mediator
        mediator.set_ui(self)

        self.colors = {
            "background": auxil.WHITE,
            "selected": auxil.RED,
            "text": auxil.BLACK,
            "title": auxil.BLUE,
            "selected_text": auxil.BLUE,
            "instructions": (100, 100, 100),
        }

        # Set attributes, but dont mediate on construction
        self.update_ui(screen_width, screen_height, mediate=False)

    def update_ui(self, screen_width: float, screen_height: float, *, mediate: bool) -> None:
        """Update the UI layout based on the screen size.

        Args:
            screen_width (float): The width of the screen.
            screen_height (float): The height of the screen.
            mediate (bool): Whether to notify the mediator of changes.

        """
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

    def get_item_rect(self, index: int) -> pygame.Rect:
        """Get the rectangle for a menu item at given index in list.

        Args:
            index (int): The index of the item in the list.

        """
        y = self.content_start_y + (self.item_height + self.item_padding) * index
        return pygame.Rect(self.content_x, y, self.content_width, self.item_height)

    def get_item_text_pos(self, item_rect: pygame.Rect) -> tuple[int, int]:
        """Get the centered position for text within an item rectangle.

        Args:
            item_rect (pygame.Rect): The rectangle of the item.

        """
        return (item_rect.centerx, item_rect.centery)


class Button:
    """Simple button class for pressable buttons."""

    def __init__(
        self,
        cen_x: float,
        y: float,
        color: tuple,
        hover_color: tuple,
        text: str = "",
        font: pygame.font.Font = std_cfg.FONT,
    ) -> None:
        """Initialize the button.

        Args:
            cen_x (float): The x-coordinate of the center of the button.
            y (float): The y-coordinate of the button.
            color (tuple): The color of the button.
            hover_color (tuple): The color of the button when hovered.
            text (str, optional): The text to display on the button. Defaults to "".
            font (pygame.font.Font, optional): The font to use for the text. Defaults to std_cfg.FONT.

        """
        self.cen_x = cen_x
        self.y = y
        self.text = text
        self.font = auxil.get_sysfont(font, 36)

        self.color = color
        self.hover_color = hover_color

        self.surface = self.font.render(self.text, std_cfg.ANTIALIAS, self.color)
        self.hover_surface = self.font.render(self.text, std_cfg.ANTIALIAS, self.hover_color)
        self.rect = self.surface.get_rect(centerx=self.cen_x, y=self.y)

    def update(self, new_cen_x: float, new_y: float) -> None:
        """Update the position of the button.

        Args:
            new_cen_x (float): The new x-coordinate of the center of the button.
            new_y (float): The new y-coordinate of the button.

        """
        self.cen_x = new_cen_x
        self.y = new_y
        self.rect = self.surface.get_rect(centerx=self.cen_x, y=self.y)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button on the screen.

        Args:
            screen (pygame.Surface): The display surface to draw on.

        """
        pos = pygame.mouse.get_pos()

        hover = self.is_over(pos)

        if hover:
            screen.blit(self.hover_surface, self.rect)
        else:
            screen.blit(self.surface, self.rect)

    def is_over(self, pos: tuple[int, int]) -> bool:
        """Check if the mouse is over the button.

        Args:
            pos (tuple[int, int]): The position of the mouse.

        Returns:
            bool: True if the mouse is over the button, False otherwise.

        """
        return bool(
            pos[0] > self.rect.x
            and pos[0] < self.rect.x + self.rect.width
            and pos[1] > self.rect.y
            and pos[1] < self.rect.y + self.rect.height,
        )
