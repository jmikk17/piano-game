import pygame

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


def get_font(font, size):
    return pygame.font.Font(font, size)


def get_sysfont(font, size):
    return pygame.font.SysFont(font, size)


def display_fps(clock, screen):
    font = pygame.font.Font(None, 36)
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, BLACK)
    screen.blit(fps_text, (10, 10))


def display_score(score, screen):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 50))


def handle_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return


def check_keyboard():
    # TODO: remove after refactoring done
    key_state = {key: False for key in keys}
    pressed_keys = pygame.key.get_pressed()
    for key in keys:
        key_state[key] = pressed_keys[key]
    return key_state
