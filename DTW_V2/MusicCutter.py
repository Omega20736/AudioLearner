import librosa
import numpy as np
from librosa.effects import time_stretch

from DTW_V2.DTWChromaAligner import DTWChromaAligner


class MusicCutter:
    def __init__(self, reference_audio, fs=44100, duration=1):
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
            pitch_pairs = self.aligner.get_time_differences_and_pitches(path)

            # Get the time difference of the last pitch pair
            time_diff = pitch_pairs[-1][1] if pitch_pairs else 0

            # Adjust timer for the next interval
            self.timer += 1 + time_diff

            # Modify duration for the next reference audio interval
            if time_diff < 0:
                # If live performance is ahead, we squeeze (speed up) the reference
                cut_reference = librosa.effects.time_stretch(y=cut_reference, rate=1 / (1 + time_diff))
            else:
                # If live performance is slower, we stretch (slow down) the reference
                duration_samples = int(self.duration * self.fs * (1 + time_diff))
                # Cut the next reference audio interval with updated duration
                cut_reference = self.reference_audio[timestamp:timestamp + duration_samples]
                # Pad the rest with empty noise (zeroes)
                if len(cut_reference) < duration_samples:
                    cut_reference = np.pad(cut_reference, (0, duration_samples - len(cut_reference)))

            for i, (pitch, time_diff) in enumerate(pitch_pairs):
                print(f"Step {i}: Pitch: {pitch}, Time difference: {time_diff} seconds")

            print(f"Current Timer: {self.timer} seconds")

