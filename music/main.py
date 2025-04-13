import math
import seaborn as sns
import matplotlib.pyplot as plt
import time as systime
import os

INPUT_FILE = "event_log.txt"
OUTPUT_FILE = "pitch_log.txt"

def read_events(filename):
    events = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines[1:]:  # Skip header
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    time_val = float(parts[0])
                    energy = float(parts[1])
                    events.append({"time": time_val, "energy": energy})
                except ValueError:
                    pass
    return events

def calculate_pitch_log_scaled(energy):
    if energy <= 0:
        return 0
    log_energy = math.log(energy)
    return 440 * (2 ** (log_energy / 12))

def generate_pitch_log(events, output_file=OUTPUT_FILE):
    with open(output_file, "w") as f:
        for event in events:
            time_val = event["time"]
            energy = event["energy"]
            frequency = 1 / time_val if time_val != 0 else 0
            pitch = calculate_pitch_log_scaled(energy)
            f.write(f"Time: {time_val}, Energy: {energy}, Frequency: {frequency:.2f}, Pitch: {pitch:.2f}\n")

def plot_energy_vs_pitch(events):
    times = [event["time"] for event in events]
    energies = [event["energy"] for event in events]
    pitches = [calculate_pitch_log_scaled(e) for e in energies]

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    plt.plot(times, pitches, label="Pitch", marker='o')
    plt.xlabel("Time (s)")
    plt.ylabel("Pitch (Hz)")
    plt.title("Pitch over Time")
    plt.legend()
    plt.tight_layout()
    # plt.show()  # Uncomment to display the plot

# Live loop
print("Monitoring event_log.txt... Press Ctrl+C to stop.")
while True:
    try:
        if os.path.exists(INPUT_FILE):
            events = read_events(INPUT_FILE)
            generate_pitch_log(events)
        systime.sleep(2)
    except KeyboardInterrupt:
        print("Stopped.")
        break
