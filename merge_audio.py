import os
from pydub import AudioSegment

# Directory containing the audio files
output_dir = "outputs"

# Get a list of all .wav files in the directory
audio_files = [f for f in os.listdir(output_dir) if f.endswith('.wav')]

# Sort the files to ensure correct order
audio_files.sort()

# Create an empty audio segment
combined = AudioSegment.empty()

# Loop through the files and append them
for filename in audio_files:
    path = os.path.join(output_dir, filename)
    sound = AudioSegment.from_wav(path)
    combined += sound

# Export the combined audio to a new file in mp3 format
combined.export("merged_output.mp3", format="mp3")

print("Successfully merged all audio files into merged_output.mp3")
