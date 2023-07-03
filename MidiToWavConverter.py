import os
import subprocess

from midi2audio import FluidSynth


class MidiToWavConverter:
    def __init__(self):
        # Path to the FluidSynth executable
        self.fluidsynth_path = 'C:/Program Files/Fluidsynth/bin/fluidsynth'

        # Path to the SoundFont file
        self.soundfont_path = 'C:/Program Files/Fluidsynth/FluidR3_GM.sf2'

    def convert(self, midi_path):
        # Generate the output path for the WAV file
        output_path = midi_path + '.wav'

        # Construct the command for MIDI to WAV conversion using FluidSynth
        command = [self.fluidsynth_path, '-ni', self.soundfont_path, midi_path + '.midi', '-F', output_path, '-r',
                   '44100']

        # Execute the command to convert MIDI to WAV
        with open(os.devnull, 'w') as f:
            subprocess.Popen(command, stdout=f, stderr=f).wait()

        return output_path