import pygame  # noqa: D100

import auxil
import error
import test
from resource_path import resource_path

# Need to initilize mixer before we can load in sound
pygame.mixer.init()


class MenuAssets:
    def __init__(self):
        self.background = None

    def load(self):
        try:
            self.background = pygame.image.load(
                resource_path("graphics/menu/background.png")
            )
        except (pygame.error, FileNotFoundError):
            error.handle_error("Menu background img not found", "not_fatal")
            self.background = pygame.Surface((1280, 720))
            self.background.fill(auxil.WHITE)

    def unload(self):
        if self.background:
            self.background = None


class GameAssets:
    def __init__(self):
        self.background = None
        self.trumpet = None
        self.note_sounds_5 = None
        self.note_sounds_6 = None

    def load(self):
        try:
            self.trumpet = test.cut_sprite_sheet(
                resource_path("graphics/trumpet.png"), 32, 32
            )
            self.background = pygame.image.load(
                resource_path("graphics/menu/background.png")
            )
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
                pygame.K_s: pygame.mixer.Sound(resource_path("audio/c6.ogg")),
                pygame.K_d: pygame.mixer.Sound(resource_path("audio/c6.ogg")),
                pygame.K_f: pygame.mixer.Sound(resource_path("audio/c6.ogg")),
                pygame.K_g: pygame.mixer.Sound(resource_path("audio/c6.ogg")),
                pygame.K_h: pygame.mixer.Sound(resource_path("audio/c6.ogg")),
                pygame.K_j: pygame.mixer.Sound(resource_path("audio/c6.ogg")),
            }
            self.note_pictures_help = {
                "4": pygame.transform.scale(
                    pygame.image.load(
                        resource_path("graphics/quarter.png")
                    ).convert_alpha(),
                    (172, 172),
                ),
                "8": pygame.transform.scale(
                    pygame.image.load(
                        resource_path("graphics/half.png")
                    ).convert_alpha(),
                    (172, 172),
                ),
                "16": pygame.transform.scale(
                    pygame.image.load(
                        resource_path("graphics/whole.png")
                    ).convert_alpha(),
                    (172, 172),
                ),
            }
            self.note_pictures = {
                "4": pygame.transform.scale(
                    pygame.image.load(
                        resource_path("graphics/quarter2.png")
                    ).convert_alpha(),
                    (172, 172),
                ),
                "8": pygame.transform.scale(
                    pygame.image.load(
                        resource_path("graphics/half2.png")
                    ).convert_alpha(),
                    (172, 172),
                ),
                "16": pygame.transform.scale(
                    pygame.image.load(
                        resource_path("graphics/whole2.png")
                    ).convert_alpha(),
                    (172, 172),
                ),
                "g": pygame.transform.scale(
                    pygame.image.load(resource_path("graphics/g.png")).convert_alpha(),
                    (172, 172),
                ),
            }
        except (pygame.error, FileNotFoundError):
            error.handle_error("Menu background img not found", "not_fatal")
            self.background = pygame.Surface((1280, 720))
            self.background.fill(auxil.WHITE)
            # TODO error handeling for sounds and notes

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
