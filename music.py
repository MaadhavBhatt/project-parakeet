from pydub import AudioSegment
from pydub.generators import Sine
import os

INPUT_FILE = "pitch_log.csv"
OUTPUT_FILE = "output_music.wav"


def read_pitch_log(filename):
    pitch_data = []
    with open(filename, "r") as file:
        lines = file.readlines()
        # Skip header line if it exists
        # Assuming the first line contains the header "time". Feel free to change this to "energy" or "frequency" if needed.
        start_line = 1 if lines and "time" in lines[0].lower() else 0

        for line in lines[start_line:]:
            values = line.strip().split(",")
            if len(values) >= 4:  # Ensure we have at least 4 values
                try:
                    time_val = float(values[0])
                    energy = float(values[1])
                    frequency = float(values[2])
                    pitch = float(values[3])
                    pitch_data.append(
                        {
                            "time": time_val,
                            "energy": energy,
                            "frequency": frequency,
                            "pitch": pitch,
                        }
                    )
                except ValueError:
                    # Skip lines that can't be converted to float
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
