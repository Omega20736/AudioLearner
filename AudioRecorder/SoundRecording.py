import sounddevice as sd
import numpy as np
import soundfile as sf

class SoundRecording:
    fs = 44100
    duration = 5  # seconds

    #devices = sd.query_devices()
    #for i, device in enumerate(devices):
    #    print(f'Device ID: {i}, Device Name: {device["name"]}, Max Input Channels: {device["max_input_channels"]}')

    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, device=27)
    print("Recording Audio")
    sd.wait()
    print("Audio recording complete, Saving File")
    sf.write('C:/Users/Omega/OneDrive/Documents/PythonScripts/AudioLearner/test.wav', myrecording, fs)
    print("File saved")