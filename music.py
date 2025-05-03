from pydub import AudioSegment
from pydub.generators import Sine
import os
from typing import Final

INPUT_FILE: Final[str] = "pitch_log.csv"
OUTPUT_FILE: Final[str] = "output_music.wav"


def read_pitch_log(filename) -> list[dict[str, float]]:
    pitch_data: list[dict[str, float]] = []
    with open(filename, "r") as file:
        lines: list = file.readlines()
        # Skip header line if it exists
        # Assuming the first line contains the header "time". Feel free to change this to "energy" or "frequency" if needed.
        # TODO: Make this more flexible to handle different permutations of headings
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


def generate_tone_from_pitch(pitch, duration_ms=500) -> AudioSegment:
    if pitch > 0:
        tone: AudioSegment = Sine(pitch).to_audio_segment(duration=duration_ms)
        return tone
    return AudioSegment.silent(duration=duration_ms)


def generate_music(
    pitch_data: list[dict[str, float]], output_file: str = OUTPUT_FILE
) -> None:
    audio: AudioSegment = AudioSegment.silent(duration=0)
    for event in pitch_data:
        pitch: float = event["pitch"]
        tone: AudioSegment = generate_tone_from_pitch(pitch, duration_ms=500)
        audio += tone

    audio.export(output_file, format="wav")
    print(f"Music generated and saved to {output_file}")


def create_music() -> None:
    if os.path.exists(INPUT_FILE):
        pitch_data: list[dict[str, float]] = read_pitch_log(INPUT_FILE)
        generate_music(pitch_data)
    else:
        print(f"Error: {INPUT_FILE} not found!")


if __name__ == "__main__":
    create_music()
