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
    set_open_callback = None
    set_close_callback = None
    orig_state = None

    def __init__(self, *args, **kwargs):
        super(GarageDoorSensor, self).__init__(args, **kwargs)
        
        if kwargs.get('read_pin') is not None:
            self.read_pin = kwargs['read_pin']

        GPIO.cleanup()
        GPIO.setup(self.read_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.orig_state = self.get_state()

        GPIO.add_event_detect(self.read_pin, GPIO.BOTH, bouncetime=0)
        if None not in [kwargs.get('open_callback'), 
                kwargs.get('close_callback')]:
            self.set_open_callback = kwargs.get('open_callback')
            self.set_close_callback = kwargs.get('close_callback')
            GPIO.add_event_callback(self.read_pin, self._callback_wrapper)
    
    def get_state(self):
        """
        return if the garage door is currently open or closed
        """
        current = GPIO.input(self.read_pin)
        if current == 1:
            return self.CLOSED
        else:
            return self.OPEN

    def _callback_wrapper(self, channel):
        """
        This is a wrapper function for the open/close callbacksj.
        Due to the nature of the reed switch it may fire multiple times during
        opening and closing. This function will only call callback when the 
        doors state has actually changed.
        """
        if (self.set_open_callback is not None) and \
            (self.set_close_callback is not None):
            new_state = self.get_state()
            if self.orig_state == self.CLOSED and new_state == self.OPEN:
                self.orig_state = new_state
                self.set_open_callback(channel)
            elif self.orig_state == self.OPEN and new_state == self.CLOSED:
                self.orig_state = new_state
                self.set_close_callback(channel)

