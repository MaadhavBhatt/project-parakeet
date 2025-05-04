from pydub import AudioSegment
from pydub.generators import Sine
from typing import Final
import os
import csv

INPUT_FILE: Final[str] = "pitch_log-gen.csv"
OUTPUT_FILE: Final[str] = "output_music-gen.wav"


def read_pitch_log(filename) -> list[dict[str, float]]:
    """
    Read a CSV file containing pitch log data and parse it into a list of dictionaries.
    The function attempts to detect if the file has a header row containing "time".
    Each row in the CSV is expected to have exactly 4 values in order representing:
    time, energy, frequency, and pitch.
    Args:
        filename (str): Path to the CSV file containing pitch data.
    Returns:
        list[dict[str, float]]: List of dictionaries, where each dictionary contains:
            - "time": The timestamp value
            - "energy": The energy value
            - "frequency": The frequency value
            - "pitch": The pitch value
    Note:
        - Rows that don't have exactly 4 values are skipped.
        - Values that can't be converted to float are skipped.
        - Valid rows are expected to be in the order of time, energy, frequency, and pitch.
        - Empty files return an empty list.
    """
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
    """
    Generate an audio tone from a given pitch frequency.

    Args:
        pitch (float): The frequency of the tone in Hz. If pitch is 0 or negative,
                      a silent segment will be returned instead.
        duration_ms (int, optional): Duration of the tone in milliseconds. Defaults to 500ms.

    Returns:
        AudioSegment: An AudioSegment object containing the generated tone,
                    or a silent segment if pitch is 0 or negative.
    """
    if pitch > 0:
        tone: AudioSegment = Sine(pitch).to_audio_segment(duration=duration_ms)
        return tone
    return AudioSegment.silent(duration=duration_ms)


def generate_music(
    pitch_data: list[dict[str, float]], output_file: str = OUTPUT_FILE
) -> None:
    """
    Generate music from pitch data and save to a WAV file.
    This function creates an audio segment by concatenating tones generated
    from a sequence of pitch values, then exports the result to an audio file.
    Args:
        pitch_data (list[dict[str, float]]): A list of dictionaries, where each
            dictionary contains at least a 'pitch' key with its corresponding
            frequency value in Hz.
        output_file (str, optional): The path where the generated audio will be saved.
            Defaults to the value of OUTPUT_FILE.
    Returns:
        None: The function saves the generated audio to a file and prints a
            confirmation message.
    Example:
        >>> pitch_data = [{"pitch": 440.0}, {"pitch": 493.88}]  # A4, B4 notes
        >>> generate_music(pitch_data, "my_music.wav")
        Music generated and saved to my_music.wav
    """
    audio: AudioSegment = AudioSegment.silent(duration=0)
    for event in pitch_data:
        pitch: float = event["pitch"]
        tone: AudioSegment = generate_tone_from_pitch(pitch, duration_ms=500)
        audio += tone

    audio.export(output_file, format="wav")
    print(f"Music generated and saved to {output_file}")



def create_music(input_file: str = INPUT_FILE) -> None:
    """
    Creates music based on pitch data from an input file.

    This function checks if the input file specified by INPUT_FILE exists.
    If it exists, it reads pitch data from the file and generates music.
    Otherwise, it prints an error message.

    Returns:
        None

    Raises:
        None explicitly, but may raise exceptions from called functions.
    """
    if os.path.exists(input_file):
        pitch_data: list[dict[str, float]] = read_pitch_log(input_file)
        generate_music(pitch_data)
    else:
        print(f"Error: {input_file} not found!")


if __name__ == "__main__":
    create_music()
