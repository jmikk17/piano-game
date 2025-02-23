from __future__ import annotations

import pygame


class SpriteManager:
    """A class that manages the loading of sprites."""

    def __init__(self) -> None:
        """Initialize the SpriteManager."""
        self.sprites = {}

    def add_sprite(
        self,
        name: str,
        sheet_path: str,
        sprite_width: int,
        sprite_height: int,
        frame_time: float | None = None,
    ) -> None:
        """Add a sprite to the SpriteManager.

        Args:
            name (str): Name of the sprite.
            sheet_path (str): File path to the sprite sheet.
            sprite_width (int): Width of individual sprite.
            sprite_height (int): Height of individual sprite.
            frame_time (float): Frame time for sprite loop in seconds, default is None.

        """
        self.sprites[name] = Sprite(sheet_path, sprite_width, sprite_height, frame_time)


class Sprite:
    """A class that load a sprite sheet and stores it in frames."""

    def __init__(self, sheet_path: str, sprite_width: int, sprite_height: int, frame_time: float | None = None) -> None:
        """Initialize the Sprite by loading the sheet and cutting it into frames.

        Args:
            sheet_path (str): File path to the sprite sheet.
            sprite_width (int): Width of individual sprite.
            sprite_height (int): Height of individual sprite.
            frame_time (float): Frame time for sprite loop in seconds, default is None.

        """
        self.sheet_path = sheet_path
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.frame_time = frame_time

        sheet = pygame.image.load(sheet_path).convert_alpha()

        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()
        num_sprites_x = sheet_width // sprite_width
        num_sprites_y = sheet_height // sprite_height

        # Cut the sheet into individual frames and store in a list
        self.frames = []
        for j in range(num_sprites_y):
            for i in range(num_sprites_x):
                rect = pygame.Rect(i * sprite_width, j * sprite_height, sprite_width, sprite_height)
                frame = sheet.subsurface(rect)
                self.frames.append(frame)

        self.nframes = len(self.frames)
