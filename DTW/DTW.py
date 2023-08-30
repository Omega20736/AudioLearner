import numpy as np
import librosa
from dtw import *

def detect_onsets(audio_file, start_time=0.0):
    # Load the audio file
    y, sr = librosa.load(audio_file)

    # Calculate the sample to start from
    start_sample = int(start_time * sr)

    # Trim the start of the audio file
    y = y[start_sample:]

    # Detect onsets
    onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')

    return onsets

#def detect_onsets(audio_file):
#    y, sr = librosa.load(audio_file)
#    onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')
#    print(f"Onsets shape for {audio_file}: {onsets.shape}")  # This should print: (n,) for some integer n
#    return onsets

# Load onsets
# change directories here
# Chopin
reference_onsets = detect_onsets('C:/Users/Omega/Music/MusicAI/Concert.mp3', start_time=1.0)
played_onsets = detect_onsets('C:/Users/Omega/Music/MusicAI/(Spotify).mp3', start_time=7.8)

# Siciliano
#reference_onsets = detect_onsets('C:/Users/Omega/Music/MusicAI/langSiciliano.mp3', start_time=3.0)
#played_onsets = detect_onsets('C:/Users/Omega/Music/MusicAI/SicilianoBWV1031.mp3', start_time=3.5)

# Create the sequences
s1 = np.array(reference_onsets, ndmin=2).T
s2 = np.array(played_onsets, ndmin=2).T

# Compute DTW
alignment = dtw(s1, s2)

# Compute timing differences
for ref_index, play_index in zip(alignment.index1, alignment.index2):
    timing_difference = played_onsets[play_index] - reference_onsets[ref_index]
    print(f'Note {ref_index}:')
    print(f'\tReference onset time: {reference_onsets[ref_index]} seconds')
    print(f'\tPlayed onset time: {played_onsets[play_index]} seconds')
    print(f'\tTiming difference: {timing_difference} seconds')
