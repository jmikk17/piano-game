import logging

import pygame

import auxil
import log
from resource_path import resource_path
from sprite import Sprite, SpriteManager

# Need to initilize mixer before we can load sound
pygame.mixer.init()


class MenuAssets:
    def __init__(self):
        self.background = None

    def load(self):
        try:
            self.background = pygame.image.load(resource_path("graphics/menu/background.png"))
        except (pygame.error, FileNotFoundError):
            log.log_write("Menu background img not found", logging.ERROR)
            self.background = pygame.Surface((1280, 720))
            self.background.fill(auxil.WHITE)

    def unload(self):
        if self.background:
            self.background = None


class GameAssets:
    def __init__(self):
        self.sprite_manager = SpriteManager()

        self.background = None

        self.note_sounds = None
        self.note_sounds_5 = None
        self.note_sounds_6 = None

    def load(self):
        try:
            # The asset manager doesn't know about UI, so we add sprites with default position and change later
            trumpet_sprite = Sprite(resource_path("graphics/trumpet.png"), 32, 32)
            self.sprite_manager.add_sprite("trumpet", trumpet_sprite, 0.1)
        except (pygame.error, FileNotFoundError):
            log.log_write("Trumpet sprite not found", logging.ERROR)
        try:
            self.background = pygame.image.load(resource_path("graphics/menu/background.png"))
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
            log.log_write("Menu background img not found", logging.ERROR)
            self.background = pygame.Surface((1280, 720))
            self.background.fill(auxil.WHITE)

    def unload(self):
        if self.background:
            self.background = None
        if self.note_sounds:
            for sound in self.note_sounds.values():
                sound.stop()
                sound = None
        if self.note_sounds:
            self.note_sounds = None

        # Could add loading of fonts, menu music, etc. here
