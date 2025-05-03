import time


def monitor_rays(signal_file="ray_signal-gen.txt"):
    print("Monitoring for rays.")

    try:
        while True:
            with open(signal_file, "r") as f:
                signal = f.read().strip()

            if signal == "1":
                start_time = time.time()

                while True:
                    with open(signal_file, "r") as f:
                        if f.read().strip() == "0":
                            break
                    time.sleep(0.001)

                end_time = time.time()
                duration = end_time - start_time
                energy = duration

                print(f"Ray detected!")
                print(f"Duration: {duration:.5f} s")
                print(f"Approx Energy: {energy:.5f} eV")

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Stopped.")


if __name__ == "__main__":
    with open("ray_signal-gen.txt", "w") as f:
        f.write("0")

    monitor_rays()
