import torch
import numpy as np
from torch import nn

class OnsetDetectionNet(nn.Module):
    def __init__(self):
        super(OnsetDetectionNet, self).__init__()

        # CNN for Spectrogram
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 16, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),  # Flatten the output for the fully connected layer
            nn.Linear(512, 512),  # A fully connected layer
            nn.ReLU()
        )

        # Fully connected layers for the final output
        # self.fc1 = nn.Linear(512, 60 * 5 * 97)  # One output for each note in each chord
        self.fc2 = nn.Linear(512, 60)  # One output for each chord duration

    def forward(self, spectrogram):
        # Pass spectrogram through CNN
        cnn_out = self.cnn(spectrogram)

        # Pass through fully connected layers to get final outputs
        # notes_logits = self.fc1(cnn_out)
        durations_out = self.fc2(cnn_out)

        return durations_out # notes_logits, durations_out
