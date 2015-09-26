#!/usr/bin/env python2
# encoding: utf-8

import Queue

class State(object):

    """State of the game, immutable"""

    def __init__(self, dictionary_args):
        """TODO: to be defined1.

        :dictionary_args: TODO

        """
        self._dictionary_args = dictionary_args

    tanks = { }                                # uuid -> car object, uuid == hexcolor?
    projectiles = { }                         # uuid -> projectile object
    prefabs = { }                             # uuid -> prefab object
    unity_connection = { }                    # TCP Bookkeeping: Port address, is alive, etc.
    phone_connection = { }                    # uuid -> use bluetooth id ? 
    car_connection = { }                      # uuid -> use bluetooth id ?, pulling from car object? Discuss
    message_to_phone = Queue.Queue()
    message_to_car = Queue.Queue()
    state_generation_time = 0                 # Will be replaced by system time
    game_start_time = 0                       # Will be replaced by the system time at initially generated state
    
def teraformer(previous_state, updates_dictionary):
    """PUT INTO NEW DOCUMENT
    Processes previous state and change events,
    to provide well formed arguments to construct state

    :previous_state: TODO
    :updates_dictionary: TODO
    :returns: TODO

    """
    pass

def updates(arg1):
    """Takes in events and outputs updates_dictionary

    :arg1: TODO
    :returns: TODO

    """
    pass


class Tank(object):

    """Docstring for Tank. """

    def __init__(self):
        """TODO: to be defined1. """
        
