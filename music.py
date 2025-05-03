from pydub import AudioSegment
from pydub.generators import Sine
from typing import Final
import os
import csv

INPUT_FILE: Final[str] = "pitch_log.csv"
OUTPUT_FILE: Final[str] = "output_music.wav"


def read_pitch_log(filename) -> list[dict[str, float]]:
    pitch_data: list[dict[str, float]] = []
    with open(filename, "r", newline="") as file:
        csv_reader = csv.reader(file)

        # Check if the first row is a header
        try:
            header = next(csv_reader)
            # Assuming the header contains "time". Feel free to adjust this to "energy", "frequency", etc.
            has_header = "time" in [h.lower() for h in header]
            if not has_header:
                # If not a header, reset file pointer and read again
                file.seek(0)
                csv_reader = csv.reader(file)
        except StopIteration:
            return pitch_data  # Empty file

        for row in csv_reader:
            if len(row) == 4:  # Ensure we have exactly 4 values
                try:
                    # TODO: Make the more flexible by checking for permutations of headings.
                    time_val = float(row[0])
                    energy = float(row[1])
                    frequency = float(row[2])
                    pitch = float(row[3])
                    pitch_data.append(
                        {
                            "time": time_val,
                            "energy": energy,
                            "frequency": frequency,
                            "pitch": pitch,
                        }
                    )
                except ValueError:
                    # Skip rows that can't be converted to float
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
