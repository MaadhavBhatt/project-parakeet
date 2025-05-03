import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from cosmic_ray_utils import CosmicRayGenerator

# Constants
SAMPLE_RATE = 100  # Hz
DURATION = 10  # seconds
NOISE_LEVEL = 0.05  # Constant noise floor level
EVENT_INTENSITY = 2.0  # Intensity of detected waves
TIME_STEP = 0.1  # Step size for live update

# Create a cosmic ray generator for visualization
ray_generator = CosmicRayGenerator(
    mode="predefined", duration=DURATION, noise_level=NOISE_LEVEL
)
events = ray_generator.get_events()

time_values = np.arange(0, DURATION, TIME_STEP)
energy_values = np.full_like(time_values, NOISE_LEVEL)

fig, ax = plt.subplots()
fig.patch.set_facecolor("black")
ax.set_facecolor("black")
ax.set_xlim(0, DURATION)
ax.set_ylim(0, EVENT_INTENSITY + NOISE_LEVEL)
ax.set_xlabel("Time (s)", color="white")
ax.set_ylabel("Energy", color="white")
ax.tick_params(axis="x", colors="white")
ax.tick_params(axis="y", colors="white")

(line,) = ax.plot([], [], "w", lw=1)

# Real-time data buffer
current_time = []
current_energy = []


def update(frame):
    global current_time, current_energy

    t = frame * TIME_STEP
    if t > DURATION:
        return (line,)

    energy = NOISE_LEVEL + np.random.uniform(-0.01, 0.01)

    for event in events:
        if abs(event["time"] - t) < TIME_STEP:
            energy += event["energy"]  # Add disturbance

    current_time.append(t)
    current_energy.append(energy)

    line.set_data(current_time, current_energy)
    return (line,)


ani = animation.FuncAnimation(
    fig, update, frames=int(DURATION / TIME_STEP), interval=100, blit=True
)
plt.show()
