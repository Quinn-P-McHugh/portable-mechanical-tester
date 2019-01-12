"""Module containing code to start and control the portable mechanical tester.

Uses Google Python Style Guide: https://google.github.io/styleguide/pyguide.html

Prof Instruments - Portable Mechanical Tester
Last Updated: January 8th, 2018

Authors:
Quinn McHugh
Ridwan Alaoudian
Tyler Bursa
"""

# Import classes
from button import Button
from limit_switch import LimitSwitch
from linear_actuator import LinearActuator
from load_cell_amplifier import LoadCellAmplifier
from motor import Motor
from rotary_encoder import RotaryEncoder

import multiprocessing

# Initialize objects
motor = Motor(20, 21)
linear_actuator = LinearActuator(motor)
rotary_encoder = RotaryEncoder(24, 18, 23)
load_cell_amplifier = LoadCellAmplifier(9, 11)
load_cell = LoadCell

# Initialize buttons
up_button = Button(3, linear_actuator.move_up)
down_button = Button(4, linear_actuator.move_down)
stop_button = Button(2, linear_actuator.stop)
inc_speed_button = Button(6, linear_actuator.increase_speed)
dec_speed_button = Button(5, linear_actuator.decrease_speed)

# Initialize limit switches
bottom_limit_switch = LimitSwitch(17, linear_actuator.stop)
top_limit_switch = LimitSwitch(27, linear_actuator.stop)

# Run load cell and rotary encoder in separate processes
multiprocessing.Process(target=load_cell_amplifier.run).start()
multiprocessing.Process(target=rotary_encoder.run).start()
