import os
import numpy as np
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from tqdm import tqdm
import soundfile as sf

def check_audio_levels_soundfile(audio_path, min_silence_len=10000, silence_thresh=-20):
    y, sr = sf.read(audio_path)
    print("Loading audio file...")

    # Convert silence threshold from dBFS to amplitude
    silence_thresh_amplitude = 10 ** (silence_thresh / 20)

    # Find non-silent segments
    nonsilent_ranges = []
    frame_length = int(sr * (min_silence_len / 1000))
    hop_length = frame_length // 4  # Reduce hop length for finer granularity

    # Keep track of the end of the last added segment to avoid overlap
    last_end = -1

    for i in range(0, len(y), hop_length):
        frame = y[i:i + frame_length]
        if np.max(np.abs(frame)) > silence_thresh_amplitude:
            # Only add if this segment doesn't overlap with the previous one
            if i > last_end:
                nonsilent_ranges.append((i, min(i + frame_length, len(y))))
                last_end = min(i + frame_length, len(y))

    if not nonsilent_ranges:
        print("No non-silent segments found")
        return None

    # Merge overlapping or very close segments
    merged_ranges = []
    if nonsilent_ranges:
        current_start, current_end = nonsilent_ranges[0]
        for start, end in nonsilent_ranges[1:]:
            if start <= current_end:
                current_end = max(current_end, end)
            else:
                merged_ranges.append((current_start, current_end))
                current_start, current_end = start, end
        merged_ranges.append((current_start, current_end))

    # Debugging output to check merged ranges
    # print("Merged non-silent ranges:", merged_ranges)

    # Create new audio with only non-silent parts
    new_audio = np.concatenate([y[start:end] for start, end in merged_ranges])
    sf.write(audio_path, new_audio, sr)
    print("Audio processing complete")
    return True

def convert_video_to_audio(input_folder, output_folder, remove_silence=False):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp4"):
            print(f"Processing {filename}")
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename.replace(".mp4", ".wav"))
            
            # Command to convert video to audio
            command = f"ffmpeg -i {input_file_path} -vn -acodec pcm_s16le -ar 16000 -ac 1 {output_file_path}"
            os.system(command)
            print(f"Converted {input_file_path} to {output_file_path}")
            
            # Check if the new audio file exists in the output folder
            if os.path.exists(output_file_path):
                if remove_silence:
                    print("Checking audio levels and removing silent segments...")
                    result = check_audio_levels_soundfile(output_file_path)
                    
                    if result is None:  # File is completely silent
                        print(f"Warning: Audio file appears to be completely silent")
                        os.remove(output_file_path)
                        os.remove(input_file_path)  # Also remove the original silent video
                        print(f"Deleted silent files {input_file_path} and {output_file_path}")
                    elif result:  # File has non-silent parts
                        os.remove(input_file_path)
                        print(f"Deleted original file {input_file_path}")
                else:
                    os.remove(input_file_path)
                    print(f"Deleted original file {input_file_path}")
            else:
                print(f"Warning: Conversion may have failed, {output_file_path} not found.")
                break

def rename_files(input_folder):
    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if " " in filename:  # Check if there is a space in the filename
            new_filename = filename.replace(" ", "_")
            original_file_path = os.path.join(input_folder, filename)
            new_file_path = os.path.join(input_folder, new_filename)
            os.rename(original_file_path, new_file_path)  # Rename the file
            print(f"Renamed '{filename}' to '{new_filename}'")


# Specify the input and output folders
# if the folder name is have empty space, it will delete all file

input_folder = "C:\\Users\\lungw\\Videos"
output_folder = "C:\\Users\\lungw\\Videos\\JCaudio"

# #testing setup
# test_folder = "C:\\Users\\lungw\\Videos\\test"
# test_output_folder = "C:\\Users\\lungw\\Videos\\test\\wav"

# input_folder = test_folder
# output_folder = test_output_folder

# Call the function

rename_files(input_folder)
convert_video_to_audio(input_folder, output_folder, remove_silence=True)  # Set flag to True to remove silence
