import numpy as np
import librosa
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw


class DTWChromaAligner:
    def __init__(self, sr=22050, hop_length=512):
        self.sr = sr
        self.hop_length = hop_length
        self.pitch_classes = 'C C# D D# E F F# G G# A A# B'.split()

    def compute_chroma(self, audio_path):
        y, sr = librosa.load(audio_path, sr=self.sr)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=self.hop_length)
        return chroma

    def align(self, audio_path1, audio_path2):
        self.chroma1 = self.compute_chroma(audio_path1)
        self.chroma2 = self.compute_chroma(audio_path2)

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


# Instantiate the DTWChromaAligner class
aligner = DTWChromaAligner()

# Compute alignment
# Change directories here
distance, path = aligner.align('C:/Users/Omega/Music/MusicAI/(Spotify).mp3', 'C:/Users/Omega/Music/MusicAI/Concert.mp3') # Chopin
#distance, path = aligner.align('C:/Users/Omega/Music/MusicAI/langSiciliano.mp3', 'C:/Users/Omega/Music/MusicAI/SicilianoBWV1031.mp3') # Siciliano

# Compute time differences and pitches
pitch_pairs = aligner.get_time_differences_and_pitches(path)

# Print the time differences in seconds and the pitches
for i, (pitch, time_diff) in enumerate(pitch_pairs):
    print(f"Step {i}: Pitch: {pitch}, Time difference: {time_diff} seconds")


