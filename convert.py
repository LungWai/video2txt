
import os
import librosa
import torch
from docx import Document
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

def convert_video_to_text(input_file, output_file, output_format):
    # Load the speech-to-text model
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")

    # Convert video to audio
    audio_file = convert_video_to_audio(input_file)

    # Transcribe audio to text
    transcription = transcribe_audio_to_text(audio_file, model, tokenizer)

    # Save transcription to output file
    if output_format == "docx":
        save_transcription_to_docx(transcription, output_file)
    elif output_format == "text":
        save_transcription_to_text(transcription, output_file)
    else:
        print("Invalid output format")

def convert_video_to_audio(input_file):
    # Convert video to audio using ffmpeg
    audio_file = "temp.wav"
    os.system(f"ffmpeg -i {input_file} -vn -acodec pcm_s16le -ar 16000 -ac 1 {audio_file}")
    return audio_file

def transcribe_audio_to_text(audio_file, model, tokenizer):
    # Load audio file
    audio_input, _ = librosa.load(audio_file, sr=16000)

    # Tokenize audio input
    input_values = tokenizer(audio_input, return_tensors="pt").input_values

    # Transcribe audio to text
    with torch.no_grad():
        logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = tokenizer.batch_decode(predicted_ids)[0]

    return transcription

def save_transcription_to_docx(transcription, output_file):
    # Save transcription to docx file
    doc = Document()
    doc.add_paragraph(transcription)
    doc.save(output_file)

def save_transcription_to_text(transcription, output_file):
    # Save transcription to text file
    with open(output_file, "w") as file:
        file.write(transcription)

