import librosa
import soundfile as sf
import os


class AudioCutter:
    def cut_audio(self, file_location, start_time, end_time):
        # Load the audio file
        y, sr = librosa.load(file_location, sr=None)

        # Convert start and end times to samples
        start_sample = librosa.time_to_samples(start_time, sr=sr)
        end_sample = librosa.time_to_samples(end_time, sr=sr)

        # Extract segment
        segment = y[start_sample:end_sample]

        # Save segment to new file
        output_file_location = os.path.splitext(file_location)[0] + '_cut.wav'
        sf.write(output_file_location, segment, sr)

        print(f"Segment cut from {start_time} to {end_time}")
        return output_file_location

# dont forget to delete the file later