# Define the input parameters
from Summary.AudioAligner import AudioAligner

#path1 = 'C:/Users/Omega/Music/MusicAI/trimmer_langSiciliano.mp3'
#path2 = 'C:/Users/Omega/Music/MusicAI/trimmer_SicilianoBWV1031.mp3'

path1 = 'C:/Users/Omega/Music/MusicAI/trimmed_Concert.mp3'
path2 = 'C:/Users/Omega/Music/MusicAI/trimmer_(Spotify).mp3'

# Create an instance of the AudioAligner class
aligner = AudioAligner()

# Create an instance of the AudioProcessor class
avg_time_diff = aligner.align(path1, path2)


# Print the result
print(f"summed Average Time Difference: {avg_time_diff} seconds")