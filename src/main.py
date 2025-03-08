import pygame

import auxil
import error
from cfg import std_cfg
from gamestate import GameStateManager


def main() -> None:
    """Initialize the game and run the main game loop.

    This function sets up the game by initializing Pygame, creating the game window,
    setting up the logger, and initializing the game state manager. It then enters
    an infinite loop where it updates the game state, draws the game screen, and updates the display.

    Todo:
        * Add a song-ending mechanic
        * Add visualization when playing keys
        * Add a score system
        * Add tracking for current pitch

    """
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Piano game")

    error.setup_logger()

    manager = GameStateManager(screen)
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(std_cfg.FPS) / 1000.0

        manager.update(dt)

        manager.draw()

        auxil.display_fps(clock, screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
