from Summary.AudioQeueu import AudioQueue
import soundfile as sf

file_location = 'C:/Users/Omega/Music/MusicAI/trimmed_Concert.mp3'
audio_queue = AudioQueue()
segments_queue = audio_queue.split_audio(file_location)
i = 0
while not segments_queue.empty():
    segment = segments_queue.get()
    output_file_location = f'C:/Users/Omega/Music/MusicAI/SplitAudio/output_segment_{i}.mp3'
    sf.write(output_file_location, segment, audio_queue.sr)
    print(f"Segment {i} saved to: {output_file_location}")
    i += 1