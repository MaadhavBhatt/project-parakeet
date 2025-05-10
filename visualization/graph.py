import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import os
import sys
from typing import Final, Optional

# Add the parent directory to the path so we can import cosmic_ray_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from cosmic_ray_utils import CosmicRayGenerator


class CosmicRayVisualizer:
    # Default constants
    DEFAULT_SAMPLE_RATE: Final[int] = 100  # Hz
    DEFAULT_DURATION: Final[int] = 10  # seconds
    DEFAULT_NOISE_LEVEL: Final[float] = 0.05  # Constant noise floor level
    DEFAULT_EVENT_INTENSITY: Final[float] = 2.0  # Intensity of detected waves
    DEFAULT_TIME_STEP: Final[float] = 0.1  # Step size for live update
    DEFAULT_GENERATOR_MODE: Final[str] = "predefined"  # Mode for cosmic ray generator
    DEFAULT_COLORS: dict[str, str] = {"background": "white", "foreground": "black"}

    def __init__(
        self,
        duration: int = DEFAULT_DURATION,
        *, # This forces keyword-only arguments after this point
        noise_level: float = DEFAULT_NOISE_LEVEL,
        event_intensity: float = DEFAULT_EVENT_INTENSITY,
        time_step: float = DEFAULT_TIME_STEP,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        generator_mode: str = DEFAULT_GENERATOR_MODE,
        colors: dict[str, str] = DEFAULT_COLORS,
    ) -> None:
        """
        Initialize the cosmic ray visualizer.
        """
        self.duration: int = duration
        self.noise_level: float = noise_level
        self.event_intensity: float = event_intensity
        self.time_step: float = time_step
        self.sample_rate: int = sample_rate
        self.generator_mode: str = generator_mode
        self.colors: dict[str, str] = colors

        # Internal data
        self.current_time: list[float] = []
        self.current_energy: list[float] = []
        self.ray_generator: Optional[CosmicRayGenerator] = None
        self.events: Optional[list[dict[str, float]]] = None
        self.fig: Optional[Figure] = None
        self.ax: Optional[Axes] = None
        self.line: Optional[Line2D] = None
        self.animation: Optional[animation.FuncAnimation] = None

    def __str__(self) -> str:
        """String representation of the visualizer."""
        return (
            f"CosmicRayVisualizer(\n"
            f"\tduration={self.duration},\n"
            f"\tgenerator_mode='{self.generator_mode}',\n"
            f"\tcolors={self.colors}\n"
            f"\tnoise_level={self.noise_level},\n"
            f"\tevent_intensity={self.event_intensity},\n"
            f"\ttime_step={self.time_step},\n"
            f"\tsample_rate={self.sample_rate},\n"
            f")"
        )

    def setup(self) -> "CosmicRayVisualizer":
        """Set up the visualization."""
        # Create a cosmic ray generator
        self.ray_generator = CosmicRayGenerator(
            mode=self.generator_mode,
            duration=self.duration,
            noise_level=self.noise_level,
        )
        self.events = self.ray_generator.get_events()

        # Initialize plot
        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor(self.colors["background"])
        self.ax.set_facecolor(self.colors["background"])
        self.ax.set_xlim(0, self.duration)
        self.ax.set_ylim(0, self.event_intensity + self.noise_level)
        self.ax.set_xlabel("Time (s)", color=self.colors["foreground"])
        self.ax.set_ylabel("Energy", color=self.colors["foreground"])
        self.ax.tick_params(axis="x", colors=self.colors["foreground"])
        self.ax.tick_params(axis="y", colors=self.colors["foreground"])

        (self.line,) = self.ax.plot([], [], self.colors["foreground"], lw=1)
        if self.fig.canvas.manager is not None:
            self.fig.canvas.manager.set_window_title("Cosmic Ray Visualization")
        return self

    def update(self, frame) -> tuple[Line2D]:
        """Update function for animation."""
        assert self.line is not None, "Line should be initialized before update"

        t = frame * self.time_step
        if t > self.duration and self.line is not None:
            return (self.line,)

        energy = self.noise_level + np.random.uniform(-0.01, 0.01)

        if self.events is not None:
            for event in self.events:
                if abs(event["time"] - t) < self.time_step:
                    energy += event["energy"]  # Add disturbance

        self.current_time.append(t)
        self.current_energy.append(energy)

        self.line.set_data(self.current_time, self.current_energy)
        return (self.line,)

    def start_animation(self, interval: int = 100) -> "CosmicRayVisualizer":
        """Start the animation."""
        if self.fig is None or self.ax is None:
            self.setup()
            assert (
                self.fig is not None
            ), "Figure should be initialized before animation. Setup failed."

        self.animation = animation.FuncAnimation(
            self.fig,
            self.update,
            frames=int(self.duration / self.time_step),
            interval=interval,
            blit=True,
        )
        return self

    def show(self) -> None:
        """Display the visualization."""
        plt.show()

    def run(self, interval: int = 100) -> None:
        """Setup, animate and show the visualization in one call."""
        self.setup()
        self.start_animation(interval)
        self.show()


if __name__ == "__main__":
    visualizer: CosmicRayVisualizer = CosmicRayVisualizer(
        duration=10, generator_mode="predefined"
    )
    visualizer.run()
    print(visualizer)
