import numpy as np
import sounddevice as sd
from queue import Queue
import time


class Recorder:
    def __init__(self, fs=44100, channels=2, duration=1):
        self.fs = fs
        self.channels = channels
        self.duration = duration
        self.idx = 0
        self.queue = Queue()

    def record(self):
        self.recording = np.zeros((self.fs * self.duration, self.channels))
        with sd.InputStream(callback=self.callback, channels=self.channels, samplerate=self.fs):
            while True:
                time.sleep(self.duration)
                self.queue.put(self.recording.copy())
                self.recording[:] = 0

    def callback(self, indata, frames, time, status):
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
            self.queue.put(self.recording.copy())  # Only put the recording into the queue
            self.recording[:] = 0  # Clear the recording
            self.idx = 0  # Reset the index
