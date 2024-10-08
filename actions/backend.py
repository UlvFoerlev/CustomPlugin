from streamcontroller_plugin_tools import BackendBase
from pathlib import Path

try:
    import os

    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
    import pygame as pg
    from pygame.mixer import Sound, Channel
except ImportError as e:
    raise e


class Backend(BackendBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pg.mixer.init()
        pg.init()

        self.cached_sounds: dict[str, Sound] = {}

    def preload_sound(self, path: str | Path) -> bool:
        key = path if isinstance(path, str) else str(path)

        try:
            self.cached_sounds[key] = pg.mixer.Sound(path)
        except (pg.error, FileNotFoundError):
            return False

        return True

    def play_sound(
        self,
        path: str | Path,
        volume: float = 100.0,
        loops: int = 0,
        fade_in: float = 0.0,
        immediate_fade_out: float = 0.0,
    ) -> tuple[Sound | None, Channel | None]:
        key = path if isinstance(path, str) else str(path)

        if key not in self.cached_sounds:
            valid = self.preload_sound(path=path)
            if not valid:
                return None, None

        sound = self.cached_sounds[key]
        real_volume = max(min((volume / 100.0), 1.0), 0.0)
        sound.set_volume(real_volume)
        channel = sound.play(loops=loops, fade_ms=int(fade_in * 1000))
        if immediate_fade_out:
            sound.fadeout(int(immediate_fade_out * 1000))

        return sound, channel


backend = Backend()
