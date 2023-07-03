import torch
from Model import OnsetDetectionModel  # Import your model

class Trainer:
    def __init__(self, audio_sample, epochs=10, learning_rate=0.001):
        self.audio_sample = audio_sample
        self.epochs = epochs
        self.learning_rate = learning_rate

        # Load model
        self.model = OnsetDetectionModel()
        if torch.cuda.is_available():
            self.model.cuda()

        # Define the loss function and optimizer
        self.criterion = torch.nn.BCELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)


    def train(self):
        self.model.train()

        # Prepare audio sample for the model
        audio_sample_tensor = torch.from_numpy(self.audio_sample).float().unsqueeze(0)
        if torch.cuda.is_available():
            audio_sample_tensor = audio_sample_tensor.cuda()

        # Create a fake label for now
        label = torch.tensor([0]).float()
        if torch.cuda.is_available():
            label = label.cuda()

        for epoch in range(self.epochs):
            # Zero the parameter gradients
            self.optimizer.zero_grad()

            # Forward + backward + optimize
            outputs = self.model(audio_sample_tensor)
            loss = self.criterion(outputs, label)
            loss.backward()
            self.optimizer.step()

            # Print loss for this epoch
            print(f'Epoch {epoch+1}/{self.epochs}, Loss: {loss.item()}')

        print('Finished Training')
