import os
import torch
import numpy as np
from torch import nn
from torch.optim import Adam

class ModelTrainer:
    def __init__(self, model, preprocessor, data_reader, learning_rate=0.00001,
                 model_path='C:/Users/Omega/OneDrive/Documents/PythonScripts/Model/Model'):
        self.model_path = model_path
        self.model = model  # Initialize with the model passed in
        self.preprocessor = preprocessor
        self.data_reader = data_reader
        # Create separate loss functions for notes and durations
        self.loss_fn_notes = nn.BCEWithLogitsLoss()
        self.loss_fn_durations = nn.MSELoss()

        self.optimizer = Adam(self.model.parameters(), lr=learning_rate)
        if not os.path.exists(self.model_path):  # if the model file doesn't exist
            torch.save(self.model.state_dict(), self.model_path)  # save the initial model
            print("Created a new model file at {}".format(self.model_path))

    def train(self, audio_filepath, data_filepath, epochs=1):
        # Load the model at the start of training
        self.model.load_state_dict(torch.load(self.model_path))
        print("Loaded model from {}".format(self.model_path))

        for epoch in range(epochs):
            # Preprocess audio file
            spectrogram = self.preprocessor.preprocess(audio_filepath)
            spectrogram = spectrogram.float()
            spectrogram = spectrogram.unsqueeze(0)  # Add a batch dimension

            # Split the matrix into duration and notes tensor
            matrix = np.array(self.data_reader.parse(data_filepath))

            durations = torch.tensor(matrix[:, 0:1]).float()  # Duration tensor (60, 1)
            notes = torch.tensor(matrix[:, 1:])  # Notes tensor (60, 5)

            # Reshape durations to match your model's output
            durations = durations.view(1, 60)

            # One-hot encoding for the notes tensor
            notes_encoded = torch.zeros((60, 5, 97))
            for t in range(60):
                for i in range(5):
                    note = notes[t, i]
                    if note != -1:  # assuming -1 is a placeholder for no note
                        notes_encoded[t, i, note.long()] = 1

            notes_encoded = notes_encoded.view(1, 60, 5*97)  # Reshape to (batch, time, features)

            # Pass data through the model
            durations_pred = self.model(spectrogram) # notes_pred, durations_pred = self.model(spectrogram)

            # Compute the loss
            # notes_pred = notes_pred.view(1, 60, 5 * 97)  # Reshape to match the target
            # loss_notes = self.loss_fn_notes(notes_pred, notes_encoded)

            durations_pred = durations_pred.view(1, 60)  # Reshape to match the target
            loss_durations = self.loss_fn_durations(durations_pred, durations)

            loss = loss_durations # loss_notes + loss_durations

            # Perform backpropagation and optimization
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            print(f'Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}')

        # Save the model after training
        self.save_model()

    def save_model(self, path=None):
        if path is None:
            path = self.model_path
        torch.save(self.model.state_dict(), path)
        print("Model saved to {}".format(path))
