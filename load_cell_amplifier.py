#!/usr/bin/python3
# Development for reading SparkFun HX711 load cell amplifier
# from https://github.com/dcrystalj/HX711py3, comes with Apache 2.0 license
# Sets up LoadCellAmplifier class to make load cell usage simple
import RPi.GPIO as GPIO
import time
import statistics

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class LoadCellAmplifier:
    """Represents a HX711 load cell amplifier."""

    def __init__(self, PIN_DAT, PIN_CLK, GAIN = 128, bitsToRead = 24):
        """Called when a new LoadCellAmplifier object is created.

        @param PIN_DAT: The pin connected to "DAT" on the load cell amplifier.
        @param PIN_CLK: The pin connected to "CLK" on the load cell cell amplifier.
        @param GAIN: The GAIN of the load cell amplifier.
        @param bitsToRead"""

        self.PIN_CLK = PIN_CLK
        self.PIN_DAT = PIN_DAT

        GPIO.setup(self.PIN_CLK, GPIO.OUT)
        GPIO.setup(self.PIN_DAT, GPIO.IN)

        # The value returned by the hx711 that corresponds to your
        # reference unit AFTER dividing by the SCALE.
        self.REFERENCE_UNIT = 1

        self.GAIN = 0
        self.OFFSET = 1
        self.lastVal = 0
        self.bitsToRead = bitsToRead
        self.twosComplementThreshold = 1 << (bitsToRead-1)
        self.twosComplementOffset = -(1 << (bitsToRead))
        self.setGAIN(GAIN)
        self.read()

        # HOW TO CALCULATE THE REFFERENCE UNIT
        #########################################
        # To set the reference unit to 1.
        # Call get_weight before and after putting 1000g weight on your sensor.
        # Divide difference with grams (1000g) and use it as reference unit.
        self.setReferenceUnit(21)
        self.reset()
        self.tare()

        self.enabled = True

    def run(self):
        self.enabled = True
        while (self.enabled):
            weight = self.getWeight()
            print("Load Cell Reading: " + "{0: 4.4f}".format(weight))

    def stop(self):
        self.enabled = False

    def isReady(self):
        return GPIO.input(self.PIN_DAT) == 0

    def setGAIN(self, GAIN):
        if GAIN is 128:
            self.GAIN = 1
        elif GAIN is 64:
            self.GAIN = 3
        elif GAIN is 32:
            self.GAIN = 2

        GPIO.output(self.PIN_CLK, False)
        self.read()

    def waitForReady(self):
        while not self.isReady():
            pass

    def correctTwosComplement(self, unsignedValue):
        if unsignedValue >= self.twosComplementThreshold:
            return unsignedValue + self.twosComplementOffset
        else:
            return unsignedValue

    def read(self):
        self.waitForReady()

        unsignedValue = 0
        for i in range(0, self.bitsToRead):
            GPIO.output(self.PIN_CLK, True)
            bitValue = GPIO.input(self.PIN_DAT)
            GPIO.output(self.PIN_CLK, False)
            unsignedValue = unsignedValue << 1
            unsignedValue = unsignedValue | bitValue

        # set channel and GAIN factor for next reading
        for i in range(self.GAIN):
            GPIO.output(self.PIN_CLK, True)
            GPIO.output(self.PIN_CLK, False)

        return self.correctTwosComplement(unsignedValue)

    def getValue(self):
        return self.read() - self.OFFSET

    def getWeight(self):
        value = self.getValue()
        value /= self.REFERENCE_UNIT
        return value

    def tare(self, times=25):
        reference_unit = self.REFERENCE_UNIT
        self.setReferenceUnit(1)

        # remove spikes
        cut = times//5
        values = sorted([self.read() for i in range(times)])[cut:-cut]
        offset = statistics.mean(values)

        self.setOffset(offset)

        self.setReferenceUnit(reference_unit)

    def setOffset(self, offset):
        self.OFFSET = offset

    def setReferenceUnit(self, reference_unit):
        self.REFERENCE_UNIT = reference_unit

    # HX711 datasheet states that setting the PDA_CLOCK pin on high
    # for a more than 60 microseconds would power off the chip.
    # I used 100 microseconds, just in case.
    # I've found it is good practice to reset the hx711 if it wasn't used
    # for more than a few seconds.
    def powerDown(self):
        GPIO.output(self.PIN_CLK, False)
        GPIO.output(self.PIN_CLK, True)
        time.sleep(0.0001)

    def powerUp(self):
        GPIO.output(self.PIN_CLK, False)
        time.sleep(0.0001)

    def reset(self):
        self.powerDown()
        self.powerUp()
