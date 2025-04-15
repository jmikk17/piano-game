import pygame

from cfg import std_cfg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# List of all playable keys
keys = [
    pygame.K_a,
    pygame.K_s,
    pygame.K_d,
    pygame.K_f,
    pygame.K_g,
    pygame.K_h,
    pygame.K_j,
]

# Dictionary mapping playable keys to index in song
key_dictionary = {
    -1: None,
    0: pygame.K_a,
    1: pygame.K_s,
    2: pygame.K_d,
    3: pygame.K_f,
    4: pygame.K_g,
    5: pygame.K_h,
    6: pygame.K_j,
}


def get_sysfont(font: str, size: int) -> pygame.font.Font:
    """Load a system font.

    Args:
        font (str): The name of the font.
        size (int): The size of the font.

    Returns:
        pygame.font.Font: The loaded font object.

    """
    return pygame.font.SysFont(font, size)


def display_fps(clock: pygame.time.Clock, screen: pygame.Surface, color: tuple) -> None:
    """Display the current frames per second (FPS) on the screen.

    Args:
        clock (pygame.time.Clock): The clock object to get the FPS from.
        screen (pygame.Surface): The screen surface to draw on.
        color (tuple): The color of the text.

    """
    font = pygame.font.Font(None, 36)
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", std_cfg.ANTIALIAS, color)
    screen.blit(fps_text, (10, 90))


def display_score(score: float, screen: pygame.Surface, color: tuple) -> None:
    """Display the current score on the screen.

    Args:
        score (float): The current score.
        screen (pygame.Surface): The screen surface to draw on.
        color (tuple): The color of the text.

    """
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", std_cfg.ANTIALIAS, color)
    screen.blit(score_text, (10, 10))


def display_octave(octave: int, screen: pygame.Surface, color: tuple) -> None:
    """Display the current octave on the screen.

    Args:
        octave (int): The current octave.
        screen (pygame.Surface): The screen surface to draw on.
        color (tuple): The color of the text.

    """
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Current octave: {octave}", std_cfg.ANTIALIAS, color)
    screen.blit(score_text, (10, 50))
