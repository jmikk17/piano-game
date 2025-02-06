import pygame
from cfg import std_cfg
import auxil
import error
from gamestate import GameStateManager


def main():

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT))
    pygame.display.set_caption("Piano game")
    
    error.setup_logger()
    
    manager = GameStateManager()
    clock = pygame.time.Clock()
    
    while True:
        dt = clock.tick(std_cfg.FPS) / 1000.0

        manager.update(dt)    
            
        manager.draw(screen)

        auxil.display_fps(clock, screen)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
