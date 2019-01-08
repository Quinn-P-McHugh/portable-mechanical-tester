import RPi.GPIO as GPIO
from time import sleep
import threading
from enum import Enum


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class Motor:
    """Represents a stepper motor."""
    STEPS_PER_REVOLUTION = 200  # The amount of steps that the motor needs to take to turn 1 revolution

    class Direction(Enum):
        """Stores the states of the encoder's direction."""
        CW = "Clockwise"
        CCW = "Counterclockwise"

    def __init__(self, PIN_DIR, PIN_PUL, PIN_ENA = None):
        """Called when a new Motor object is created.

        @param PIN_DIR: The direction pin. Connected to "DIR-" on the microstep driver.
        @param PIN_PUL: The pulse pin. Connected to "PUL-" on the microstep driver.
        @param PIN_ENA: The enable pin. Connected to "ENA-" on the microstep driver."""

        # Initialize pin numbers
        self.PIN_DIR = PIN_DIR
        self.PIN_PUL = PIN_PUL
        self.PIN_ENA = PIN_ENA

        # Specify GPIO pins as input/outputs
        GPIO.setup(self.PIN_DIR, GPIO.OUT)
        GPIO.setup(self.PIN_PUL, GPIO.OUT)
        if PIN_ENA is not None:
            GPIO.setup(self.PIN_ENA, GPIO.OUT)

        self.enabled = True                        # Keeps track of the enable pin's state
        if PIN_ENA is not None:
            GPIO.output(self.PIN_ENA, self.enabled)

        self.set_direction(self.Direction.CW)  # Sets the initial motor direction as clockwise
        self.speed = 100          # Default speed of the motor [steps/s]

    def move_CW(self):
        """Turns the motor a single step clockwise (when looking at the motor's top face).

        @param speed: The rotational speed of the motor [steps/s]."""
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
        """Turns the motor a single step counterclockwise (when looking at the motor's top face).

        @param speed: The rotational speed of the motor [steps/s]."""
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
        """Moves the motor a single step in whichever direction the PIN_DIR is set.

        @param speed: The rotational speed [steps/s]."""
        while (self.enabled):
            GPIO.output(self.PIN_PUL, 1)
            sleep(2/self.speed)
            GPIO.output(self.PIN_PUL, 0)
            sleep(2/self.speed)

    def disable(self):
        """disables the motor and updates its 'enabled' state."""
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

        @param direction: The direction that the motor should turn -- either self.Direction.CW or self.Direction.CCW."""
        if (direction == self.Direction.CW):
            self.direction = self.Direction.CW
            GPIO.output(self.PIN_DIR, 1)
        elif (direction == self.Direction.CCW):
            self.direction = self.Direction.CCW
            GPIO.output(self.PIN_DIR, 0)
        else:
            print ("ERROR: Invalid direction specified.")
