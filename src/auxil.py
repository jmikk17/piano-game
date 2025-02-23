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
    key_state = {key: False for key in keys}
    pressed_keys = pygame.key.get_pressed()
    for key in keys:
        key_state[key] = pressed_keys[key]
    return key_state


def cut_sprite_sheet(sheet_path: str, sprite_width: int, sprite_height: int) -> list:
    """Cut a sprite sheet into individual frames.

    Args:
        sheet_path (str): Path to the sprite sheet image
        sprite_width (int): Width of each individual sprite
        sprite_height (int): Height of each individual sprite

    Returns:
        list: List of pygame Surface objects, each containing one frame

    Todo:
        * Rewrite this as a class.

    """
    sheet = pygame.image.load(sheet_path).convert_alpha()

    # Calculate number of sprites in the sheet
    sheet_width = sheet.get_width()
    sheet_height = sheet.get_height()
    num_sprites_x = sheet_width // sprite_width
    num_sprites_y = sheet_height // sprite_height

    # Cut the sheet into individual frames and store in a list
    frames = []
    for j in range(num_sprites_y):
        for i in range(num_sprites_x):
            rect = pygame.Rect(i * sprite_width, j * sprite_height, sprite_width, sprite_height)
            frame = sheet.subsurface(rect)
            frames.append(frame)

    return frames
