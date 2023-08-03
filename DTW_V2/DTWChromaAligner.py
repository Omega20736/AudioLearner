import numpy as np
import librosa
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw


class DTWChromaAligner:
    def __init__(self, sr=22050, hop_length=512):
        self.sr = sr
        self.hop_length = hop_length
        self.pitch_classes = 'C C# D D# E F F# G G# A A# B'.split()

    def compute_chroma(self, audio_data, sr=22050):
        # Ensuring the audio data is floating-point
        audio_data = audio_data.astype(np.float32)
        chroma = librosa.feature.chroma_stft(y=audio_data, sr=sr, hop_length=self.hop_length)
        return chroma

    def align(self, audio_data1, audio_data2):
        self.chroma1 = self.compute_chroma(audio_data1)
        self.chroma2 = self.compute_chroma(audio_data2)

        distance, path = fastdtw(self.chroma1.T, self.chroma2.T, dist=euclidean)

        return distance, path

    def get_time_differences_and_pitches(self, path):
        time_differences = []
        pitch_pairs = []
        for pair in path:
            time_diff = (pair[1] - pair[0]) * self.hop_length / self.sr
            time_differences.append(time_diff)

            pitch1 = self.pitch_classes[np.argmax(self.chroma1[:, pair[0]])]
            pitch2 = self.pitch_classes[np.argmax(self.chroma2[:, pair[1]])]

            if pitch1 == pitch2:
                pitch_pairs.append((pitch1, time_diff))

        return pitch_pairs
