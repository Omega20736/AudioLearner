import random
from music21 import *


class MusicCreator:
    # Predefining notes
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octaves = range(1, 8)

    @staticmethod
    def random_pitch():
        name = random.choice(MusicCreator.note_names)
        octave = random.choice(MusicCreator.octaves)
        return note.Note(name + str(octave))

    @staticmethod
    def compose(saveLocation, fileNumber, BPM, durationTimeMin, durationTimeMax):
        # defining the stream
        s = stream.Stream()
        mm = tempo.MetronomeMark(number=BPM)
        s.insert(0, mm)

        # Appending notes time length approx 1 min / metronomMark
        t = 0
        with open(saveLocation + '/Audio' + str(fileNumber) + '.txt', 'w') as file:
            while t < 60:
                durationTime = random.uniform(durationTimeMin, durationTimeMax)
                if random.randint(0, 1000) == 1:
                    n = note.Rest()
                    file.write(f'Duration: {durationTime}, Notes: Rest \n')
                else:
                    chordsAmount = 5 # random.randint(1, 5)
                    notes = [MusicCreator.random_pitch() for _ in range(chordsAmount)]
                    n = chord.Chord(notes)
                    note_names = ", ".join([note_obj.nameWithOctave for note_obj in n.pitches])
                    file.write(f'Duration: {durationTime}, Notes: {note_names}\n')
                n.quarterLength = durationTime
                s.append(n)
                t += 1

        # s.show()
        s.write('midi', fp=saveLocation + '/Audio' + str(fileNumber) + '.midi')

        return saveLocation + '/Audio' + str(fileNumber)
