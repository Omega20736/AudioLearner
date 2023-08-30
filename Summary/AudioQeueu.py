import librosa
import queue

import librosa
import queue


class AudioQueue:
    def __init__(self):
        self.sr = None

    def split_audio(self, file_location):
        # Load the audio file
        y, self.sr = librosa.load(file_location, sr=None)

        # Create a queue to store the 1-second segments
        segments_queue = queue.Queue()

        # Calculate the number of samples in 1 second
        samples_per_second = self.sr

        # Split the audio into 1-second segments and add them to the queue
        for start_sample in range(0, len(y), samples_per_second):
            end_sample = start_sample + samples_per_second
            segment = y[start_sample:end_sample]
            segments_queue.put(segment)

        return segments_queue
