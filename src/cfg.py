import logging


class Config:
    """Class for the game configuration."""

    # Screen settings
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 60

    # Game settings
    BPM = 120
    BEATS_PER_BAR = 4
    SLOTS_PER_BAR = 16
    NOTE_VELOCITY = 300
    FADEOUT = 250
    FONT = "courier new"
    MIN_OCTAVE = 5
    MAX_OCTAVE = 6
    NOTE_MIRROR = 7
    B_TRACK_VOL = 0.5

    # Play area settings
    PLAY_AREA_X = 350
    PLAY_AREA_WIDTH = 20
    PLAY_AREA_HEIGHT = 130
    PLAY_AREA_Y = 100
    HIT_WINDOW = 15

    ANTIALIAS = True

    # Logging settings
    DEBUG_MODE = False
    LOG_FILE = "game.log"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    if DEBUG_MODE:
        LOG_LEVEL = logging.DEBUG
        LOG_TO_CONSOLE = True
    else:
        LOG_LEVEL = logging.ERROR
        LOG_TO_CONSOLE = False


std_cfg = Config()
