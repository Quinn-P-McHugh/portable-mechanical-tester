"""Module defining LoadCell class and related functions.

Original Source Code: https://github.com/dcrystalj/HX711py3, comes with Apache 2.0 license

Uses Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
"""

import load_cell_amplifier
import statistics

class LoadCell:
    def __init__(self, source=None, samples=20, spikes=4, sleep=0.1):

        self.source = source or LoadCellAmplifier()
        self.samples = samples
        self.spikes = spikes
        self.sleep = sleep
        self.history = []

        self.enabled = True

    def newMeasure(self):
        value = self.source.getWeight()
        self.history.append(value)

    def getMeasure(self):
        """Useful for continuous measurements."""
        self.newMeasure()
        # cut to old values
        self.history = self.history[-self.samples:]

        avg = statistics.mean(self.history)
        deltas = sorted([abs(i-avg) for i in self.history])

        if len(deltas) < self.spikes:
            max_permitted_delta = deltas[-1]
        else:
            max_permitted_delta = deltas[-self.spikes]

        valid_values = list(filter(
            lambda val: abs(val - avg) <= max_permitted_delta, self.history
        ))

        avg = statistics.mean(valid_values)

        return avg

    def getWeight(self, samples=None):
        """Get weight for once in a while. It clears history first."""
        self.history = []

        [self.newMeasure() for i in range(samples or self.samples)]

        return self.getMeasure()

    def tare(self, times=25):
        self.source.tare(times)

    def setOffset(self, offset):
        self.source.setOffset(offset)

    def setReferenceUnit(self, reference_unit):
        self.source.setReferenceUnit(reference_unit)

    def powerDown(self):
        self.source.powerDown()

    def powerUp(self):
        self.source.powerUp()

    def reset(self):
        self.source.reset()

    def run(self):
        """Determines the force applied onto the load cell and outputs
        it the console.
        """
        self.enabled = True
        while (self.enabled):
            # TODO: Set load cell amplifier reference unit using instructions in LoadCellAmplifier _init__
            weight = self.get_weight()
            print("Load Cell Reading: " + "{0: 4.4f}".format(weight))

    def stop(self):
        """Stops the load cell from outputting values to the console."""
        self.enabled = False
