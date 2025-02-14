import pytest
import pygame
from cfg import std_cfg
from gamestate import GameStateManager  # Adjust import path as needed


@pytest.fixture
def mock_screen(mocker):
    screen = mocker.MagicMock()
    screen.get_width.return_value = std_cfg.SCREEN_WIDTH
    screen.get_height.return_value = std_cfg.SCREEN_HEIGHT
    return screen


@pytest.fixture
def mock_game(mocker):
    return mocker.MagicMock()


@pytest.fixture
def mock_menu_manager(mocker):
    return mocker.MagicMock()


@pytest.fixture
def game_state_manager(mocker, mock_screen, mock_menu_manager):
    # Patch pygame.display.set_mode
    mocker.patch("pygame.display.set_mode", return_value=mock_screen)

    # Patch MenuManager
    mocker.patch("menu.MenuManager", return_value=mock_menu_manager)

    return GameStateManager(mock_screen)


def test_init_state(game_state_manager):
    """Test initial state of GameStateManager"""
    assert game_state_manager.current_state == "MENU"
    assert not hasattr(game_state_manager, "game") or game_state_manager.game is None


def test_menu_quit_event(game_state_manager, mocker):
    """Test handling of quit event in menu state"""
    # Create mock event
    mock_event = mocker.MagicMock(type=pygame.QUIT)

    # Patch pygame.event.get
    mocker.patch("pygame.event.get", return_value=[mock_event])

    # Patch pygame.quit to prevent actual quit
    mocker.patch("pygame.quit")

    with pytest.raises(SystemExit):
        game_state_manager.update(0.016)


def test_menu_resize_event(game_state_manager, mocker, mock_screen):
    """Test handling of resize event in menu state"""
    # Create mock resize event
    new_width = std_cfg.SCREEN_WIDTH + 100
    new_height = std_cfg.SCREEN_HEIGHT + 100
    mock_event = mocker.MagicMock(type=pygame.VIDEORESIZE, size=(new_width, new_height))

    # Patch pygame.event.get
    mocker.patch("pygame.event.get", return_value=[mock_event])

    # Patch display.set_mode
    mock_set_mode = mocker.patch("pygame.display.set_mode", return_value=mock_screen)

    game_state_manager.update(0.016)

    # Verify set_mode was called with correct dimensions
    mock_set_mode.assert_called_once_with((new_width, new_height), pygame.RESIZABLE)


def test_start_game_transition(game_state_manager, mocker, mock_screen):
    """Test transition from menu to game state"""
    # Mock Game class
    mock_game_class = mocker.patch("game.Game")
    mock_game_instance = mocker.MagicMock()
    mock_game_class.return_value = mock_game_instance

    # Mock song data
    mock_song_data = mocker.MagicMock()

    # Patch display.set_mode
    mock_set_mode = mocker.patch("pygame.display.set_mode", return_value=mock_screen)

    game_state_manager.handle_state_transition("START_GAME", mock_song_data)

    assert game_state_manager.current_state == "GAME"
    assert game_state_manager.game == mock_game_instance
    mock_set_mode.assert_called_once_with((std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT))


def test_game_update_quit_to_menu(game_state_manager, mocker):
    """Test game update with quit to menu"""
    # Setup game state with mock game
    mock_game = mocker.MagicMock()
    mock_game.update.return_value = "QUIT_TO_MENU"
    game_state_manager.game = mock_game
    game_state_manager.current_state = "GAME"

    # Patch display.set_mode
    mocker.patch("pygame.display.set_mode")

    game_state_manager.update(0.016)

    mock_game.update.assert_called_once_with(0.016)
    assert game_state_manager.current_state == "MENU"
    assert game_state_manager.game is None


@pytest.mark.parametrize(
    "current_state,expected_draw_call",
    [
        ("MENU", "menu_manager.draw"),
        ("GAME", "game.draw"),
    ],
)
def test_draw(game_state_manager, mocker, current_state, expected_draw_call):
    """Test draw method in different states"""
    game_state_manager.current_state = current_state

    if current_state == "GAME":
        game_state_manager.game = mocker.MagicMock()

    game_state_manager.draw()

    if current_state == "MENU":
        game_state_manager.menu_manager.draw.assert_called_once_with(
            game_state_manager.screen
        )
    else:
        game_state_manager.game.draw.assert_called_once_with(game_state_manager.screen)


def test_handle_return_to_menu(game_state_manager, mocker, mock_screen):
    """Test handling return to menu transition"""
    # Setup initial game state
    game_state_manager.current_state = "GAME"
    game_state_manager.game = mocker.MagicMock()

    # Patch display.set_mode
    mock_set_mode = mocker.patch("pygame.display.set_mode", return_value=mock_screen)

    game_state_manager.handle_state_transition("RETURN_TO_MENU", None)

    assert game_state_manager.current_state == "MENU"
    assert game_state_manager.game is None
    mock_set_mode.assert_called_once_with(
        (std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT), pygame.RESIZABLE
    )
