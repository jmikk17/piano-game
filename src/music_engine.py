from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pygame

import auxil
from cfg import std_cfg
from resource_path import resource_path

if TYPE_CHECKING:
    from assets import GameAssets


class Note:
    """A class representing a single note in a song."""

    def __init__(self, bar: int, slot: int, note_type: int, pitch: int) -> None:
        """Initialize a note with the given parameters.

        Args:
            bar (int): Bar number in song
            slot (int): Slot within the bar
            note_type (int): Duration or type of note
            pitch (int): Pitch of the note

        """
        self.bar = bar
        self.slot = slot
        self.note_type = note_type
        self.pitch = pitch

        self.active = False
        self.hit = False

        self.rect = None
        self.image = None

        self.score = 0

    def __repr__(self) -> str:
        """Return a string representation of the note, mainly for debugging purposes."""
        return f"Note(slot={self.slot}, type={self.note_type}, pitch={self.pitch})"


class Song:
    """A class representing a song with notes to play.

    Methods:
        add_note: Add a note to the song
        remove_note: Remove a note from the song
        from_json: Create a Song object from a JSON file
        get_notes_for_time: Get all notes for a given slot + bar combination

    """

    def __init__(
        self,
        bpm: int = std_cfg.BPM,
        slots_per_bar: int = std_cfg.SLOTS_PER_BAR,
        b_path: str | None = None,
    ) -> None:
        """Initialize a song with the given parameters.

        Args:
            bpm (int, optional): BPM of the song. Defaults to std_cfg.BPM.
            slots_per_bar (int, optional): Slots per bar of the song. Defaults to std_cfg.SLOTS_PER_BAR.
            b_path (str | None, optional): Path to the b-track for song. Defaults to None.

        """
        self.bpm = bpm
        self.slots_per_bar = slots_per_bar
        self.notes = []
        self.b_path = b_path

    def add_note(self, bar: int, slot: int, note_type: int, pitch: int) -> None:
        """Add a note to the song.

        Args:
            bar (int): Bar number in song
            slot (int): Slot within the bar
            note_type (int): Duration or type of note
            pitch (int): Pitch of the note

        """
        self.notes.append(Note(bar, slot, note_type, pitch))

    def remove_note(self, note: Note) -> None:
        """Remove a note from the song.

        Args:
            note (Note): Note to remove

        """
        if note in self.notes:
            self.notes.remove(note)

    @classmethod
    def from_json(cls, filepath: str) -> Song:
        """Create a Song object from a JSON file.

        Args:
            filepath (str): Path to the JSON file

        Returns:
            Song: A Song object created from the JSON file

        """
        with Path(resource_path("songs/" + filepath)).open() as f:
            data = json.load(f)
        b_path = data.get("b_path", None)
        song = cls(data["bpm"], data["slots_per_bar"], b_path)
        for note_data in data["notes"]:
            song.add_note(
                note_data["bar"],
                note_data["slot"],
                note_data["note_type"],
                note_data["pitch"],
            )
        return song

    def get_notes_for_time(self, bar: int, slot: int) -> list[Note]:
        """Get all notes for a given slot + bar combination.

        Args:
            bar (int): Bar number
            slot (int): Slot in the bar

        Returns:
            list[Note]: List of notes for the given slot + bar combination

        """
        return [note for note in self.notes if note.bar == bar and note.slot == slot]

    def __repr__(self) -> str:
        """Return a string representation of the song, mainly for debugging purposes."""
        return f"Song(bpm={self.bpm}, slots_per_bar={self.slots_per_bar}, notes={self.notes})"


