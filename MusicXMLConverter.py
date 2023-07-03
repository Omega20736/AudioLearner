from music21 import converter, tempo


class MusicXMLConverter:

    @staticmethod
    def converter():
        # Load the MusicXML file
        #score = converter.parse('C:/Users/Omega/OneDrive/Documents/PythonScripts/MusicXML/040-1a-BH-001.musicxml')

        # Convert the score to MIDI
        #midi_file_path = 'C:/Users/Omega/OneDrive/Documents/PythonScripts/MusicXML/test.mid'
        #score.write('midi', fp=midi_file_path)

        # Load the MIDI file
        midi_file_path = 'C:/Users/Omega/OneDrive/Documents/PythonScripts/MusicXML/test.mid'
        score = converter.parse(midi_file_path)

        # Get the tempo indications from the MIDI file
        tempo_indications = score.flat.getElementsByClass(tempo.MetronomeMark)

        # Modify the tempo of the MIDI file
        for tempo_indication in tempo_indications:
            tempo_indication.number = 120  # Change the number to the desired tempo (e.g., 60 for slower tempo)

        # Write the modified MIDI file
        output_midi_file_path = 'C:/Users/Omega/OneDrive/Documents/PythonScripts/MusicXML/test-slower.mid'
        score.write('midi', fp=output_midi_file_path)