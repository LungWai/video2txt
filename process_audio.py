from process import check_audio_levels_soundfile
import os

def patch_audio_levels(folder_path, min_silence_len=10000, silence_thresh=-50):
    """
    Process all WAV files in a folder to check audio levels and remove silent segments
    
    Args:
        folder_path: Path to folder containing WAV files
        min_silence_len: Minimum length of silence in ms to remove
        silence_thresh: Silence threshold in dBFS
    """

    
    # Iterate through all files in folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.wav'):
            audio_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}...")
            
            # Check audio levels and remove silence
            result = check_audio_levels_soundfile(audio_path, 
                                      min_silence_len=min_silence_len,
                                      silence_thresh=silence_thresh)
            
            if result is None:
                print(f"Warning: {filename} appears to be completely silent")
                os.remove(audio_path)
                print(f"Deleted silent file {filename}")
            else:
                print(f"Successfully processed {filename}")

    print("Finished processing all audio files")




input_folder =  "C:\\Users\\lungw\\Videos\\JCaudio"

patch_audio_levels(input_folder)