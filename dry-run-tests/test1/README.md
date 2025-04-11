## Test 1.1 (Raw Code)

### Idea

We'll be writing a code to simulate a cosmic ray, and then time for how long the dummy GPIO pin stays HIGH for, to deduce energy. The interesting bit of this will be that there will be 2 
seperate programs, one to **_create_** a ray of a random energy level, and one to **_deduce_** energy by the time period.

### Results

Logic works, but we have to derive a solid formula for the **_actual_** conversion from time to energy.

## Test 1.2 (Hardware)

### Idea

We'll be using the RPi 4 for now to simulate how the GPIO pin will go HIGH. The logic is simple. A **_male to female_** jumper wire is going
to be connected to the RPi GPIO port, and the male portion of the wire is going to be touched on the 3v3 pin of the RPi, essentially, making the pin go HIGH. Then, the next steps will be the same as **_Test 1.1_**.

### Results

Logic works, but we have to derive a solid formula for the **_actual_** conversion from time to energy.