class MusicPlayer:
    """Class for playing a song.

    Methods:
        update: Update the music player
        draw: Draw the notes on the screen

    """

    def __init__(
        self,
        song: str,
        assets: GameAssets,
        play_center: float,
        play_margain: float,
        play_b_time: float,
    ) -> None:
        """Initialize the music player.

        Args:
            song (str): The file path for the song selected.
            assets (GameAssets): The assets used in the game.
            play_center (float): x-coordinate of the center of the play area
            play_margain (float): Width of the play area
            play_b_time (float): When to start playing the b-track to match with notes

        """
        self.assets = assets
        self.song = Song.from_json(song)
        self.play_center = play_center
        self.play_margain = play_margain
        self.play_b_time = play_b_time

        self.start_time = pygame.time.get_ticks() / 1000.0

        self.note_manager = NoteManager(self.song, self.assets, self.play_margain, self.play_center)
        self.audio_manager = AudioManager(self.song, self.assets, self.play_b_time)
        self.input_handler = InputHandler()

        self.key_state = dict.fromkeys(auxil.keys, False)
        self.score = 0

    def update(self, dt: float) -> str | None:
        """Update the musicplayer.

        Args:
            dt (float): Time since last update

        Returns:
            str | None: Status of the game, such as "QUIT_TO_MENU" or None

        """
        self.key_state = self.input_handler.check_keyboard()
        status = self.input_handler.handle_input(self.audio_manager.b_track, b_playing=self.audio_manager.b_playing)

        self.note_manager.check_note_hit(self.key_state, self.input_handler.octave)
        self.note_manager.check_note_spawn()
        self.score += self.note_manager.update_notes(dt)

        self.audio_manager.play_notes(self.key_state, self.input_handler.octave)
        self.audio_manager.play_b_track(self.start_time)

        return status

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the notes.

        Args:
            screen (pygame.Surface): The display surface for the game.

        """
        self.note_manager.draw(screen)
        auxil.display_score(self.score, screen, auxil.WHITE)
        auxil.display_octave(self.input_handler.octave, screen, auxil.WHITE)

        for key, is_pressed in self.key_state.items():
            if is_pressed:
                index = auxil.keys.index(key)
                pygame.draw.circle(
                    screen,
                    auxil.RED,
                    (self.play_center, 220 - (index + (self.input_handler.octave - 5) * 7) * 10),
                    5,
                )

        if std_cfg.DEBUG_MODE:
            auxil.display_fps(pygame.time.Clock(), screen, auxil.WHITE)


class AudioManager:
    """A class for managing audio part of a song.

    Methods:
        play_b_track: Play the b-track of the song
        play_notes: Play notes when keys are pressed

    """

    def __init__(self, song: Song, assets: GameAssets, play_b_time: float | None) -> None:
        """Initilize audio manager.

        Args:
            song (Song): Song object being played
            assets (GameAssets): Assets object containing audio for notes
            play_b_time (float): When to start playing the b-track

        """
        self.song = song
        self.play_b_time = play_b_time
        self.b_playing = False

        self.assets = assets

        self.b_track = None
        if self.song.b_path:
            self.b_track = pygame.mixer.Sound(resource_path("audio/" + self.song.b_path))

    def play_b_track(self, start_time: float) -> None:
        """Play the b-track of the song if enough time has passed and it is not already playing.

        Args:
            start_time (float): The time when the game started a song

        """
        current_time = pygame.time.get_ticks() / 1000.0
        if self.song.b_path and current_time - start_time >= self.play_b_time and not self.b_playing:
            self.b_playing = True
            self.b_track.play()

    def play_notes(self, key_state: dict[str, bool], octave: int) -> None:
        """Play notes when keys are pressed.

        Args:
            key_state (dict[str, bool]): Dictionary of key states
            octave (int): The current octave of the keyboard

        """
        for key, is_pressed in key_state.items():
            if is_pressed:
                self.assets.note_sounds[str(octave)][key].play()
            elif not is_pressed:
                for octave_key in self.assets.note_sounds:
                    self.assets.note_sounds[octave_key][key].fadeout(std_cfg.FADEOUT)


class InputHandler:
    """A class for managing input during a song.

    Methods:
        handle_input: Handle input during a song, such as changing octave or quitting
        check_keyboard: Check the state of the keyboard

    """

    def __init__(self) -> None:
        """Set the initial octave to 5."""
        self.octave = 5

    def handle_input(self, b_track: pygame.mixer.Sound | None, *, b_playing: bool) -> str | None:
        """Handle input during a song.

        Args:
            b_playing (bool): Whether the b-track is playing
            b_track (pygame.mixer.Sound): The b-track sound object

        Returns:
            str | None: Status of the game, such as "QUIT_TO_MENU" or None

        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if b_playing:
                        b_track.stop()
                    return "QUIT_TO_MENU"
                if event.key == pygame.K_UP and self.octave < std_cfg.MAX_OCTAVE:
                    self.octave += 1
                if event.key == pygame.K_DOWN and self.octave > std_cfg.MIN_OCTAVE:
                    self.octave -= 1
        return None

    def check_keyboard(self) -> dict:
        """Check the state of the keyboard.

        Returns:
            dict: Dictionary of key states, where the key is the key name and the value is True if pressed,
            False otherwise

        """
        key_state = dict.fromkeys(auxil.keys, False)
        pressed_keys = pygame.key.get_pressed()
        for key in auxil.keys:
            key_state[key] = pressed_keys[key]
        return key_state


