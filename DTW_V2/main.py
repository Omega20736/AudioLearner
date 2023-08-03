import librosa
import threading

from DTW_V2.AudioFileReader import AudioFileReader
from DTW_V2.MusicCutter import MusicCutter
from DTW_V2.Recorder import Recorder

if __name__ == '__main__':
    reference_path = 'C:/Users/Omega/Music/MusicAI/(Spotify).mp3'
    reference_audio, sr = librosa.load(reference_path, sr=22050)

    test_audio_path = 'C:/Users/Omega/Music/MusicAI/Concert.mp3'  # Replace with your test audio file path
    reader = AudioFileReader(test_audio_path)

    #recorder = Recorder()
    cutter = MusicCutter(reference_audio)

    read_thread = threading.Thread(target=reader.read)
    process_thread = threading.Thread(target=cutter.process, args=(reader.queue,))

    #record_thread = threading.Thread(target=recorder.record)
    #process_thread = threading.Thread(target=cutter.process, args=(recorder.queue,))

    read_thread.start()
    #record_thread.start()
    process_thread.start()
