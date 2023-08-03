import numpy as np
import librosa
from queue import Queue


class AudioFileReader:
    def __init__(self, audio_file_path, fs=44100, channels=2, duration=1):
        self.fs = fs
        self.channels = channels
        self.duration = duration
        self.queue = Queue()

        # Load audio file
        self.audio_data, _ = librosa.load(audio_file_path, sr=self.fs)

    def read(self):
        # Calculate the number of chunks based on duration
        num_chunks = len(self.audio_data) // (self.fs * self.duration)

        for i in range(num_chunks):
            # Cut audio data into chunks of the specified duration and add to queue
            start = i * self.fs * self.duration
            end = (i + 1) * self.fs * self.duration
            chunk = self.audio_data[start:end]
            self.queue.put(chunk)

        # If there is remaining data, add it to the queue as well
        remaining_data = self.audio_data[num_chunks * self.fs * self.duration:]
        if len(remaining_data) > 0:
            self.queue.put(remaining_data)