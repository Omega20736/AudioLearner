import librosa
import soundfile as sf

# Load audio file
y, sr = librosa.load('C:/Users/Omega/Music/MusicAI/langSiciliano.mp3', sr=None)

# Trim the silence from the beginning and end
yt, index = librosa.effects.trim(y, top_db=20)

# Save the trimmed audio
sf.write('C:/Users/Omega/Music/MusicAI/trimmer_langSiciliano.mp3', yt, sr)