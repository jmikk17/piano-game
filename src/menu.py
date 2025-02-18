import pygame
from cfg import std_cfg
import auxil
import json
import error
import os
from abc import ABC, abstractmethod
from assets import MenuAssets
import sys

# from ui import UILayout, Button
import ui
from resource_path import resource_path


class BaseMenu(ABC):
    def __init__(self, assets, layout):
        self.font = auxil.get_sysfont(std_cfg.FONT, 36)
        self.title_font = auxil.get_sysfont(std_cfg.FONT, 48)
        # TODO should be changed so all children refer to same ui guidelines, so we only need to update one
        # self.layout = UILayout(std_cfg.SCREEN_WIDTH, std_cfg.SCREEN_HEIGHT)
        self.layout = layout
        self.assets = assets

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def handle_input(self, event):
        pass

    @abstractmethod
    def update_menu_ui(self, layout):
        pass

    def draw_title(self, screen, x_pos, y_pos, title):
        """Draws title of selected menu"""
        # Can be made abstract later if we need different titles
        title_surface = self.title_font.render(title, True, self.layout.colors["title"])
        title_rect = title_surface.get_rect(centerx=x_pos, y=y_pos)
        screen.blit(title_surface, title_rect)


class MainMenu(BaseMenu):
    def __init__(self, assets, layout):
        super().__init__(assets, layout)
        self.options = ["Play", "Options", "Exit"]

        self.scaled_background = None

        self.buttons = []
        button_y = self.layout.content_start_y
        for idx, name in enumerate(self.options):
            self.buttons.append(
                ui.Button(
                    self.layout.x_center,
                    button_y,
                    self.layout.colors["text"],
                    self.layout.colors["selected"],
                    name,
                )
            )
            button_y = self.buttons[idx].rect.bottom + self.layout.pad_y

    def draw(self, screen):
        if self.scaled_background:
            screen.blit(self.scaled_background, (0, 0))
        elif self.assets.background:
            screen.blit(self.assets.background, (0, 0))
        else:
            screen.fill(self.layout.colors["background"])

        self.draw_title(screen, self.layout.x_center, self.layout.title_y, "Piano game")

        for button in self.buttons:
            button.draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.isOver(pos):
                    if button.text == "Exit":
                        pygame.quit()
                        sys.exit()
                    elif button.text == "Play":
                        return "SHOW_SONG_SELECT", None
                    elif button.text == "Options":
                        return "SHOW_OPTIONS", None
        return None, None

    def update_menu_ui(self, layout):
        # Get new scaled ui guides
        self.layout = layout

        # Update buttons
        button_y = self.layout.content_start_y
        for i, button in enumerate(self.buttons):
            button.update(self.layout.x_center, button_y)
            button_y = self.buttons[i].rect.bottom + self.layout.pad_y

        # Scale background
        self.scaled_background = pygame.transform.scale(
            self.assets.background, (self.layout.x_unit * 100, self.layout.y_unit * 100)
        )


class SongSelectMenu(BaseMenu):
    # TODO add more info on song, and solution for if we have too many songs?
    # + check if use of content_end for back_button is correct, and if we can use it to determine how many songs we can show
    def __init__(self, assets, layout):
        super().__init__(assets, layout)
        self.songs = []
        self.buttons = []
        self.load_available_songs()

        self.back_button = ui.Button(
            self.layout.x_center,
            self.layout.content_end_y,
            self.layout.colors["text"],
            self.layout.colors["selected"],
            "Back to main menu",
        )
        self.scaled_background = None

    def load_available_songs(self):
        song_dir = resource_path("songs/")
        if not os.path.exists(song_dir):
            error.handle_error("Songs dir not found", "fatal")

        song_files = [f for f in os.listdir(song_dir) if f.endswith(".json")]

        for file in song_files:
            with open(os.path.join(song_dir, file)) as f:
                song_data = json.load(f)
                self.songs.append(
                    {
                        "filename": file,
                        "title": song_data.get("title", file),
                        "difficulty": song_data.get("difficulty", "Normal"),
                        "bpm": song_data.get("bpm", std_cfg.BPM),
                    }
                )

        button_y = self.layout.content_start_y
        for idx, song in enumerate(self.songs):
            self.buttons.append(
                ui.Button(
                    self.layout.x_center,
                    button_y,
                    self.layout.colors["text"],
                    self.layout.colors["selected"],
                    song["title"],
                )
            )
            button_y = self.buttons[idx].rect.bottom + self.layout.pad_y

    def draw(self, screen):
        if self.scaled_background:
            screen.blit(self.scaled_background, (0, 0))
        elif self.assets.background:
            screen.blit(self.assets.background, (0, 0))
        else:
            screen.fill(self.layout.colors["background"])

        self.draw_title(
            screen, self.layout.x_center, self.layout.title_y, "Select a song"
        )

        for button in self.buttons:
            button.draw(screen)

        self.back_button.draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if self.back_button.isOver(pos):
                return "SHOW_MAIN_MENU", None
            for idx, button in enumerate(self.buttons):
                if button.isOver(pos):
                    return "START_GAME", self.songs[idx]["filename"]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "SHOW_MAIN_MENU", None
        return None, None

    def update_menu_ui(self, layout):
        # Get new scaled ui guides
        self.layout = layout
        # Update buttons
        button_y = self.layout.content_start_y
        for i, button in enumerate(self.buttons):
            button.update(self.layout.x_center, button_y)
            button_y = self.buttons[i].rect.bottom + self.layout.pad_y

        self.back_button.update(self.layout.x_center, self.layout.content_end_y)

        # Scale background
        self.scaled_background = pygame.transform.scale(
            self.assets.background, (self.layout.x_unit * 100, self.layout.y_unit * 100)
        )


