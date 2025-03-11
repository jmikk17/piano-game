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
            pitch (int): Pitch/octave of the note

        """
        self.bar = bar
        self.slot = slot
        self.note_type = note_type
        self.pitch = pitch

        self.active = False
        self.hit = False
        self.missed = False

        self.rect = None
        self.image = None

    def __repr__(self) -> str:
        """Return a string representation of the note, mainly for debugging purposes."""
        return f"Note(slot={self.slot}, type={self.note_type}, pitch={self.pitch})"


class Song:
    """A class representing a song with notes to play.

    Attributes:
        bpm (int): BPM of the song
        slots_per_bar (int): Slots per bar of the song
        notes (list[Note]): List of notes in the song
        b_path (str | None): Path to the b-track for the song

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
    def __init__(self, song, assets, play_center, play_margain, play_b_time):
        self.assets = assets
        self.song = Song.from_json(song)
        self.play_center = play_center
        self.play_margain = play_margain
        self.play_b_time = play_b_time

        if self.song.b_path:
            self.b_track = pygame.mixer.Sound(resource_path("audio/" + self.song.b_path))
        self.b_playing = False

        self.play_state = {key: False for key in auxil.keys}
        self.octave = 5

        self.score = 0

        self.current_slot = -1
        self.current_bar = 0
        self.time_per_slot = 60 / (self.song.bpm * self.song.slots_per_bar / std_cfg.BEATS_PER_BAR)  # Seconds per slot
        self.start_time = pygame.time.get_ticks() / 1000.0  # Current time in seconds
        self.last_update_time = self.start_time

        self.active_notes = []
        self.line_spawned = False

    def check_note_spawn(self) -> None:
        """Check if it is time to spawn notes."""
        current_time = pygame.time.get_ticks() / 1000.0

        if current_time - self.last_update_time >= self.time_per_slot:
            if (self.current_slot + 1) % self.song.slots_per_bar < self.current_slot:
                self.current_bar += 1
            self.current_slot = (self.current_slot + 1) % self.song.slots_per_bar
            self.last_update_time += self.time_per_slot
            self.spawn_notes()
        if self.song.b_path and (current_time - self.start_time >= self.play_b_time and not self.b_playing):
            self.b_playing = True
            self.b_track.play()

    def check_line_spawn(self) -> None:
        current_time = pygame.time.get_ticks() / 1000.0
        if self.line_spawned is False:
            if (
                self.current_slot is std_cfg.SLOTS_PER_BAR - 1
                and current_time - self.last_update_time >= self.time_per_slot / 2
            ):
                self.spawn_line()
                self.line_spawned = True
        elif self.current_slot == 0:
            self.line_spawned = False

    def spawn_notes(self) -> None:
        notes = self.song.get_notes_for_time(self.current_bar + 1, self.current_slot + 1)
        for note in notes:
            if note.active is False:
                if note.pitch > 6:
                    # could potentially move this to init of a note
                    # at least image, so we can preprocess line/noline and transform
                    note.image = pygame.transform.flip(self.assets.note_pictures[str(note.note_type)], True, True)
                    note.rect = note.image.get_rect(center=(1200, 260 - note.pitch * 10))
                else:
                    note.image = self.assets.note_pictures[str(note.note_type)]
                    note.rect = note.image.get_rect(center=(1200, 180 - note.pitch * 10))
                note.active = True
                self.active_notes.append(note)

    def update_notes(self, dt) -> None:
        to_remove = []
        for note in self.active_notes:
            note.rect.x -= dt * std_cfg.NOTE_VELOCITY
            if note.hit:
                to_remove.append(note)
            elif note.rect.x < 100 and note.hit:
                note.missed = True
                to_remove.append(note)
        for note in to_remove:
            self.active_notes.remove(note)

    def play_notes(self, key_state) -> None:
        for key, is_pressed in key_state.items():
            if is_pressed and not self.play_state[key]:
                self.play_state[key] = True
                if self.octave == 5:
                    self.assets.note_sounds_5[key].play()
                elif self.octave == 6:
                    self.assets.note_sounds_6[key].play()
                hit, score = self.check_note_hit(key)
                if hit:
                    self.score += score
            elif not is_pressed:
                self.play_state[key] = False
                self.assets.note_sounds_5[key].fadeout(std_cfg.FADEOUT)
                self.assets.note_sounds_6[key].fadeout(std_cfg.FADEOUT)

    def check_note_hit(self, key):
        for note in self.active_notes:
            if note.hit or note.missed:
                continue

                # %7 or (+1)%7 here?????
            if (
                auxil.key_dictionary[note.pitch % 7] == key
                and
                # self.play_center - self.play_margain <= note.rect.centerx-5 <= self.play_center + self.play_margain):
                self.play_center - self.play_margain <= note.rect.centerx <= self.play_center + self.play_margain
            ):
                # -5 is manual adjustment for pictures, probalby doesnt scale well?

                # Calculate score based on accuracy
                # distance = abs(note.rect.centerx - self.play_center)
                distance = abs(note.rect.centerx - self.play_center)
                if distance < self.play_margain / 3:
                    note.score = 1000  # Perfect
                elif distance < self.play_margain / 2:
                    note.score = 500  # Good
                else:
                    note.score = 100  # OK

                note.hit = True

                return True, note.score

        return False, 0  # No note hit

    def spawn_line(self):
        # TODO
        pass

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.b_playing:
                        self.b_track.stop()
                    return "QUIT_TO_MENU"
                if event.key == pygame.K_UP:
                    if self.octave < 6:
                        self.octave += 1
                    print(self.octave)
                if event.key == pygame.K_DOWN:
                    if self.octave > 5:
                        self.octave -= 1
                    print(self.octave)
        return None

    def draw(self, screen):
        for note in self.active_notes:
            screen.blit(note.image, note.rect)
            if std_cfg.DEBUG_MODE:
                # Red circle for debug
                pygame.draw.circle(screen, auxil.RED, (note.rect.centerx, note.rect.centery), 5)

    def update(self, dt, key_state):
        status = self.handle_input()
        self.play_notes(key_state)
        self.check_note_spawn()
        self.check_line_spawn()
        self.update_notes(dt)
        return status


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
                self.assets.note_sounds[octave][key].play()
            elif not is_pressed:
                for octave_key in self.assets.note_sounds:
                    self.assets.note_sounds[octave_key][key].fadeout(std_cfg.FADEOUT)


class InputHandler:
    """A class for managing input during a song.

    Methods:
        handle_input: Handle input during a song, such as changing octave or quitting

    """

    # How to handle octave? And b_track? Attributes here or in musicplayer?

    def __init__(self) -> None:
        """Set the initial octave to 5."""
        self.octave = 5

    def handle_input(self, b_playing, b_track):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if b_playing:
                        b_track.stop()
                    return "QUIT_TO_MENU"
                if event.key == pygame.K_UP and self.octave < 6:
                    self.octave += 1
                if event.key == pygame.K_DOWN and self.octave > 5:
                    self.octave -= 1
        return None


class NoteManager:
    def __init__(self, song, assets):
        self.song = song
        self.assets = assets

        self.active_notes = []
        self.current_slot = -1  # because we only check on update?
        self.current_bar = 0
        self.time_per_slot = 60 / (self.song.bpm * self.song.slots_per_bar / std_cfg.BEATS_PER_BAR)
        self.last_update_time = pygame.time.get_ticks() / 1000.0
