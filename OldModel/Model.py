import torch
import torch.nn as nn


class OnsetDetectionModel(nn.Module):
    def __init__(self):
        super(OnsetDetectionModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        self.conv2 = nn.Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.bn2 = nn.BatchNorm2d(64)

        self.gru = nn.GRU(64, 32, bidirectional=True, batch_first=True)

        self.fc = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = x.unsqueeze(1)  # Add an extra dimension for CNN
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = x.permute(0, 2, 1, 3).contiguous()
        x = x.view(x.size(0), -1, self.conv2.out_channels)  # Reshape output for GRU layers

        x, _ = self.gru(x)  # GRU layer
        x = self.fc(x[:, -1, :])  # Fully connected layer
        x = self.sigmoid(x)

        return x