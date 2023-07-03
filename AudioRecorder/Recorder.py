import sounddevice as sd
import numpy as np
import time


class Recorder:
    def __init__(self, queue, fs=44100, duration=5, channels=2):
        self.queue = queue
        self.fs = fs
        self.duration = duration
        self.channels = channels
        self.recording = np.zeros((fs * duration, channels))  # Pre-allocate an array to hold the audio data
        self.idx = 0  # Index to keep track of where to insert new data in the recording array

    def callback(self, indata, frames, time, status):
        # This function is called for every chunk of audio data that is available.
        # It updates the recording array with the new audio data

        # Calculate remaining space in the recording array
        remaining_space = self.fs * self.duration - self.idx

        # Calculate number of frames to add
        frames_to_add = min(frames, remaining_space)

        # Add frames to the recording array
        self.recording[self.idx:self.idx + frames_to_add] = indata[:frames_to_add]
        self.idx += frames_to_add

        # Check if the recording array is full
        if self.idx >= self.fs * self.duration:
            print("Recording complete, adding to queue...")
            self.queue.put((f'output.wav', self.recording.copy()))  # Add the filename and recording to the queue
            self.recording[:] = 0  # Clear the recording
            self.idx = 0  # Reset the index

    def record_and_send(self):
        with sd.InputStream(callback=self.callback, channels=self.channels, samplerate=self.fs):
            while True:
                time.sleep(0.1)  # This is just to keep the program running
        print("Recording stopped")