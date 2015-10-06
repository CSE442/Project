class Orientation(object):
    def __init__(self):
        self.position     = {}
        self.velocity     = {}
        self.acceleration = {}
        self.angle        = {}

class Tank(object):
    """
    Docstring for Tank.
    """
    def __init__(self, turret = Turret(), uuid = Uuid.generate()):
        """TODO: to be defined. """
        self.turret = turret
        self.uuid = uuid
        self.orientation = 

class Player(object):
    """
    Player associates a bluetooth id with a uuid
    """
    def __init__(self, btid = bluetoothid, uuid = Uuid.generate()):
        self.btid = btid
        self.uuid = uuid

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

class Turret(object):
    """
    Turret is a value-semantic type that represents the
    salient attributes of a tank turret.
    """
    def __init__(self, weapon = Weapon.default()):
        """TODO: to be defined. """
        self.weapon = weapon