class OptionsMenu(BaseMenu):
    def __init__(self, assets, layout):
        super().__init__(assets, layout)
        self.options = ["TO DO"]

        self.scaled_background = None

        self.buttons = []
        button_y = self.layout.content_start_y
        for idx, name in enumerate(self.options):
            self.buttons.append(
                ui.Button(
                    self.layout.x_center,
                    button_y,
                    self.layout.colors["text"],
                    self.layout.colors["selected"],
                    name,
                )
            )
            button_y = self.buttons[idx].rect.bottom + self.layout.pad_y

        self.back_button = ui.Button(
            self.layout.x_center,
            self.layout.content_end_y,
            self.layout.colors["text"],
            self.layout.colors["selected"],
            "Back to main menu",
        )

    def draw(self, screen):
        if self.scaled_background:
            screen.blit(self.scaled_background, (0, 0))
        elif self.assets.background:
            screen.blit(self.assets.background, (0, 0))
        else:
            screen.fill(self.layout.colors["background"])

        self.draw_title(screen, self.layout.x_center, self.layout.title_y, "Options")

        for button in self.buttons:
            button.draw(screen)

        self.back_button.draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if self.back_button.isOver(pos):
                return "SHOW_MAIN_MENU", None
            for button in self.buttons:
                if button.isOver(pos):
                    if button.text == "TO DO":
                        pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "SHOW_MAIN_MENU", None
        return None, None

    def update_menu_ui(self, layout):
        # Get new scaled ui guides
        self.layout = layout

        # Update buttons
        button_y = self.layout.content_start_y
        for i, button in enumerate(self.buttons):
            button.update(self.layout.x_center, button_y)
            button_y = self.buttons[i].rect.bottom + self.layout.pad_y

        self.back_button.update(self.layout.x_center, self.layout.content_end_y)

        # Scale background
        self.scaled_background = pygame.transform.scale(
            self.assets.background, (self.layout.x_unit * 100, self.layout.y_unit * 100)
        )


class MenuManager:
    def __init__(self, layout, mediator):
        self.layout = layout
        self.menu_assets = MenuAssets()
        self.menu_assets.load()
        mediator.set_manager(self)

        self.menus = {
            "main": MainMenu(self.menu_assets, self.layout),
            "song_select": SongSelectMenu(self.menu_assets, self.layout),
            "options": OptionsMenu(self.menu_assets, self.layout),
        }

        self.show_menu("main")

    def show_menu(self, menu_name):
        """Change reference of current_menu to a specified menu"""
        self.current_menu = self.menus[menu_name]
        # Update UI on change in case it was changed in previous menu
        self.current_menu.update_menu_ui(self.layout)

    def handle_input(self, event):
        """Handle input through the menus own function"""
        # Returns action, data as "START_GAME",song_name if a song is selected, which indicates we need a state swap
        # Also handles quit and menu swap if requested
        if self.current_menu:
            action, data = self.current_menu.handle_input(event)
            if action:
                if action == "START_GAME":
                    return action, data
                elif action == "SHOW_MAIN_MENU":
                    self.show_menu("main")
                elif action == "SHOW_SONG_SELECT":
                    self.show_menu("song_select")
                elif action == "SHOW_OPTIONS":
                    self.show_menu("options")
                elif action == "QUIT":
                    pygame.quit()
                    sys.exit()
        return (None, None)

    def draw(self, screen):
        """Draw the menu through its own drawing function"""
        if self.current_menu:
            self.current_menu.draw(screen)

    def update_manager_ui(self, layout):
        # TODO this is clunky, we are updating ui in both manager and menus right now
        self.layout = layout
        self.current_menu.update_menu_ui(layout)