class NoteManager:
    """A class for managing notes in a song.

    Todo:
        * Add spawning of "bar lines"
        * Fix hard coded values for note spawning and removing

    """

    def __init__(self, song: Song, assets: GameAssets, play_margain: float, play_center: float) -> None:
        """Initialize the note manager.

        Args:
            song (Song): Song object being played
            assets (GameAssets): Assets object containing audio for notes
            play_margain (float): Width of the play area
            play_center (float): x-coordinate of the center of the play area

        """
        self.song = song
        self.assets = assets

        self.active_notes = []
        self.current_slot = -1  # because we only check on update
        self.current_bar = 0
        self.time_per_slot = 60 / (self.song.bpm * self.song.slots_per_bar / std_cfg.BEATS_PER_BAR)
        self.last_update_time = pygame.time.get_ticks() / 1000.0

        self.play_margain = play_margain
        self.play_center = play_center

    def check_note_spawn(self) -> None:
        """Check if delta t is enough to update slot and bar. Also spawn notes when updating."""
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.last_update_time >= self.time_per_slot:
            if (self.current_slot + 1) % self.song.slots_per_bar < self.current_slot:
                self.current_bar += 1
            self.current_slot = (self.current_slot + 1) % self.song.slots_per_bar
            self.last_update_time += self.time_per_slot
            self.spawn_note()

    def spawn_note(self) -> None:
        """Spawn notes for the current slot and bar."""
        notes = self.song.get_notes_for_time(self.current_bar + 1, self.current_slot + 1)
        for note in notes:
            if note.active is False:
                if note.pitch >= std_cfg.NOTE_MIRROR:
                    note.image = pygame.transform.flip(
                        self.assets.note_pictures[str(note.note_type)],
                        flip_x=True,
                        flip_y=True,
                    )
                    note.rect = note.image.get_rect(center=(1200, 260 - note.pitch * 10))
                else:
                    note.image = self.assets.note_pictures[str(note.note_type)]
                    note.rect = note.image.get_rect(center=(1200, 180 - note.pitch * 10))
                note.active = True
                self.active_notes.append(note)

    def update_notes(self, dt: float) -> float:
        """Update note positions on the screen, and remove notes that have been hit or are out of bounds.

        Args:
            dt (float): Time since last update

        """
        score = 0
        to_remove = [note for note in self.active_notes if note.hit or note.rect.x < 100]
        for note in to_remove:
            score += note.score
            self.active_notes.remove(note)
        for note in self.active_notes:
            note.rect.x -= dt * std_cfg.NOTE_VELOCITY
        return score

    def check_note_hit(self, key_state: dict, octave: int) -> None:
        """Check whether any notes in the active_notes list have been hit.

        Args:
            key_state (dict): _description_
            octave (int): _description_

        Returns:
            tuple[bool, int]: _description_

        """
        for note in self.active_notes:
            if note.hit or not (
                self.play_center - self.play_margain <= note.rect.centerx <= self.play_center + self.play_margain
            ):
                continue
            for key, playing in key_state.items():
                if (
                    playing
                    and auxil.key_dictionary[note.pitch % 7] == key
                    and (note.pitch // 7) + std_cfg.MIN_OCTAVE == octave
                ):
                    distance = abs(note.rect.centerx - self.play_center)
                    note.score = (
                        1000 if distance < self.play_margain / 3 else 500 if distance < self.play_margain / 2 else 100
                    )
                    note.hit = True

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the notes on the screen.

        Args:
            screen (pygame.Surface): The display surface for the game.

        """
        for note in self.active_notes:
            screen.blit(note.image, note.rect)
            if std_cfg.DEBUG_MODE:
                pygame.draw.circle(screen, auxil.RED, (note.rect.centerx, note.rect.centery), 5)
