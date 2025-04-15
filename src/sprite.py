from __future__ import annotations

import logging

import pygame

import log


class SpriteManager:
    """A class that manages the loading of sprites."""

    def __init__(self) -> None:
        """Initialize the SpriteManager."""
        self.sprites = {}
        self.sprite_clock = 0

    def add_sprite(
        self,
        name: str,
        sprite: Sprite,
        update_interval: float = 0.1,
        pos: tuple[float | int, float | int] = (0, 0),
    ) -> None:
        """Add a sprite to the SpriteManager.

        Args:
            name (str): The name of the sprite to add, used as id for other functions.
            sprite (Sprite): The sprite object to add.
            update_interval (float): Frame time for sprite loop in seconds, default is 0.1 seconds.
            pos (tuple[float | int, float | int]): The position of the sprite.

        """
        if name in self.sprites:
            log.log_write("Two sprites with same name, use copy instead", logging.CRITICAL)
        self.sprites[name] = {
            "sprite": sprite,
            "interval": update_interval,
            "last_update": 0,
            "position": pos,
        }

    def update(self, dt: float) -> None:
        """Update the sprite clock and current frame for sprites.

        Args:
            dt (float): Time passed since last frame in seconds.

        """
        self.sprite_clock += dt

        for sprite_info_dict in self.sprites.values():
            # Key is sprite, and value is sprite_info_dict containing interval and last_update
            if self.sprite_clock - sprite_info_dict["last_update"] > sprite_info_dict["interval"]:
                sprite_info_dict["sprite"].update()
                sprite_info_dict["last_update"] = self.sprite_clock

    def change_position(self, name: str, pos: tuple[float | int, float | int]) -> None:
        """Change the position of a sprite.

        Args:
            name (str): The name of the sprite to change the position of.
            sprite (Sprite): The sprite object to change the position of.
            pos (tuple[float | int, float | int]): The new position of the sprite.

        """
        if name in self.sprites:
            self.sprites[name]["position"] = pos

    def draw(self, screen: pygame.Surface) -> None:
        """Draw all sprites on the screen."""
        for sprite_info_dict in self.sprites.values():
            sprite = sprite_info_dict["sprite"]
            screen.blit(sprite.frames[sprite.current_frame], sprite_info_dict["position"])

    def copy(self, name: str, new_name: str, update_interval: float | None = None) -> None:
        """Copy a sprite with a new name.

        Args:
            name (str): The name of the sprite to copy.
            new_name (str): The new name of the sprite.
            update_interval (float | None): The new update interval for the sprite.
                If None, the original update interval is used.

        """
        if name in self.sprites and new_name not in self.sprites:
            self.sprites[new_name] = self.sprites[name].copy()
        else:
            log.handle_error("Sprite copy failure, use add instead or give unique name", "fatal")

        # If we want a different update interval, we will need a new sprite class,
        # since current frame is tracked within the class
        if update_interval:
            self.sprites[new_name]["sprite"] = Sprite(
                self.sprites[name]["sprite"].sheet_path,
                self.sprites[name]["sprite"].sprite_width,
                self.sprites[name]["sprite"].sprite_height,
            )
            self.sprites[new_name]["interval"] = update_interval


class Sprite:
    """A class that load a sprite sheet and stores it in frames."""

    def __init__(self, sheet_path: str, sprite_width: int, sprite_height: int) -> None:
        """Initialize the Sprite by loading the sheet and cutting it into frames.

        Args:
            sheet_path (str): File path to the sprite sheet.
            sprite_width (int): Width of individual sprite.
            sprite_height (int): Height of individual sprite.
            frame_time (float): Frame time for sprite loop in seconds, default is None.

        """
        self.current_frame = 0
        self.sheet_path = sheet_path
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height

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

    def update(self) -> None:
        """Update the current frame."""
        self.current_frame = (self.current_frame + 1) % self.nframes
