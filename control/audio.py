import speech_recognition as sr
from contextlib import contextmanager
from .config import Config, resolve_config
import atexit
from typing import Callable


class Listener:
    def __init__(self, config: Config = None):
        self.config = resolve_config(config)
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self._calibrated = False

    def calibrate(self, source):
        self.r.adjust_for_ambient_noise(source)
        self._calibrated = True

    def __enter__(self):
        self.source = self.m.__enter__()
        if not self._calibrated:
            self.calibrate(self.source)

        return self

    def listen(self):
        audio = self.r.listen(self.source, phrase_time_limit=self.config.listen_timeout)
        return audio

    def __exit__(self, type, value, traceback):
        return self.m.__exit__(type, value, traceback)

    def listen_in_background(
        self, callback: Callable[[sr.Recognizer, sr.AudioData], None]
    ):
        with self.m as source:
            self.calibrate(source)

        print("Listening in background")
        stop_listening = self.r.listen_in_background(self.m, callback)
        atexit.register(stop_listening, wait_for_stop=False)
