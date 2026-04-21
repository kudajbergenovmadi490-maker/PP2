"""
player.py - Music Player logic.
Manages a playlist, playback state, and pygame.mixer interaction.
"""

import os
import pygame


class MusicPlayer:
    """
    Encapsulates playlist management and audio playback.

    Attributes:
        tracks      : list of absolute file paths
        current_idx : index of the currently selected track
        is_playing  : True while a track is actively playing
    """

    SUPPORTED_EXTENSIONS = (".mp3", ".wav", ".ogg", ".flac")

    def __init__(self, music_dir: str) -> None:
        """
        Scans *music_dir* for supported audio files and builds the playlist.

        Args:
            music_dir : path to the folder containing audio files
        """
        self.tracks: list[str] = []
        self.current_idx: int  = 0
        self.is_playing: bool  = False

        if not os.path.isdir(music_dir):
            print(f"[WARN] Music directory '{music_dir}' not found. "
                  "No tracks loaded.")
            return

        for fname in sorted(os.listdir(music_dir)):
            if fname.lower().endswith(self.SUPPORTED_EXTENSIONS):
                self.tracks.append(os.path.join(music_dir, fname))

        if self.tracks:
            print(f"[INFO] Found {len(self.tracks)} track(s) in '{music_dir}'")
        else:
            print(f"[WARN] No supported audio files found in '{music_dir}'.")

    # ── Playback controls ─────────────────────────────────────────────────────

    def play(self) -> None:
        """Starts or resumes playback of the current track."""
        if not self.tracks:
            return
        if not self.is_playing:
            pygame.mixer.music.load(self.current_track)
            pygame.mixer.music.play()
            self.is_playing = True
            print(f"[PLAY] {self.current_track_name}")

    def stop(self) -> None:
        """Stops playback entirely."""
        pygame.mixer.music.stop()
        self.is_playing = False
        print("[STOP]")

    def next_track(self) -> None:
        """Advances to the next track and starts playing."""
        if not self.tracks:
            return
        self.current_idx = (self.current_idx + 1) % len(self.tracks)
        self._reload_and_play()

    def prev_track(self) -> None:
        """Goes back to the previous track and starts playing."""
        if not self.tracks:
            return
        self.current_idx = (self.current_idx - 1) % len(self.tracks)
        self._reload_and_play()

    def _reload_and_play(self) -> None:
        """Internal helper – loads the current track and plays it."""
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.current_track)
        pygame.mixer.music.play()
        self.is_playing = True
        print(f"[PLAY] {self.current_track_name}")

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def current_track(self) -> str:
        """Full path of the currently selected track."""
        if not self.tracks:
            return ""
        return self.tracks[self.current_idx]

    @property
    def current_track_name(self) -> str:
        """Filename (without directory) of the current track."""
        return os.path.basename(self.current_track) if self.current_track else "—"

    @property
    def track_count(self) -> int:
        return len(self.tracks)

    @property
    def position_label(self) -> str:
        """Human-readable track counter, e.g. '2 / 5'."""
        if not self.tracks:
            return "0 / 0"
        return f"{self.current_idx + 1} / {self.track_count}"

    def get_playback_pos_ms(self) -> int:
        """Returns current playback position in milliseconds (0 if stopped)."""
        if self.is_playing:
            return pygame.mixer.music.get_pos()   # ms since play() was called
        return 0
