import speech_recognition as sr
from contextlib import contextmanager
from .config import Config, resolve_config


class Listener:
    def __init__(self, config: Config = None):
        self.config = resolve_config(config)

    def __enter__(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.source = self.m.__enter__()
        self.r.adjust_for_ambient_noise(self.source)

        return self

    def listen(self):
        audio = self.r.listen(self.source, phrase_time_limit=self.config.listen_timeout)
        return audio

    def __exit__(self, type, value, traceback):
        return self.m.__exit__(type, value, traceback)
