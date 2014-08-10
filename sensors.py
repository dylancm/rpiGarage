"""
This file contains the classes used to interface with the various sensors in
the garage.
"""
import logging

import RPi.GPIO as GPIO

LOGGER = logging.getLogger(__name__)


class Sensor(object):
    """
    This is the super class for all sensor objects
    """
    def __init__(self, args, **kwargs):
        GPIO.setmode(GPIO.BOARD)


class GarageDoorSensor(Sensor):
    """
    The GarageDoorSensor object provides access to the state of the garage door
    (open/closed)
    """
    # STATICS
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    DOOR_STATE = {
            'OPEN': OPEN,
            'CLOSED': CLOSED
        }

    # instance_vars
    read_pin = 7
    update_callback = None

    def __init__(self, args, **kwargs):
        super(GarageDoorSensor, self).__init__(args, **kwargs)
        
        if kwargs.get('read_pin') is not None:
            self.read_pin = kwargs['read_pin']

        GPIO.setup(self.read_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        if kwargs.get('callback') is not None:
            GPIO.add_event_callback(self.read_pin, kwargs.get('callback'))
    
    def get_state(self):
        """
        return if the garage door is currently open or closed
        """
        current = GPIO.input(self.read_pin)
        if current == 1:
            return self.CLOSED
        else:
            return self.OPEN

