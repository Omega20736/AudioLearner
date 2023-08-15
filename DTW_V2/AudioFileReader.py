import numpy as np
import librosa
from queue import Queue

class AudioFileReader:
    def __init__(self, audio_file_path, fs=22050, channels=2, duration=1):
        self.fs = fs
        self.channels = channels
        self.duration = duration
        self.queue = Queue()

        # Load audio file in stereo
        self.audio_data, _ = librosa.load(audio_file_path, sr=self.fs, mono=False)

    def read(self):
        # Check if the audio is stereo or mono. If mono, make it stereo for consistency
        if len(self.audio_data.shape) == 1:
            self.audio_data = np.tile(self.audio_data[:, np.newaxis], (1, 2))

        # Calculate the number of chunks based on duration
        num_samples_per_chunk = self.fs * self.duration
        num_chunks = len(self.audio_data[0]) // num_samples_per_chunk  # Using [0] since it's a stereo signal

        for i in range(num_chunks):
            # Cut audio data into chunks of the specified duration and add to queue
            start = i * num_samples_per_chunk
            end = (i + 1) * num_samples_per_chunk
            chunk = self.audio_data[:, start:end]
            self.queue.put(chunk.T)  # Transpose to make it consistent with Recorder's output

        # If there is remaining data, add it to the queue as well
        remaining_data = self.audio_data[:, num_chunks * num_samples_per_chunk:]
        if remaining_data.shape[1] > 0:
            self.queue.put(remaining_data.T)
