import math
import matplotlib.pyplot as plt
import time as systime
import os
import sys

# Add the parent directory to the path so we can import cosmic_ray_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from cosmic_ray_utils import CosmicRayGenerator

INPUT_FILE = "event_log-gen.txt"
OUTPUT_FILE = "pitch_log-gen.txt"


def calculate_pitch(energy):
    """
    Calculate pitch from energy using logarithmic mapping.
    """
    if energy <= 0:
        return 0
    return 440 * math.exp(math.log(2) * math.log(energy) / 12)


def generate_pitch_log(events, output_file=OUTPUT_FILE):
    """
    Generate a log file with pitch calculations for each event.
    """
    with open(output_file, "w") as f:
        for event in events:
            time_val = event["time"]
            energy = event["energy"]
            frequency = 1 / time_val if time_val != 0 else 0
            pitch = calculate_pitch(energy)

            # Include altitude information if available
            altitude_info = (
                f", Altitude: {event.get('altitude', 0):.2f}"
                if "altitude" in event
                else ""
            )

            f.write(
                f"Time: {time_val}, Energy: {energy}, Frequency: {frequency:.2f}, Pitch: {pitch:.2f}{altitude_info}\n"
            )
    print(f"[PITCH] Generated pitch log with {len(events)} events")


def plot_energy_vs_pitch(events, show_plot=False):
    """
    Create a plot showing the relationship between energy and pitch.
    """
    times = [event["time"] for event in events]
    energies = [event["energy"] for event in events]
    pitches = [calculate_pitch(e) for e in energies]

    plt.figure(figsize=(10, 6))
    plt.plot(times, pitches, label="Pitch", marker="o")
    plt.xlabel("Time (s)")
    plt.ylabel("Pitch (Hz)")
    plt.title("Pitch over Time")
    plt.legend()
    plt.tight_layout()
    if show_plot:
        plt.show()


if __name__ == "__main__":
    print("[PITCH] Pitch processor started.")

    # Create a ray generator in file mode
    ray_generator = CosmicRayGenerator(mode="file", event_log=INPUT_FILE)

    while True:
        try:
            if os.path.exists(INPUT_FILE):
                # Get events from the log file
                events = ray_generator.read_events_from_file()
                if events:
                    generate_pitch_log(events)
            systime.sleep(2)
        except KeyboardInterrupt:
            print("[PITCH] Stopped.")
            break
