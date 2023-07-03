import soundfile as sf
from multiprocessing import Process, Queue
import time

class Processor:
    def __init__(self, queue, fs=44100):
        self.queue = queue
        self.fs = fs

    def process(self):
        i = 0;
        while True:
            if not self.queue.empty():  # There's a recording in the queue
                filename, recording = self.queue.get()  # Get the filename and recording from the queue
                print(f"Processing {filename} ...")
                filename = f'output_{i}.wav'
                sf.write('C:/Users/Omega/OneDrive/Documents/PythonScripts/AudioLearner/' + filename, recording, self.fs)  # Write the recording to file
                print(f"File {filename} processed.")
                i += 1
                time.sleep(3)  # Simulate CPU-heavy processing by sleeping