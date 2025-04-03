# Keep the comments and docstrings in the code. They might just come in handy.

import numpy as np
import seaborn as sns
import soundfile as sf
import matplotlib.pyplot as plt
import matplotlib.animation as animation

SAMPLE_RATE = 44100  # Hz
DURATION = 10  # seconds


def get_events(use_cosmic_events=True, **kwargs):
    """
    Get cosmic events from RPi or use simple events.

    Parameters:
    - use_cosmic_events (bool): If True, get cosmic events from RPi. Otherwise, use simple events.

    Returns:
    - events (list): List of event dictionaries with time, energy, and altitude.
    """
    use_noise = kwargs.get("use_noise", False)
    noise_level = kwargs.get("noise_level", 0)

    if not isinstance(use_cosmic_events, bool):
        raise TypeError("use_cosmic_events must be a boolean")
    if not isinstance(use_noise, bool):
        raise TypeError("use_noise must be a boolean")

    if not use_cosmic_events:
        # Simple events with timestamp, energy, position
        events = [
            {"time": 0.05, "energy": 2.3, "altitude": 0.2},
            {"time": 0.72, "energy": 1.5, "altitude": 0.7},
            # ...more events
        ]

        if use_noise:
            for event in events:
                event["energy"] += noise_level * np.random.uniform(
                    -0.01, 0.01
                )  # Add noise to energy
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
    if not isinstance(duration, int):
        raise TypeError("Duration must be an integer")
    if not duration > 0:
        raise ValueError("Duration must be positive")
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

    assert isinstance(signal, np.ndarray), "Signal must be a numpy array"
    assert signal.ndim == 1, "Signal must be 1-dimensional"
    assert len(signal) == sample_rate * duration, "Signal length mismatch"
    assert np.issubdtype(signal.dtype, np.number), "Signal must contain numeric values"

    if show_plot or plot_save_path is not None:
        plot_signal(signal, sample_rate, duration, animate=False)
        if plot_save_path:
            plt.savefig(plot_save_path)
        else:
            plt.show()

    return signal


def plot_signal(signal, sample_rate, duration, animate=True, **kwargs):
    """
    Plot the generated signal.

    Parameters:
    - signal (numpy.ndarray): Signal to plot.
    - sample_rate (int): Sample rate in Hz.
    - duration (int or float): Duration of the signal in seconds.

    Returns:
    - None
    """
    time_step = kwargs.get("animation_time_step", 0.1)

    # Validate inputs
    if not isinstance(signal, np.ndarray):
        raise TypeError("Signal must be a numpy array")
    if signal.ndim != 1:
        raise ValueError("Signal must be a 1D array")
    if len(signal) != sample_rate * duration:
        raise ValueError("Signal length mismatch")
    if not isinstance(signal[0], (int, float)):
        raise TypeError("Signal must contain numeric values")

    if animate:
        current_time = []
        current_energy = []

        def __update(frame):

            t = frame * time_step
            if t > duration:
                return (line,)

            current_time.append(t)
            current_energy.append(signal[int(t * sample_rate)])

            line.set_data(current_time, current_energy)
            return (line,)

        fig, ax = plt.subplots()
        ax.set_xlim(0, duration)
        ax.set_ylim(-0.5, 2.5)
        ax.set_title("Cosmic Events Signal")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        (line,) = ax.plot([], [], "black", lw=1)
        global ani
        ani = animation.FuncAnimation(
            fig, __update, frames=int(duration / time_step), interval=100, blit=True
        )
    else:
        sns.set_style(style="whitegrid")
        sns.lineplot(x=np.arange(len(signal)) / sample_rate, y=signal)
        plt.title("Cosmic Events Signal")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.xlim(0, duration)
        plt.ylim(-0.5, 2.5)
    plt.show()


def convert_to_audio(signal, sample_rate, save_path="signal.wav", return_signal=False):
    if not isinstance(save_path, str) or not save_path.endswith(".wav"):
        raise TypeError("Save path must be a string ending with .wav")
    if not isinstance(return_signal, bool):
        raise TypeError("return_signal must be a boolean")

    # Normalize signal to range [-1, 1]
    audio_signal = signal / np.max(np.abs(signal))

    save_audio_file(audio_signal, sample_rate, save_path)
    return audio_signal if return_signal else None


def save_audio_file(audio_signal, sample_rate, file_path):
    try:
        sf.write(file_path, audio_signal, sample_rate)
    except Exception as e:
        raise RuntimeError(f"Failed to save audio file: {e}")


if __name__ == "__main__":
    signal = generate_signal(
        sample_rate=SAMPLE_RATE,
        duration=DURATION,
        use_cosmic_events=False,
        show_plot=True,
        plot_save_path="signal_plot.png",
    )
    print("Signal generated with cosmic events.")
    print("Signal length:", len(signal))

    convert_to_audio(signal=signal, sample_rate=SAMPLE_RATE, return_signal=True)
    print("Signal converted to audio.")
