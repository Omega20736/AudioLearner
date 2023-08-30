from Summary.AudioCutter import AudioCutter
from Summary.AudioQeueu import AudioQueue
from Summary.ChromaDTW import DTWChromaAligner
import soundfile as sf
import sys


class AudioAligner:
    start_time = 0
    end_time = 1
    temp_ATD = 0
    ATD_sum = 0
    temp_path = 'C:/Users/Omega/Music/MusicAI/temp.mp3'
    def __init__(self):
        self.aligner = DTWChromaAligner()
        self.cutter = AudioCutter()
        self.audio_queue = AudioQueue()
    def align(self, path1, path2):
        # establish Audioqeueu
        segments_queue = self.audio_queue.split_audio(path1)
        total_segments = segments_queue.qsize()
        current_segment = 0

        while True:
            segment = segments_queue.get()
            current_segment += 1

            if current_segment == total_segments:
                print("Last Segment, time to kill")
                sys.exit(0)

            sf.write(AudioAligner.temp_path, segment, self.audio_queue.sr)

            # Cut audio
            cutPath = self.cutter.cut_audio(path2, AudioAligner.start_time, AudioAligner.end_time)

            # Align audios
            distance, path = self.aligner.align(AudioAligner.temp_path, cutPath)
            avg_time_diff = self.aligner.get_time_differences_and_pitches(path)

            # Adjust variables
            AudioAligner.start_time += 1 + AudioAligner.temp_ATD
            AudioAligner.end_time += 1 + avg_time_diff
            AudioAligner.temp_ATD = avg_time_diff
            AudioAligner.ATD_sum += avg_time_diff

            print(
                f"new Start time: {AudioAligner.start_time}, new End time Difference: {AudioAligner.end_time}, summed Average Time Difference: {AudioAligner.ATD_sum}")

            if segments_queue.empty():
                break




        return AudioAligner.ATD_sum
