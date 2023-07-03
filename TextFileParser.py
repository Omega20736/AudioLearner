class TextFileParser:
    def __init__(self):
        self.duration_min = 0.75
        self.duration_max = 1.25
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.index_to_note = {index: note for index, note in enumerate(self.note_names)}

    def parse(self, file_path):
        matrix = []
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                duration_index = line.index("Duration:")
                notes_index = line.index("Notes:")
                duration = float(line[duration_index + 9: notes_index].strip().rstrip(","))
                normalized_duration = self.normalize_duration(duration)  # Normalize duration her
                notes = line[notes_index + 6:].strip()

                row = [normalized_duration] + self.notes_to_indices(notes)
                matrix.append(row)

        return matrix

    def notes_to_indices(self, notes):
        indices = [-1] * 5  # Update to 5 columns for note indices (including the duration column)
        if notes != "Rest":
            notes_list = notes.split(", ")
            for i, note in enumerate(notes_list):
                pitch = note[:-1]  # remove the octave number
                octave = int(note[-1])
                index = self.note_octave_to_index(pitch, octave)
                indices[i] = index
        return indices

    def note_octave_to_index(self, pitch, octave):
        note_index = self.note_names.index(pitch)
        return (note_index + 1) + (octave - 1) * 12

    def index_to_note_octave(self, index):
        note_index = (index - 1) % 12
        octave = (index - 1) // 12 + 1
        return self.index_to_note[note_index] + str(octave)

    def normalize_duration(self, duration):
        return (duration - self.duration_min) / (self.duration_max - self.duration_min)

