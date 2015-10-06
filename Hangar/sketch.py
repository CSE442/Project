#!/usr/bin/env python2
# encoding: utf-8

import Queue

class Encodable(object):
    @staticmethod
    def from_json():
        raise NotImplementedException()
        
    def to_json(s):
        raise NotImplementedException()

class State(object, Encodable):
    """
    State is a value-semantic type that retains the salient attributes of
    the state of the game at a given point in time.
    """
    def __init__(self, dictionary_args):
        """TODO: to be defined1.
        :dictionary_args: TODO
        """
    self._dictionary_args = dictionary_args
    tanks            = { }                         # uuid -> car object, uuid == hexcolor?
    projectiles      = { }                         # uuid -> projectile object
    prefabs          = { }                         # uuid -> prefab object
    unity_connection = { }                         # TCP Bookkeeping: Port address, is alive, etc.
    phone_connection = { }                         # uuid -> use bluetooth id ? 
    car_connection   = { }                         # uuid -> use bluetooth id ?, pulling from car object? Discuss
    message_to_phone = Queue.Queue()
    message_to_car   = Queue.Queue()
    state_generation_time = 0                      # Will be replaced by system time
    game_start_time = 0                            # Will be replaced by the system time at initially generated state
    
def terraform(previous_state, updates_dictionary):
    """PUT INTO NEW DOCUMENT
    Processes previous state and change events,
    to provide well formed arguments to construct state

    :previous_state: TODO
    :updates_dictionary: TODO
    :returns: TODO

    """
    pass

def updates(previous_state, event):
    """Takes in events and outputs updates_dictionary
    :arg1: TODO
    :returns: TODO
    """
    pass            

class Orientation(object):
    def __init__(self):
        self.position     = {}
        self.velocity     = {}
        self.acceleration = {}
        self.angle        = {}

class Player(object):
    """Class to keep track of player associated atributes"""
    def __init__(self):


        bluetooth_uuid

class Tank(object):
    """
    Docstring for Tank.
    """
    def __init__(self, turret = Turret(), uuid = Uuid.generate()):
        """TODO: to be defined. """
        self.turret = turret
        self.uuid = uuid
        self.orientation = orientation
        self.player_uuid = player_uuid


class Weapon(object):
    """
    Weapon is an examplar of an enumerated type.
    """
    
    @staticmethod
    def default():
        return DefaultWeapon()
    
    def ammo(self):
        raise NotImplementedException()
        
    def fire(self):
        raise NotImplementedException()
        
    def uuid(self):
        raise NotImplementedException()
        
class DefaultWeapon(Weapon):
    """
    """
    
    def __init__(self, uuid = Uuid.generate()):
        self.uuid = uuid
        pass
        
    def ammo(self):  
        pass
        
    def fire(self):
        pass
        
    def uuid(self):
        return self.uuid
        
    
class Explodingbunnies(Weapon):
    """
    Luanch exlploding bunnies option
    """        
    @staticmethod
    def maximum_ammo():
        return 200
    
    def __init__(self, ammo = 0):
        self.ammo = ammo
    
    def bunny(self):
        pass

 
class FlamethrowerWeapon(Weapon):
    """
    Flamethrower optional weapon
    """
    
    def __init__(self, ammo = 0):
        self.ammo = ammo
    
    def fire(self):
        pass

class Uuid(object):
    """
    Uuid is a utility class for creating globally unique identifiers
    """
    next_uuid = 0
    
    @staticmethod
    def generate():
        next_uuid += 1
        return next_uuid

class Turret(object):
    """
    Turret is a value-semantic type that represents the
    salient attributes of a tank turret.
    """
    def __init__(self, weapon = Weapon.default()):
        """TODO: to be defined. """
        self.weapon = weapon