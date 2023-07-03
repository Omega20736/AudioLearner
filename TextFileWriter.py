import numpy as np

class TextFileWriter:
    def __init__(self):
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.duration_min = 0.75
        self.duration_max = 1.25

    def indices_to_notes(self, indices):
        notes = []
        for i in indices:
            if i != -1:  # assuming -1 is a placeholder for no note
                notes.append(self.note_index_to_note_octave(i))
            else:
                continue  # Skip -1 indices
        return ', '.join(notes)

    def note_index_to_note_octave(self, index):
        index -= 1  # accounting for 1-based indexing in note_octave_to_index()
        octave = index // 12 + 1
        note = self.note_names[index % 12]
        return note + str(octave)

    def write(self, matrix, file_path):
        with open(file_path, 'w') as file:
            for row in matrix:
                # reverse normalization of duration
                duration = row[0]

                # convert one-hot encoded notes back to note indices
                note_indices = [int(i) for i in row[1:]]

                notes = self.indices_to_notes(note_indices)
                line = f'Duration: {duration}, Notes: {notes}\n'
                file.write(line)
