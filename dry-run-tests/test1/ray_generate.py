import time
import random


# 1 second = 1 eV of energy (Hypothetical conversion for simulation purposes)

def simulate_ray(signal_file="ray_signal.txt"):
    while True:
        wait_time = random.uniform(2, 5)
        time.sleep(wait_time)

        energy = random.uniform(1, 10)
        duration = energy / 10  

        print(f"[GEN] Simulating ray: Energy={energy:.2f}, Duration={duration:.2f}s")
        with open(signal_file, 'w') as f:
            f.write('1')

        time.sleep(duration)

        with open(signal_file, 'w') as f:
            f.write('0')

        print("[GEN] Ray ended.\n")

if __name__ == "__main__":
    simulate_ray()
