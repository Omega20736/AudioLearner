import mido
from mido import Message, MidiFile, MidiTrack


class TextToMidi:
    def __init__(self, file_path):
        self.file_path = 'C:/Users/Omega/Music/MusicAI/NotenBach.txt'

    def convert_to_midi(self):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        with open(self.file_path, 'r') as f:
            lines = f.readlines()

            for i, line in enumerate(lines):
                if i == 0:
                    continue

                data = line.strip().split('\t')

                note = int(data[11])
                velocity = int(data[3])
                time = int(data[9])

                track.append(Message('note_on', note=note, velocity=velocity, time=time))
                track.append(Message('note_off', note=note, velocity=velocity, time=time))

        mid.save('output.mid')


# Usage
file_path = 'path_to_your_txt_file.txt'
converter = TextToMidi(file_path)
converter.convert_to_midi()