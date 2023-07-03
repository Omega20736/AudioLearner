import torch
import librosa
import numpy as np

class AudioPreprocessor:
    def __init__(self, sample_rate=22050, duration=5, n_mfcc=64):
        self.sample_rate = sample_rate
        self.duration = duration
        self.n_mfcc = n_mfcc
        self.hop_length = int(sample_rate * duration / (n_mfcc - 1))  # to make time dimension ~n_mfcc

    def preprocess(self, file_path):
        # Load the audio file
        signal, sr = librosa.load(file_path, sr=self.sample_rate, mono=False)

        # Convert to mono if necessary
        if len(signal.shape) > 1:
            signal = np.mean(signal, axis=0)

        # Ensure consistency of length
        if len(signal) > self.sample_rate * self.duration:
            signal = signal[:int(self.sample_rate * self.duration)]  # crop longer signals
        elif len(signal) < self.sample_rate * self.duration:
            signal = np.pad(signal, (0, int(self.sample_rate * self.duration) - len(signal)))  # pad shorter signals

        # Compute MFCCs
        mfccs = librosa.feature.mfcc(y=signal, sr=self.sample_rate, n_mfcc=self.n_mfcc, hop_length=self.hop_length)

        # Convert to PyTorch tensor and add a batch dimension
        mfccs_tensor = torch.from_numpy(mfccs).unsqueeze(0)

        return mfccs_tensor
