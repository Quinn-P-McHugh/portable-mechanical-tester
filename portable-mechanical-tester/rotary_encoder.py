"""Module defining RotaryEncoder class and related functions.

Uses Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
"""

from enum import Enum
import RPi.GPIO as GPIO
import time

class RotaryEncoder:
    """Represents a AMT102 rotary encoder from CUI Inc. used to keep track of
    the position of a stepper motor.

    Attributes:
        PIN_A: An integer indicating the GPIO pin number connected to "A" on the
            rotary encoder.
        PIN_B: An integer indicating the GPIO pin number connected to "B" on the
            rotary encoder.
        PIN_X: An integer indicating the GPIO pin number connected to "X" on the
            rotary encoder.
    """
    PULSES_PER_REVOLUTION = 2048    # The number of pulses sent by the encoder per revolution.

    class Direction(Enum):
        """Stores the states of the encoder's direction."""
        CW = "Clockwise"
        CCW = "Counterclockwise"

    def __init__(self, PIN_A, PIN_B, PIN_X):
        """Initializes RotaryEncoder with the "A", "B", and "X" pins and sets
        all pins as inputs.
        """

        """Initialize GPIO pin numbers"""
        self.PIN_A = PIN_A
        self.PIN_B = PIN_B
        self.PIN_X = PIN_X

        """Specify GPIO pins as inputs/outputs"""
        GPIO.setup(self.PIN_A, GPIO.IN)
        GPIO.setup(self.PIN_B, GPIO.IN)
        GPIO.setup(self.PIN_X, GPIO.IN)

        """Set default values"""
        self.angular_velocity = 0
        self.direction = self.Direction.CW
        self.enabled = True

    def run(self):
        """Runs the rotary encoder and outputs its angular velocity to the console."""
        SAMPLING_RATE = 1    # Amount of time elapsed before the angular velocity of the encoder is calculated [s]

        while (self.enabled):
            pulses_counted = 0
            time_elapsed = 0
            t_initial = time.perf_counter()
            previous_pin_A_state = GPIO.input(self.PIN_A)
            while (time_elapsed < SAMPLING_RATE):
                pin_A_state = GPIO.input(self.PIN_A)
                pin_B_state = GPIO.input(self.PIN_B)
                print (pin_A_state)
                print(pin_B_state)

                self.direction = self.__get_direction(pin_A_state, pin_B_state, previous_pin_A_state)
                last_state = GPIO.input(self.PIN_A)

                if (pin_B_state == 1):
                    pulses_counted += 1
                if (pin_B_state == 1):
                    pulses_counted += 1

                time_elapsed = time.perf_counter() - t_initial

            self.angular_velocity = self.__calculate_angular_velocity(pulses_counted, time_elapsed)
            print("Encoder angular velocity: " + str(self.angular_velocity))

    def __get_direction(self, pin_A_state, pin_B_state, previous_pin_A_state):
        """Determines the direction in which the encoder is rotating.

        Args:
            pin_A_state: An integer corresponding to the current state (high, 1 or low, 0) of pin A.
            pin_B_state: An integer corresponding to the current state (high, 1 or low, 0) of pin B.
            previous_pin_A_state: An integer corresponding to the previous state (high, 1 or low, 0) of pin A.

        Returns:
            The direction in which the encoder is rotating.
        """
        if (pin_A_state != previous_pin_A_state):
            if (pin_B_state != pin_A_state):
                return self.Direction.CW
            else:
                return self.Direction.CCW

    def __calculate_angular_velocity(self, pulses_counted, time_interval):
        """Calculates the angular velocity of the encoder.

        Args:
            pulses_counted: The number of pulses counted during the specified
                time interval.
            time_interval: An number indicating the amount of time elapsed.

        Returns:
            The calculated angular velocity of the encoder.
        """
        angular_velocity = (pulses_counted / RotaryEncoder.PULSES_PER_REVOLUTION) * (60 / time_interval)
        if (self.direction == self.Direction.CW):
            angular_velocity *= -1
        return angular_velocity
