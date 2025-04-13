import math
from pydub import AudioSegment
from pydub.generators import Sine
import os

INPUT_FILE = "pitch_log.txt"
OUTPUT_FILE = "output_music.wav"

def read_pitch_log(filename):
    pitch_data = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(", ")
            if len(parts) == 4:
                try:
                    time_val = float(parts[0].split(": ")[1])
                    energy = float(parts[1].split(": ")[1])
                    frequency = float(parts[2].split(": ")[1])
                    pitch = float(parts[3].split(": ")[1])
                    pitch_data.append({"time": time_val, "energy": energy, "frequency": frequency, "pitch": pitch})
                except ValueError:
                    pass
    return pitch_data

def generate_tone_from_pitch(pitch, duration_ms=500):
    if pitch > 0:
        tone = Sine(pitch).to_audio_segment(duration=duration_ms)
        return tone
    return AudioSegment.silent(duration=duration_ms)

def generate_music(pitch_data, output_file=OUTPUT_FILE):
    audio = AudioSegment.silent(duration=0)
    for event in pitch_data:
        pitch = event["pitch"]
        tone = generate_tone_from_pitch(pitch, duration_ms=500)
        audio += tone 

    audio.export(output_file, format="wav")
    print(f"Music generated and saved to {output_file}")

def create_music():
    if os.path.exists(INPUT_FILE):
        pitch_data = read_pitch_log(INPUT_FILE)
        generate_music(pitch_data)
    else:
        print(f"Error: {INPUT_FILE} not found!")

create_music()
