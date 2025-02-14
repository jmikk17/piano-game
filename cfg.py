import logging  # noqa: D100


# Written as a class if need other configs in the future
class Config:
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

    # Play area settings
    PLAY_AREA_X = 350
    PLAY_AREA_WIDTH = 20
    PLAY_AREA_HEIGHT = 130
    PLAY_AREA_Y = 100
    HIT_WINDOW = 15

    # Logging settings
    DEBUG_MODE = True
    LOG_FILE = "game.log"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    if DEBUG_MODE:
        LOG_LEVEL = logging.DEBUG
        LOG_TO_CONSOLE = True
    else:
        LOG_LEVEL = logging.ERROR
        LOG_TO_CONSOLE = False


# The std_cfg instance is imported by all, so we could e.g. do:
# if DEBUG_mode:
#   std_cfg = Config_debug()
# else:
std_cfg = Config()
