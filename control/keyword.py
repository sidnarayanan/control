import pickle
from typing import List, Union

import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from python_speech_features import mfcc
from dtw import dtw

from .config import resolve_config, Config


class Keyword:
    def __init__(self, name: str):
        """MFCC-based keyword class

        Args:
            name (str): Name of this keyword.
        """
        self.name = name

        self.mfccs = []

    @staticmethod
    def audio_to_mfcc(audio: sr.AudioData) -> np.ndarray:
        """Convert an audio sample into MFCCs

        Args:
            audio (sr.AudioData): Audio sample

        Returns:
            np.ndarray: MFCC array
        """
        wav_data = audio.get_wav_data()
        # there's probably a cleaner way of getting the rate:
        with open(f"/tmp/tmp_calibrate.wav", "wb") as fwav:
            fwav.write(wav_data)
        rate, sig = wav.read("/tmp/tmp_calibrate.wav")
        mfccs = mfcc(sig, rate)
        return mfccs

    def add_calibration_sample(self, audio: sr.AudioData):
        """Add a reference sample for this keyword.

        Args:
            audio (sr.AudioData): Audio sample used as
                an example of this keyword
        """
        mfccs = self.audio_to_mfcc(audio)
        self.mfccs.append(mfccs)

    def score_audio(self, audio: sr.AudioData) -> float:
        """
        Given a new audio sample, score its similarity to the
        reference keyword. Dynamic time warping is used to align
        the MFCCs, and we use the unnormalized euclidean distance
        of the alignment as the distance metric. The mean distance
        among references is the similarity score.

        Args:
            audio (sr.AudioData): New audio sample

        Returns:
            float: Distance
        """
        query = self.audio_to_mfcc(audio)

        dists = []
        for ref in self.mfccs:
            dists.append(dtw(query, ref).distance)

        return np.mean(dists)


class KeywordSet(dict):
    def __init__(self, config: Config = None):
        if config is not None:
            self.load(config)
        self.config = resolve_config(config)

    def summarize(self):
        for name, kw in self.items():
            print(f"{name}: {len(kw.mfccs)} samples")

    def __getitem__(self, key) -> Keyword:
        try:
            return super().__getitem__(self, key)
        except KeyError:
            raise KeyError(f'"{key}" is not a known keyword') from None

    def add(self, keyword: Keyword):
        self[keyword.name] = keyword

    def save(self, config: Config):
        with open(f"{config.config_path}/keywords.pkl", "wb") as fpkl:
            pickle.dump(dict(self), fpkl)

    def load(self, config: Config):
        try:
            with open(f"{config.config_path}/keywords.pkl", "rb") as fpkl:
                self.update(pickle.load(fpkl))
        except FileNotFoundError:
            print("No keyword cache found")

    def score_audio(self, audio: sr.AudioData) -> Union[str, None]:
        """Try to find the best keyword match to an audio sample

        Args:
            audio (sr.AudioData): An audio sample.

        Returns:
            Union[str, None]: The best keyword match, determined by
                the keyword with the smallest score. If the best match's
                score is greater than config.keyword_match_threshold, then
                None is returned (no successful match).
        """
        scores = [(kw.score_audio(audio), kw.name) for kw in self.values()]
        print(scores)
        best_score, best_key = min(scores)
        if best_score > self.config.keyword_match_threshold:
            return None
        else:
            return best_key
