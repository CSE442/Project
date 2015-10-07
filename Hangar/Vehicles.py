#!/usr/bin/env python2
# encoding: utf-8

# file:Vehicles.py 
# desc:Basic data-types and methods for use by games "Vehicles"

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

class Turret(object):
    """
    Turret is a value-semantic type that represents the
    salient attributes of a tank turret.
    """
    def __init__(self, weapon = Weapon.default()):
        """TODO: to be defined. """
        self.weapon = weapon
        
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
