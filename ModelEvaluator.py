import numpy as np
from sklearn.metrics import accuracy_score, f1_score
from torch import nn
import torch
import os

from TextFileWriter import TextFileWriter


class ModelEvaluator:
    def __init__(self, model, preprocessor, data_reader):
        self.model = model
        self.preprocessor = preprocessor
        self.data_reader = data_reader
        self.loss_fn = nn.BCEWithLogitsLoss()
        self.writer = TextFileWriter()

    def load_model(self, path):
        if os.path.exists(path):
            self.model.load_state_dict(torch.load(path))
            self.model.eval()  # Set the model to evaluation mode
            print("Model loaded from {}".format(path))
        else:
            print("No existing model found. Please ensure that you have trained a model and saved it at the specified path.")

    def evaluate(self, audio_filepath, data_filepath):
        # Preprocess audio file
        spectrogram = self.preprocessor.preprocess(audio_filepath)
        spectrogram = spectrogram.float()
        spectrogram = spectrogram.unsqueeze(0)  # Add a batch dimension

        # Split the matrix into duration and notes tensor
        matrix = np.array(self.data_reader.parse(data_filepath))

        durations = torch.tensor(matrix[:, 0:1]).float()   # Duration tensor (60, 1)
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
        # loss_notes = self.loss_fn(notes_pred, notes_encoded)

        durations_pred = durations_pred.view(1, 60)  # Reshape to match the target
        loss_durations = nn.functional.mse_loss(durations_pred, durations)

        loss = loss_durations # loss_notes + loss_durations

        # Calculate accuracy and f1-score for notes
        # notes_pred_labels = (torch.sigmoid(notes_pred) > 0.5).float()
        # notes_accuracy = accuracy_score(notes_encoded.detach().numpy().flatten(),
        #                                 notes_pred_labels.detach().numpy().flatten())
        # notes_f1 = f1_score(notes_encoded.detach().numpy().flatten(), notes_pred_labels.detach().numpy().flatten())

        # Calculate MSE for durations
        durations_mse = nn.functional.mse_loss(durations_pred, durations).item()

        # print(f'Total Loss: {loss.item()}, Notes Accuracy: {notes_accuracy}, Notes F1 Score: {notes_f1}, Duration MSE: {durations_mse}')
        print(f'Total Loss: {loss.item()}, Duration MSE: {durations_mse}')

        # Prepare data for writing
        min_val = 0.75
        max_val = 1.25
        # notes_pred_labels = notes_pred.view(-1, 5, 97)
        notes_pred_labelstest = notes_encoded.view(-1, 5, 97)
        durations_pred_unnormalized = durations_pred * (max_val - min_val) + min_val
        durations_pred_unnormalizedtest = durations * (max_val - min_val) + min_val
        # note_indices = [[np.where(vec == 1)[0][0] if vec.sum() > 0 else -1 for vec in notes_pred_labels[i]] for i in
        #                 range(60)]
        note_indicestest = [[np.where(vec == 1)[0][0] if vec.sum() > 0 else -1 for vec in notes_pred_labelstest[i]] for i in
                        range(60)]
        duration_and_notes = [[durations_pred_unnormalized[0][i].item()] for i in range(60)] # [[durations_pred_unnormalized[0][i].item()] + note_indices[i] for i in range(60)]
        duration_and_notestest = [[durations_pred_unnormalizedtest[0][i].item()] + note_indicestest[i] for i in range(60)]

        # Write to file
        self.writer.write(duration_and_notes, audio_filepath + 'output.txt')
        self.writer.write(duration_and_notestest, audio_filepath + 'outputtest.txt')

