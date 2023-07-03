import random
from music21 import *

class PopinGenerator:
    # defining the stream
    s = stream.Stream()
    mm = tempo.MetronomeMark(number=120)
    s.insert(0, mm)

    with open('C:/Users/Omega/OneDrive/Documents/PythonScripts/Output' + '/chopin' + '.txt', 'w') as file:
        n = chord.Chord(["A3", "C#4", "A4"])
        note_names = ", ".join([note_obj.nameWithOctave for note_obj in n.pitches])
        file.write(f'Duration: 1.00, Notes: {note_names}\n')
        s.append(n)
        n = chord.Chord(["C#4", "E4", "C#4", "E4", "D4"])
        note_names = ", ".join([note_obj.nameWithOctave for note_obj in n.pitches])
        file.write(f'Duration: 1.00, Notes: {note_names}\n')
        s.append(n)
        n = chord.Chord(["F#4", "D4", "G#4", "D4", "A4"])
        note_names = ", ".join([note_obj.nameWithOctave for note_obj in n.pitches])
        file.write(f'Duration: 1.00, Notes: {note_names}\n')
        s.append(n)


    s.write('midi', fp='C:/Users/Omega/OneDrive/Documents/PythonScripts/Output' + '/chopin' + '.midi')