# Keep the comments and docstrings in the code. They might just come in handy.

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

SAMPLE_RATE = 44100  # Hz
DURATION = 10  # seconds


def get_events(use_cosmic_events=True):
    """
    Get cosmic events from RPi or use simple events.

    Parameters:
    - use_cosmic_events (bool): If True, get cosmic events from RPi. Otherwise, use simple events.

    Returns:
    - events (list): List of event dictionaries with time, energy, and altitude.
    """
    if not isinstance(use_cosmic_events, bool):
        raise TypeError("use_cosmic_events must be a boolean")

    if not use_cosmic_events:
        # Simple events with timestamp, energy, position
        events = [
            {"time": 0.05, "energy": 2.3, "altitude": 0.2},
            {"time": 0.72, "energy": 1.5, "altitude": 0.7},
            # ...more events
        ]
    else:
        pass  # Get cosmic events from RPi

    return events


def generate_signal(
    sample_rate,
    duration,
    use_cosmic_events=True,
    show_plot=False,
    plot_save_path: str | None = None,
):
    """
    Generate a signal based on cosmic events.

    Parameters:
    - sample_rate (int): Sample rate in Hz.
    - duration (int or float): Duration of the signal in seconds.
    - use_cosmic_events (bool): If True, use cosmic events. Otherwise, use simple events.
    - show_plot (bool): If True, show the plot of the signal.
    - plot_save_path (str or None): Path to save the plot. If None, do not save.

    Returns:
    - signal (numpy.ndarray): Generated signal.
    """
    # Validate inputs
    if not isinstance(sample_rate, int):
        raise TypeError("Sample rate must be an integer")
    if not sample_rate > 0:
        raise ValueError("Sample rate must be positive")
    if not isinstance(duration, (int, float)):
        raise TypeError("Duration must be an integer or float")
    if not duration > 0:
        raise ValueError("Duration must be positive")
    if not isinstance(use_cosmic_events, bool):
        raise TypeError("use_cosmic_events must be a boolean")
    if not isinstance(show_plot, bool):
        raise TypeError("show_plot must be a boolean")
    if plot_save_path is not None and not isinstance(plot_save_path, str):
        raise TypeError("plot_save_path must be a string or None")

    events = get_events(use_cosmic_events)

    # Create blank signal at audio rate
    signal = np.zeros(sample_rate * duration)

    # Add pulses for cosmic events
    for event in events:
        event_time = event["time"]
        energy = event["energy"]
        idx = int(event_time * sample_rate)
        if idx < len(signal):
            # Create exponential decay
            decay = energy * np.exp(-np.arange(1000) / 200)
            signal[idx : idx + len(decay)] += decay

    if show_plot or plot_save_path is not None:
        plot_signal(signal, sample_rate, duration)
        if plot_save_path:
            plt.savefig(plot_save_path)
        else:
            plt.show()

    return signal


def plot_signal(signal, sample_rate, duration):
    """
    Plot the generated signal.

    Parameters:
    - signal (numpy.ndarray): Signal to plot.
    - sample_rate (int): Sample rate in Hz.
    - duration (int or float): Duration of the signal in seconds.

    Returns:
    - None
    """
    # Validate inputs
    if not isinstance(signal, np.ndarray):
        raise TypeError("Signal must be a numpy array")
    if signal.ndim != 1:
        raise ValueError("Signal must be a 1D array")
    if signal.size == 0:
        raise ValueError("Signal cannot be empty")
    if not isinstance(signal[0], (int, float)):
        raise TypeError("Signal must contain numeric values")
    if not isinstance(sample_rate, int):
        raise TypeError("Sample rate must be an integer")
    if not isinstance(duration, (int, float)):
        raise TypeError("Duration must be an integer or float")

    sns.set_style(style="whitegrid")
    sns.lineplot(x=np.arange(len(signal)) / sample_rate, y=signal)
    plt.title("Cosmic Events Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.xlim(0, duration)
    plt.ylim(-0.5, 2.5)
    plt.show()


signal = generate_signal(
    sample_rate=SAMPLE_RATE,
    duration=DURATION,
    use_cosmic_events=False,
    show_plot=True,
    plot_save_path="signal_plot.png",
)
print("Signal generated with cosmic events.")
print("Signal length:", len(signal))
