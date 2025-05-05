import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime, timedelta
import os
import sys

# Add the parent directory to the path so we can import cosmic_ray_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from cosmic_ray_utils import CosmicRayGenerator

# Constants
DURATION = 10  # seconds
TIME_STEP = 0.1  # Step size for live update

# Create cosmic ray generator for visualization
ray_generator = CosmicRayGenerator(mode="predefined", duration=DURATION)
events = ray_generator.get_events()

start_utc = datetime.utcnow().replace(microsecond=0)

fig = plt.figure(figsize=(12, 6), facecolor="black")
gs = fig.add_gridspec(1, 2, width_ratios=[3, 1])
ax_main = fig.add_subplot(gs[0])
ax_side = fig.add_subplot(gs[1])

ax_main.set_facecolor("black")
ax_main.axis("off")
clock_text = ax_main.text(
    0.5,
    0.5,
    "",
    color="cyan",
    ha="center",
    va="center",
    fontsize=36,
    fontfamily="monospace",
)

ax_side.set_facecolor("black")
ax_side.axis("off")
ax_side.set_title("Ray Detections", color="yellow", pad=20)
detection_texts = []

displayed_events = set()


def update(frame):
    global displayed_events

    t = frame * TIME_STEP
    if t > DURATION:
        return [clock_text] + detection_texts

    current_utc = start_utc + timedelta(seconds=t)
    clock_text.set_text(current_utc.strftime("%Y-%m-%d\n%H:%M:%S UTC"))

    new_detections = []
    for event in events:
        if abs(event["time"] - t) < TIME_STEP and event["time"] not in displayed_events:
            displayed_events.add(event["time"])
            event_utc = (start_utc + timedelta(seconds=event["time"])).strftime(
                "%H:%M:%S"
            )

            # Include altitude information if available
            altitude_info = (
                f" | Alt: {event.get('altitude', 0):.0f}m"
                if "altitude" in event
                else ""
            )

            detection_text = ax_side.text(
                0.1,
                0.9 - len(detection_texts) * 0.15,
                f"{event_utc} | {event['energy']:.1f} keV{altitude_info}",
                color="yellow",
                fontsize=14,
                transform=ax_side.transAxes,
            )
            detection_texts.append(detection_text)

    return [clock_text] + detection_texts


ani = animation.FuncAnimation(
    fig, update, frames=int(DURATION / TIME_STEP), interval=100, blit=True
)

plt.tight_layout()
plt.show()
