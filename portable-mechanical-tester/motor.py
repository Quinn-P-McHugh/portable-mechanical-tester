"""Module defining Motor class and related functions.

Uses Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
"""

from enum import Enum
import RPi.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class Motor:
    """Represents a stepper motor.

    Attributes:
        PIN_DIR: An integer indicating the GPIO pin number of the direction pin.
            Connected to "DIR-" on the microstep driver.
        PIN_PUL: An integer indicating the GPIO pin number of the pulse pin.
            Connected to "PUL-" on the microstep driver.
        PIN_ENA: An integer indicating the GPIO pin number of the enable pin.
            Connected to "ENA-" on the microstep driver.
    """
    STEPS_PER_REVOLUTION = 200  # The amount of steps that the motor needs to take to turn 1 revolution

    class Direction(Enum):
        """Stores the states of the motor's direction."""
        CW = "Clockwise"
        CCW = "Counterclockwise"

    def __init__(self, PIN_DIR, PIN_PUL, PIN_ENA = None):
        """Initializes Motor class with GPIO pin numbers for direction, pulse,
        and enable pins.
        """

        """Initialize pin numbers"""
        self.PIN_DIR = PIN_DIR
        self.PIN_PUL = PIN_PUL
        self.PIN_ENA = PIN_ENA

        """Specify GPIO pins as input/outputs"""
        GPIO.setup(self.PIN_DIR, GPIO.OUT)
        GPIO.setup(self.PIN_PUL, GPIO.OUT)
        if PIN_ENA is not None:
            GPIO.setup(self.PIN_ENA, GPIO.OUT)

        """Set default values"""
        self.enabled = True     # Keeps track of the enable pin's state
        if PIN_ENA is not None:
            GPIO.output(self.PIN_ENA, self.enabled)

        self.set_direction(self.Direction.CW)  # Sets the initial motor direction as clockwise
        self.speed = 100          # Default speed of the motor [steps/s]

    def move_CW(self):
        """Turns the motor a single step clockwise (when looking at the motor's top face)."""
        print("Move CW pressed")
        if (self.enabled):
            if (self.direction == self.Direction.CW):
                print("ERROR: Motor is already turning CW")
            else:
                self.disable()
        else:
            self.enable()
            self.set_direction(self.Direction.CW)
            threading.Thread(target=self.__move).start()
            print("Motor CW")

    def move_CCW(self):
        """Turns the motor a single step counterclockwise (when looking at the
        motor's top face).
        """
        print("Move CCW pressed")
        if (self.enabled):
            if (self.direction == self.Direction.CCW):
                print("ERROR: Motor is already turning CCW")
            else:
                self.disable()
        else:
            self.enable()
            self.set_direction(self.Direction.CCW)
            threading.Thread(target=self.__move).start()
            print("Motor CCW")

    def __move(self):
        """Moves the motor a single step in whichever direction the direction
        is set.
        """
        while (self.enabled):
            GPIO.output(self.PIN_PUL, 1)
            time.sleep(2/self.speed)
            GPIO.output(self.PIN_PUL, 0)
            time.sleep(2/self.speed)

    def disable(self):
        """Disables the motor and updates its 'enabled' state."""
        if self.PIN_ENA is not None:
            GPIO.output(self.PIN_ENA, 0)
        self.enabled = False
        print ("Motor DISABLED")

    def enable(self):
        """Enables the motor and updates its 'enabled' state."""
        if self.PIN_ENA is not None:
            GPIO.output(self.PIN_ENA, 1)
        self.enabled = True
        print ("Motor ENABLED")

    def set_direction(self, direction):
        """Sets the direction of the motor and updates its 'direction' state.

        Args:
            direction: An Enum value indicating the direction the motor should
            turn.
        """
        if (direction == self.Direction.CW):
            self.direction = self.Direction.CW
            GPIO.output(self.PIN_DIR, 1)
        elif (direction == self.Direction.CCW):
            self.direction = self.Direction.CCW
            GPIO.output(self.PIN_DIR, 0)
        else:
            print ("ERROR: Invalid direction specified.")
