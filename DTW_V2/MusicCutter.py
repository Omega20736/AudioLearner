import librosa
import numpy as np
from librosa.effects import time_stretch

from DTW_V2.DTWChromaAligner import DTWChromaAligner


class MusicCutter:
    def __init__(self, reference_audio, fs=22050, duration=1):
        self.fs = fs
        self.duration = duration
        self.timer = 0.0
        self.reference_audio = reference_audio
        self.aligner = DTWChromaAligner()

    def process(self, queue):
        while self.timer * self.fs < len(self.reference_audio):
            live_performance = queue.get()

            # Current time stamp for reference audio cut
            timestamp = int(self.timer * self.fs)

            # Default duration in samples
            duration_samples = int(self.duration * self.fs)

            # Get the reference cut based on current timestamp and duration
            cut_reference = self.reference_audio[timestamp:timestamp + duration_samples]

            # Align the live performance and reference audio and compute time difference
            distance, path = self.aligner.align(np.array(live_performance).flatten(), cut_reference)
            time_differences = self.aligner.get_time_differences_and_pitches(path)

            # Get the time difference of the last pitch pair
            time_diff = time_differences[-1] if time_differences else 0

            # Adjust timer for the next interval
            self.timer = self.timer + 1 + time_diff

            print(f"time_diff: {time_diff} seconds")
            print(f"Current Timer: {self.timer} seconds")

