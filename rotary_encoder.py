import RPi.GPIO as GPIO
import time
from enum import Enum

class RotaryEncoder:
    """Represents a AMT102 rotary encoder from CUI Inc. used to keep track of the position of a stepper motor."""

    PULSES_PER_REVOLUTION = 2048

    class Direction(Enum):
        """Stores the states of the encoder's direction."""
        CW = "Clockwise"
        CCW = "Counterclockwise"

    def __init__(self, PIN_A, PIN_B, PIN_X):
        """Called when a new RotaryEncoder object is created.

        @param PIN_A: The direction pin. Connected to "DIR-" on the microstep driver.
        @param PIN_B: The pulse pin. Connected to "PUL-" on the microstep driver.
        @param PIN_X: The enable pin. Connected to "ENA-" on the microstep driver."""

        self.PIN_A = PIN_A
        self.PIN_B = PIN_B
        self.PIN_X = PIN_X

        GPIO.setup(self.PIN_A, GPIO.IN)
        GPIO.setup(self.PIN_B, GPIO.IN)
        GPIO.setup(self.PIN_X, GPIO.IN)

        self.angular_velocity = 0
        self.direction = self.Direction.CW
        self.enabled = True

    def run(self):
        SAMPLING_RATE = 1    # Amount of time elapsed before speed is calculated [s]

        while (self.enabled):
            pulses_counted = 0
            time_elapsed = 0
            t_initial = time.perf_counter()
            last_state = GPIO.input(self.PIN_A)
            while (time_elapsed < SAMPLING_RATE):
                pin_A_state = GPIO.input(self.PIN_A)
                pin_B_state = GPIO.input(self.PIN_B)
                print (pin_A_state)
                print(pin_B_state)

                self.direction = self.get_direction(pin_A_state, pin_B_state, last_state)
                last_state = GPIO.input(self.PIN_A)

                if (pin_B_state == 1):
                    pulses_counted += 1
                if (pin_B_state == 1):
                    pulses_counted += 1

                time_elapsed = time.perf_counter() - t_initial

            self.angular_velocity = self.calculate_velocity(pulses_counted, time_elapsed)
            print("Encoder angular velocity: " + str(self.angular_velocity))

    def get_direction(self, pin_A_state, pin_B_state, last_state):
        """Moves the motor a single step in whichever direction the PIN_DIR is set.

        @param speed: The rotational speed [steps/s]."""
        if (pin_A_state != last_state):
            if (pin_B_state != pin_A_state):
                return self.Direction.CW
            else:
                return self.Direction.CCW
    
    def calculate_velocity(self, pulses_counted, time_interval):
        """Moves the motor a single step in whichever direction the PIN_DIR is set.

        @param speed: The rotational speed [steps/s]."""
        angular_velocity = (pulses_counted / RotaryEncoder.PULSES_PER_REVOLUTION) * (60 / time_interval)
        if (self.direction == self.Direction.CW):
            angular_velocity *= -1
        return angular_velocity
