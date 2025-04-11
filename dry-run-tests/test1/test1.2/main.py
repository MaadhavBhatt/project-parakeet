import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
SIGNAL_PIN = 23    # The pin detecting the "ray"
BUZZER_PIN = 24    # The pin powering the buzzer

GPIO.setup(SIGNAL_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

print("[DETECTOR] Ready. Touch 3.3V to GPIO 23 to simulate a ray.")

try:
    while True:
        if GPIO.input(SIGNAL_PIN) == GPIO.HIGH:
            print("[DETECTOR] Ray detected!")
            start = time.time()

            while GPIO.input(SIGNAL_PIN) == GPIO.HIGH:
                time.sleep(0.001)

            end = time.time()
            duration = end - start
            energy = duration * 1e6  # dummy formula

            print(f"  Duration: {duration:.6f} s")
            print(f"  Approx Energy: {energy:.2f} eV")
           
            # Buzz for 100ms
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            print()

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n[DETECTOR] Stopped.")

finally:
    GPIO.cleanup()
