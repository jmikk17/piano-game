from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

import auxil
from assets import GameAssets
from cfg import std_cfg
from music_engine import MusicPlayer

if TYPE_CHECKING:
    import ui


class Game:
    """Class for the game state.

    This class draws the static part of the music player, and initialize and updates the music player.

    Attributes:
        assets (GameAssets): The assets used in the game.
        layout (UIAuxil): The layout guidelines for the game.
        scaled_background (pygame.Surface, optional): The background image scaled to the screen size.
        lines (int): The number of lines on the screen.
        line_thick (int): The thickness of the lines.
        line_gap (int): The gap between the lines.
        line_lower (int): The y-coordinate of the lower line.
        line_left (int): The x-coordinate of the left line.
        line_right (int): The x-coordinate of the right line.
        play_box (tuple): The rectangle for the play area.
        play_width (int): The width of the play area.
        play_center (int): The center of the play area.
        play_b_delay (int): The delay for the play area.
        musicplayer (MusicPlayer): The music player for the game.
        trumpet_time (float): The time for the trumpet sprite.
        current_trumpet (int): The current trumpet sprite.

    Todo:
        * Standardize the screen layout from the layout class instead of hardcoded values.
        * Make seperate class for handling sprites.

    """

    def __init__(self, data: str, layout: ui.UIAuxil) -> None:
        """Initialize the Game class.

        Args:
            data (str): The file path for the song selected.
            layout (UIAuxil): The layout guidelines for the game.

        """
        self.assets = GameAssets()
        self.assets.load()
        self.layout = layout

        self.scaled_background = None
        if self.layout.x_unit * 100 != std_cfg.SCREEN_WIDTH or self.layout.y_unit * 100 != std_cfg.SCREEN_HEIGHT:
            self.scaled_background = pygame.transform.scale(
                self.assets.background,
                (self.layout.x_unit * 100, self.layout.y_unit * 100),
            )

        self.lines = 5
        self.line_thick = 2
        self.line_gap = 20
        self.line_lower = 200
        self.line_left = 240
        self.line_right = 1280

        self.play_box = (350, 100, 50, 130)
        self.play_width = self.play_box[2] / 2
        self.play_center = self.play_box[0] + self.play_width

        self.play_b_delay = (1200 - self.play_center) / std_cfg.NOTE_VELOCITY
        # 1200 = where we spawn notes
        # self.play_center = where we register hit
        # -5 = adjustment for center of note ish

        self.musicplayer = MusicPlayer(data, self.assets, self.play_center, self.play_width, self.play_b_delay)

        # sprite test!
        self.assets.sprite_manager.change_position("trumpet", (500, 500))

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the background, static part of the music player, and the spite(s).

        Args:
            screen (pygame.Surface): The display surface for the game.

        """
        if self.scaled_background:
            screen.blit(self.scaled_background, (0, 0))
        elif self.assets.background:
            screen.blit(self.assets.background, (0, 0))
        else:
            screen.fill(self.layout.colors["background"])

        for i in range(self.lines):
            pygame.draw.line(
                screen,
                auxil.BLACK,
                (self.line_left, self.line_lower - i * self.line_gap),
                (self.line_right, self.line_lower - i * self.line_gap),
                self.line_thick,
            )
        screen.blit(self.assets.note_pictures["g"], (200, 74))
        self.play_box = pygame.draw.rect(screen, (0, 255, 0), self.play_box)  # x,y,width,height

        self.musicplayer.draw(screen)

        self.assets.sprite_manager.draw(screen)

    def update(self, dt: float) -> str | None:
        """Update the music player and the sprite(s).

        Args:
            dt (float): Time passed since last frame in seconds.

        Returns:
            str: Return a string with "QUIT_TO_MENU" if the game should return to the menu.

        """
        key_state = auxil.check_keyboard()
        status = self.musicplayer.update(dt, key_state)

        # sprite test!
        self.assets.sprite_manager.update(dt)

        return status
