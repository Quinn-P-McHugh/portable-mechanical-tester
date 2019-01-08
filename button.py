import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class Button:
    """Represents a button connected to a specified GPIO pin on the Raspberry Pi."""

    def __init__(self, PIN, CALLBACK, BOUNCE_TIME = 300):
        """Called when a new Button object is created.

        @param PIN: The pin connected to the button.
        @param CALLBACK: The name of the function to execute when the button is pressed."""
        self.PIN = PIN
        self.CALLBACK = CALLBACK
        self.BOUNCE_TIME = BOUNCE_TIME

        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.PIN, GPIO.RISING, callback=self.CALLBACK, bouncetime=self.BOUNCE_TIME)
