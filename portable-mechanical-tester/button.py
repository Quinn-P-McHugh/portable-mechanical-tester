"""Module defining Button class and related functions.

Uses Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
"""

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class Button:
    """Represents a button connected to a specified GPIO pin on the Raspberry Pi.

    Attributes:
        PIN: An integer indicating the GPIO pin number that the button is connected to.
        CALLBACK: A string containing name of the function that will be executed when the
            button is pressed.
        BOUNCE_TIME: An integer indicating the amount of time to wait after the
            button is pressed before another button press can be registered [ms].
    """

    def __init__(self, PIN, CALLBACK, BOUNCE_TIME = 300):
        """Initializes Button with a GPIO pin number, callback function, and
        a bounce time. Sets GPIO pin as input and begins button press detection.
        """
        self.PIN = PIN
        self.CALLBACK = CALLBACK
        self.BOUNCE_TIME = BOUNCE_TIME

        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.PIN, GPIO.RISING, callback=self.CALLBACK, bouncetime=self.BOUNCE_TIME)
