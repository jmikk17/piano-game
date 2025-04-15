import logging

import pygame

import auxil
import log
from resource_path import resource_path
from sprite import Sprite, SpriteManager

# Need to initilize mixer before we can load sound
pygame.mixer.init()


class MenuAssets:
    """Class for the menu assets. Handles loading and unloading of the menu assets."""

    def __init__(self) -> None:
        """Initialize the MenuAssets class."""
        self.background = None

    def load(self) -> None:
        """Load the menu assets."""
        try:
            self.background = pygame.image.load(resource_path("graphics/menu/background.png"))
        except (pygame.error, FileNotFoundError):
            log.log_write("Menu background img not found", logging.ERROR)
            self.background = pygame.Surface((1280, 720))
            self.background.fill(auxil.WHITE)

    def unload(self) -> None:
        """Unloadoad the menu assets."""
        if self.background:
            self.background = None


class GameAssets:
    """Class for the game assets. Handles loading and unloading of the game assets."""

    def __init__(self) -> None:
        """Initialize the GameAssets class."""
        self.sprite_manager = SpriteManager()

        self.background = None

    def load(self) -> None:
        """Load the game assets."""
        try:
            # The asset manager doesn't know about UI, so we add sprites with default position and change later
            trumpet_sprite = Sprite(resource_path("graphics/trumpet.png"), 32, 32)
            self.sprite_manager.add_sprite("trumpet", trumpet_sprite, 0.1)
        except (pygame.error, FileNotFoundError):
            log.log_write("Trumpet sprite not found", logging.ERROR)

        try:
            self.background = pygame.image.load(resource_path("graphics/menu/background.png"))
        except (pygame.error, FileNotFoundError):
            log.log_write("Menu background img not found", logging.ERROR)
            self.background = pygame.Surface((1280, 720))
            self.background.fill(auxil.WHITE)

        try:
            self.note_sounds_5 = {
                pygame.K_a: pygame.mixer.Sound(resource_path("audio/c5.ogg")),
                pygame.K_s: pygame.mixer.Sound(resource_path("audio/d5.ogg")),
                pygame.K_d: pygame.mixer.Sound(resource_path("audio/e5.ogg")),
                pygame.K_f: pygame.mixer.Sound(resource_path("audio/f5.ogg")),
                pygame.K_g: pygame.mixer.Sound(resource_path("audio/g5.ogg")),
                pygame.K_h: pygame.mixer.Sound(resource_path("audio/a5.ogg")),
                pygame.K_j: pygame.mixer.Sound(resource_path("audio/b5.ogg")),
            }
            self.note_sounds_6 = {
                pygame.K_a: pygame.mixer.Sound(resource_path("audio/c6.ogg")),
                pygame.K_s: pygame.mixer.Sound(resource_path("audio/d6.ogg")),
                pygame.K_d: pygame.mixer.Sound(resource_path("audio/e6.ogg")),
                pygame.K_f: pygame.mixer.Sound(resource_path("audio/f6.ogg")),
                pygame.K_g: pygame.mixer.Sound(resource_path("audio/g6.ogg")),
                pygame.K_h: pygame.mixer.Sound(resource_path("audio/a6.ogg")),
                pygame.K_j: pygame.mixer.Sound(resource_path("audio/b6.ogg")),
            }
            self.note_sounds = {
                "5": self.note_sounds_5,
                "6": self.note_sounds_6,
            }
        except (pygame.error, FileNotFoundError):
            log.log_write("Note sounds not found", logging.CRITICAL)

        try:
            self.note_pictures_help = {
                "4": pygame.transform.scale(
                    pygame.image.load(resource_path("graphics/quarter.png")).convert_alpha(),
                    (172, 172),
                ),
                "8": pygame.transform.scale(
                    pygame.image.load(resource_path("graphics/half.png")).convert_alpha(),
                    (172, 172),
                ),
                "16": pygame.transform.scale(
                    pygame.image.load(resource_path("graphics/whole.png")).convert_alpha(),
                    (172, 172),
                ),
            }
            self.note_pictures = {
                "4": pygame.transform.scale(
                    pygame.image.load(resource_path("graphics/quarter2.png")).convert_alpha(),
                    (172, 172),
                ),
                "8": pygame.transform.scale(
                    pygame.image.load(resource_path("graphics/half2.png")).convert_alpha(),
                    (172, 172),
                ),
                "16": pygame.transform.scale(
                    pygame.image.load(resource_path("graphics/whole2.png")).convert_alpha(),
                    (172, 172),
                ),
                "g": pygame.transform.scale(
                    pygame.image.load(resource_path("graphics/g.png")).convert_alpha(),
                    (172, 172),
                ),
            }
        except (pygame.error, FileNotFoundError):
            log.log_write("Note pictures not found", logging.CRITICAL)

    def unload(self) -> None:
        """Unload the game assets."""
        if self.background:
            self.background = None
        for octave in self.note_sounds:
            if self.note_sounds[octave]:
                for sound in self.note_sounds[octave].values():
                    sound.stop()
                self.note_sounds[octave] = None
        if self.sprite_manager:
            self.sprite_manager = None

        # Could add loading of fonts, menu music, etc. here
