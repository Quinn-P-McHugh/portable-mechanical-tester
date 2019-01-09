"""Module defining LoadCellAmplifier class and related functions.

Source Code: https://github.com/dcrystalj/HX711py3, comes with Apache 2.0 license

Uses Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
"""

import RPi.GPIO as GPIO
import time
import statistics

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class LoadCellAmplifier:
    """Represents a HX711 load cell amplifier.

    Attributes:
        PIN: An integer indicating the GPIO pin connected to "DAT" on the load
            cell amplifier.
        PIN_CLK: An integer indicating the GPIO pin connected to "CLK" on the load
            cell amplifier.
        GAIN: An integer indicating the gain of the load cell amplifier.
        BITS_TO_READ: An integer indicating the number of bits to read before
            calculating a force value.
    """

    def __init__(self, PIN_DAT, PIN_CLK, GAIN = 128, BITS_TO_READ = 24):
        """Initializes LoadCellAmplifier with a "DAT" pin, a "CLK" pin, gain,
        and the number of bits to read. Tares load cell and begins reading values.
        """
        self.PIN_CLK = PIN_CLK
        self.PIN_DAT = PIN_DAT

        GPIO.setup(self.PIN_CLK, GPIO.OUT)
        GPIO.setup(self.PIN_DAT, GPIO.IN)

        # The value returned by the hx711 that corresponds to your
        # reference unit AFTER dividing by the SCALE.
        self.REFERENCE_UNIT = 1

        self.GAIN = 0
        self.OFFSET = 1
        self.BITS_TO_READ = BITS_TO_READ
        self.last_val = 0
        self.twos_complement_threshold = 1 << (BITS_TO_READ-1)
        self.twos_complement_offset = -(1 << (BITS_TO_READ))
        self.set_gain(GAIN)
        self.read()

        # HOW TO CALCULATE THE REFFERENCE UNIT
        #########################################
        # To set the reference unit to 1.
        # Call get_weight before and after putting 1000g weight on your sensor.
        # Divide difference with grams (1000g) and use it as reference unit.
        self.set_reference_unit(21)
        self.reset()
        self.tare()

        self.enabled = True

    def run(self):
        """Calculates the force applied onto the load cell and outputs
        it the console.
        """
        self.enabled = True
        while (self.enabled):
            weight = self.get_weight()
            print("Load Cell Reading: " + "{0: 4.4f}".format(weight))

    def stop(self):
        """Stops the load cell from outputting values to the console."""
        self.enabled = False

    def isReady(self):
        return GPIO.input(self.PIN_DAT) == 0

    def set_gain(self, gain):
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

        GPIO.output(self.PIN_CLK, False)
        self.read()

    def wait_for_ready(self):
        while not self.isReady():
            pass

    def correct_twos_complement(self, unsignedValue):
        if unsignedValue >= self.twos_complement_threshold:
            return unsignedValue + self.twos_complement_offset
        else:
            return unsignedValue

    def read(self):
        self.wait_for_ready()

        unsignedValue = 0
        for i in range(0, self.BITS_TO_READ):
            GPIO.output(self.PIN_CLK, True)
            bitValue = GPIO.input(self.PIN_DAT)
            GPIO.output(self.PIN_CLK, False)
            unsignedValue = unsignedValue << 1
            unsignedValue = unsignedValue | bitValue

        # set channel and GAIN factor for next reading
        for i in range(self.GAIN):
            GPIO.output(self.PIN_CLK, True)
            GPIO.output(self.PIN_CLK, False)

        return self.correct_twos_complement(unsignedValue)

    def get_value(self):
        return self.read() - self.OFFSET

    def get_weight(self):
        value = self.get_value()
        value /= self.REFERENCE_UNIT
        return value

    def tare(self, times=25):
        reference_unit = self.REFERENCE_UNIT
        self.set_reference_unit(1)

        # remove spikes
        cut = times//5
        values = sorted([self.read() for i in range(times)])[cut:-cut]
        offset = statistics.mean(values)

        self.set_offset(offset)

        self.set_reference_unit(reference_unit)

    def set_offset(self, offset):
        self.OFFSET = offset

    def set_reference_uni(self, reference_unit):
        self.REFERENCE_UNIT = reference_unit

    # HX711 datasheet states that setting the PDA_CLOCK pin on high
    # for a more than 60 microseconds would power off the chip.
    # I used 100 microseconds, just in case.
    # I've found it is good practice to reset the hx711 if it wasn't used
    # for more than a few seconds.
    def power_down(self):
        GPIO.output(self.PIN_CLK, False)
        GPIO.output(self.PIN_CLK, True)
        time.sleep(0.0001)

    def power_up(self):
        GPIO.output(self.PIN_CLK, False)
        time.sleep(0.0001)

    def reset(self):
        self.power_down()
        self.power_up()
