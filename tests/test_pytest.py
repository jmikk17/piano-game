import pygame
import pytest
from pytest_mock import MockerFixture

from src.cfg import std_cfg
from src.gamestate import GameStateManager

# Setup for a future testing framework, very useless in its current form


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """Initialize pygame before running any tests."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_screen(mocker: MockerFixture):
    screen = mocker.MagicMock()
    screen.get_width.return_value = std_cfg.SCREEN_WIDTH
    screen.get_height.return_value = std_cfg.SCREEN_HEIGHT
    return screen


@pytest.fixture
def mock_menu_manager(mocker):
    return mocker.MagicMock()


@pytest.fixture
def game_state_manager(mocker, mock_screen, mock_menu_manager):
    # Patch pygame.display.set_mode
    mocker.patch("pygame.display.set_mode", return_value=mock_screen)

    # Patch MenuManager
    mocker.patch("src.menu.MenuManager", return_value=mock_menu_manager)

    return GameStateManager(mock_screen)


def test_init_state(game_state_manager):
    """Test initial state of GameStateManager."""
    assert game_state_manager.current_state == "MENU"
    assert not hasattr(game_state_manager, "game") or game_state_manager.game is None
