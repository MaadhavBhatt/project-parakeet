import time
import random
import numpy as np
import os


class CosmicRayGenerator:
    """
    A unified class for generating cosmic ray events in different ways.
    This combines functionality from multiple parts of the project.
    """

    def __init__(self, mode="simulated", validate=True, **kwargs):
        """
        Initialize a cosmic ray generator.

        Parameters:
        - mode: The generation mode ("simulated", "hardware", "predefined", or "file")
        - kwargs: Additional parameters:
            - signal_file: Path to signal file (for hardware simulation)
            - event_log: Path to event log file (for file mode)
            - duration: Duration for predefined events (default: 10)
            - noise_level: Base noise level (default: 0.05)
        """
        if validate:
            # Validate mode
            if mode not in ["simulated", "hardware_sim", "predefined", "file"]:
                raise ValueError(
                    "Invalid mode. Choose from 'simulated', 'hardware_sim', 'predefined', or 'file'."
                )

            if mode == "file" and not kwargs.get("event_log"):
                raise ValueError(
                    "Event log file path must be provided for 'file' mode."
                )

            if mode == "hardware_sim" and not kwargs.get("signal_file"):
                raise ValueError(
                    "Signal file path must be provided for 'hardware_sim' mode."
                )

            # Warn about unneeded kwargs
            known_params = ["signal_file", "event_log", "duration", "noise_level"]
            for key in kwargs:
                if key not in known_params:
                    print(f"Warning: Unused parameter '{key}' provided")

            # Warn about mode-specific parameters not needed for the selected mode
            if mode != "hardware_sim" and "signal_file" in kwargs:
                print(
                    f"Warning: 'signal_file' parameter is only used in 'hardware_sim' mode"
                )
            if mode != "file" and "event_log" in kwargs:
                print(f"Warning: 'event_log' parameter is only used in 'file' mode")

        self.mode: str = mode
        self.signal_file: str = kwargs.get("signal_file", "ray_signal.txt")
        self.event_log: str = kwargs.get("event_log", "event_log.txt")
        self.duration: float = kwargs.get("duration", 10)
        self.noise_level: float = kwargs.get("noise_level", 0.05)

        # For hardware simulation, ensure the signal file exists
        if self.mode == "hardware_sim" and not os.path.exists(self.signal_file):
            with open(self.signal_file, "w") as f:
                f.write("0")

    def get_predefined_events(self) -> list[dict[str, float]]:
        """
        Return a predefined set of cosmic ray events.
        Used for consistent testing and visualization.
        """
        return [
            {"time": 1.0, "energy": 2.3, "altitude": 2500},
            {"time": 4.5, "energy": 1.5, "altitude": 2300},
            {"time": 6.2, "energy": 3.0, "altitude": 2700},
            {"time": 8.7, "energy": 2.0, "altitude": 2400},
        ]

    def generate_random_event(self) -> dict[str, float]:
        """
        Generate a single random cosmic ray event.
        """
        energy: float = random.uniform(1, 10)
        duration: float = energy / 10  # Simple conversion for simulation
        altitude: float = random.uniform(2000, 3000)  # Simulated altitude in meters

        return {
            "time": time.time(),
            "energy": energy,
            "duration": duration,
            "altitude": altitude,
        }

    def simulate_continuous(self, callback=None, stop_event=None) -> None:
        """
        Continuously simulate cosmic ray events until stopped.

        Parameters:
        - callback: Function to call with each event
        - stop_event: Threading event to signal stopping
        """
        while True:
            if stop_event and stop_event.is_set():
                break

            wait_time: float = random.uniform(2, 5)
            time.sleep(wait_time)

            event: dict[str, float] = self.generate_random_event()

            if callback:
                callback(event)

            if self.mode == "hardware_sim":
                # Simulate hardware signal
                with open(self.signal_file, "w") as f:
                    f.write("1")

                time.sleep(event["duration"])

                with open(self.signal_file, "w") as f:
                    f.write("0")

            print(
                f"Ray: Energy={event['energy']:.2f}, Duration={event['duration']:.2f}s"
            )

    def read_events_from_file(self) -> list[dict[str, float]]:
        """
        Read cosmic ray events from a log file.
        """
        events: list[dict[str, float]] = []
        if not os.path.exists(self.event_log):
            return events

        with open(self.event_log, "r") as file:
            lines: list[str] = file.readlines()
            for line in lines[1:]:  # Skip header
                parts: list[str] = line.strip().split()
                if len(parts) >= 2:
                    try:
                        # Basic format: time energy [altitude]
                        time_val: float = float(parts[0])
                        energy: float = float(parts[1])
                        altitude: float = float(parts[2]) if len(parts) > 2 else 0
                        events.append(
                            {"time": time_val, "energy": energy, "altitude": altitude}
                        )
                    except (ValueError, IndexError):
                        pass
        return events

    def get_events(self) -> list[dict[str, float]]:
        """
        Get cosmic ray events based on the selected mode.
        """
        if self.mode == "predefined":
            return self.get_predefined_events()
        elif self.mode == "file":
            return self.read_events_from_file()
        elif self.mode == "simulated":
            # For one-time simulated events, generate a few random ones
            events: list[dict[str, float]] = []
            base_time: float = time.time()
            for i in range(random.randint(3, 8)):
                event: dict[str, float] = self.generate_random_event()
                event["time"] = i * (
                    self.duration / 10
                )  # Spread events over the duration
                events.append(event)
            return events
        else:
            # Default empty list for other modes
            return []

    def generate_signal(self, sample_rate: int = 100) -> tuple[np.ndarray, np.ndarray]:
        """
        Generate a signal array from cosmic ray events.

        Parameters:
        - sample_rate: Number of samples per second

        Returns:
        - time_values: Array of time points
        - signal_values: Array of signal values
        """
        # Create time base and empty signal
        time_values: np.ndarray = np.arange(0, self.duration, 1 / sample_rate)
        signal_values: np.ndarray = np.full_like(time_values, self.noise_level)

        # Add random noise
        signal_values += np.random.uniform(-0.01, 0.01, size=len(time_values))

        # Get events
        events: list[dict[str, float]] = self.get_events()

        # Add events to signal
        for event in events:
            # Find the index corresponding to the event time
            idx: int = int(event["time"] * sample_rate)
            if idx < len(signal_values):
                # Create a decaying pulse
                decay_length: int = int(0.1 * sample_rate)  # 100ms decay
                end_idx: int = min(idx + decay_length, len(signal_values))
                decay: np.ndarray = event["energy"] * np.exp(
                    -np.arange(end_idx - idx) / (0.02 * sample_rate)
                )
                signal_values[idx:end_idx] += decay

        return time_values, signal_values
