import torch
from torch import nn


class AudioTextNet(nn.Module):
    def __init__(self, num_classes):
        super(AudioTextNet, self).__init__()

        # CNN for Spectrogram
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 16, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )

        # LSTM for Chord/Duration sequence
        self.lstm = nn.LSTM(input_size=100, hidden_size=128, num_layers=2, batch_first=True)

        # Fully connected layer for final output
        self.fc = nn.Linear(32 * 8 * 8 + 128, num_classes)

    def forward(self, spectrogram, chord_sequence):
        # Pass spectrogram through CNN
        cnn_out = self.cnn(spectrogram)
        cnn_out = cnn_out.view(cnn_out.size(0), -1)  # Flatten CNN output to feed it into FC layer

        # Pass chord sequence through LSTM
        lstm_out, _ = self.lstm(chord_sequence)
        lstm_out = lstm_out[:, -1, :]  # We only need the final output of the LSTM

        # Concatenate CNN and LSTM outputs
        out = torch.cat((cnn_out, lstm_out), dim=1)

        # Pass through fully connected layer to get final output
        out = self.fc(out)

        return out
