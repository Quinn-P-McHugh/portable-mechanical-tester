"""Module defining LinearActuator class and related functions.

Uses Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
"""

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class LinearActuator:
    """Represents a linear actuator actuated by a stepper motor.

    Attributes:
        MOTOR: The Motor object that actuates the linear actuator.
        speed: An integer representing the speed of the motor [mm/s].
        SCREW_LEAD: AN integer specifying the linear distance that the linear
            actuator carriage travels per revolution of the lead screw.
            Lead for the SFU1605 ball screw is 5mm:
            (Page 4) https://www.linearmodul.dk/Filer/PDF-Kataloger/PDF-Katalog%20Ballscrews.pdf
    """
    MAX_SPEED = 500   # The maximum speed of the linear actuator [mm/s]
    MIN_SPEED = 0    # The minimum speed of the linear actuator [mm/s]

    def __init__(self, MOTOR, speed = 500, SCREW_LEAD = 5):
        """Initializes LinearActuator with a motor and and an initial speed."""
        self.MOTOR = MOTOR
        self.set_speed(speed)
        self.SCREW_LEAD = SCREW_LEAD

    def move_down(self, test):
        """Moves the linear actuator downwards."""
        self.MOTOR.move_CCW()

    def move_up(self, test):
        """Moves the linear actuator upwards."""
        self.MOTOR.move_CW()

    def stop(self, test):
        """Stops the linear actuator."""
        self.MOTOR.disable()

    def increase_speed(self, test):
        """Increases the speed of the linear actuator by a specified increment."""
        INCREMENT = 25  # How much the speed of the MOTOR should be increased by [mm/s]
        if (self.speed + INCREMENT >= LinearActuator.MAX_SPEED):
            print ("ERROR: Linear actuator has reached its maximum speed.")
        else:
            print ("INCREMENT: " + str(INCREMENT) + "     " + "Speed: " + str(self.speed))
            self.set_speed(self.speed + INCREMENT)
            print ("Linear actuator speed increased to: " + str(self.speed))
            print ("MOTOR speed increased to:           " + str(self.MOTOR.speed))

    def decrease_speed(self, test):
        """Decreases the speed of the linear actuator by a specified decrement."""
        DECREMENT = 25 # How much the speed of the MOTOR should be decreased by [mm/s]
        if (self.speed - DECREMENT <= LinearActuator.MIN_SPEED):
            print ("ERROR: Linear actuator has reached its minimum speed.")
        else:
            print ("DECREMENT: " + str(DECREMENT) + "     " + "Speed: " + str(self.speed))
            self.set_speed(self.speed - DECREMENT)
            print ("Linear actuator speed decreased to: " + str(self.speed))
            print ("MOTOR speed decreased to:           " + str(self.MOTOR.speed))


    def set_speed(self, speed):
        """Sets the speed of both the linear actuator and the motor that drives it.

        Args:
            speed: The speed of the linear actuator [mm/s].
        """
        if (speed > LinearActuator.MAX_SPEED):
            speed = LinearActuator.MAX_SPEED
            print("Linear actuator speed set to maximum speed.")
        elif (speed < LinearActuator.MIN_SPEED):
            speed = LinearActuator.MIN_SPEED
            print("Linear actuator speed set to minimum speed.")
        self.speed = speed
        self.MOTOR.speed = self.convert_to_steps_per_s(self.speed)

    def convert_to_steps_per_s(self, linear_speed):
        """Converts the linear speed of the linear actuator to rotational speed
        of the motor.

        Args:
            linear_speed: An integer indicating the speed of the linear actuator [mm/s].

        Returns:
            An integer indicating to the rotational speed of the motor [steps/s].
        """
        rpm = linear_speed * (1/self.SCREW_LEAD) * 60  # [mm/s] * [1rev/mm] * [60s/1min] = [rev/min]
        steps_per_s = rpm * (1/60) * self.MOTOR.STEPS_PER_REVOLUTION     # [rev/min] * [1min/60s] * [steps/rev] = [steps/s]
        return steps_per_s
