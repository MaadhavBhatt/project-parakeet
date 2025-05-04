## RPi 4 Test 1 ([Raw Code](raw_code/))

We'll be writing code to simulate a cosmic ray, and then time for how long the dummy GPIO pin stays HIGH for, to deduce energy. The interesting bit of this will be that there will be 2 separate programs, one to create a ray of a random energy level, and one to deduce energy by the time period.

### Results

Logic works, but we have to derive a solid formula for the _actual_ conversion from time to energy.

## RPi 4 Test 2 ([Code and Hardware](code_and_hardware/))

We'll be using the RPi 4 for now to simulate how the GPIO pin will go HIGH. The logic is simple. A male-to-female jumper wire is going to be connected to the RPi GPIO port, and the male portion of the wire is going to be touched on the 3v3 pin of the RPi, essentially, making the pin go HIGH. Then, the next steps will be the same as RPi 4 Test 1.

### Results

The GPIO pin goes HIGH when the jumper wire is touched to the 3V GPIO pin, as well as when we touch it with our finger. The time period is recorded, and the energy is calculated. The results are consistent with the expected behavior of a cosmic ray.
