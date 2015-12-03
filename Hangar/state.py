#!/usr/local/env python2
#
# file:    state.py
# authors: Nathan Burgers
#
# purpose: Provide the implementation of the game state

import time
import json
import math

class DictionaryUtil(object):
    @staticmethod
    def from_json(self, value_type):
        result = {}
        for key in self:
            value = self[key]
            result[key] = value_type.from_json(value)
        return result

    @staticmethod
    def to_json(self):
        result = {}
        for key in self:
            value = self[key]
            result[key] = value.to_json()
        return result

class Quaternion(object):
    def __init__(self, a = 0.0, i = 0.0, j = 0.0, k = 0.0):
        assert type(a) is float
        assert type(i) is float
        assert type(j) is float
        assert type(k) is float
        self.a = a
        self.i = i
        self.j = j
        self.k = k

    @staticmethod
    def unit():
        return Quaternion(1.0, 0.0, 0.0, 0.0)

    @staticmethod
    def from_axis_angle(x = 0.0, y = 0.0, z = 0.0, angle = 0.0):
        normal = math.sqrt(x**2 + y**2 + z**2)
        normal_x = x / normal
        normal_y = y / normal
        normal_z = z / normal
        return Quaternion(math.cos(angle/2),
                          normal_x * math.sin(angle/2),
                          normal_y * math.sin(angle/2),
                          normal_z * math.sin(angle/2))

    def tuple(self):
        return (self.a, self.i, self.j, self.k)

    def normalize(self):
        n = sqrt(self.a * self.a +
                 self.i * self.i +
                 self.j * self.j +
                 self.k * self.k)
        return Quaternion(self.a / n,
                          self.i / n,
                          self.j / n,
                          self.k / n)

    def matrix3x3(self):
        normal = self.normalize()
        a = normal.a
        i = normal.i
        j = normal.j
        k = normal.k
        return Matrix3x3((1 - 2*j**2 - 2*k**2,  2*i*j - 2*k*a,  2*i*k + 2*j*a),
                         (2*i*j + 2*a*k,  1 - 2*i**2 - 2*k**2,  2*j*k - 2*i*a),
                         (2*i*k - 2*j*a,  2*j*k + 2*i*a,  1 - 2*i**2 - 2*j**2))

    @staticmethod
    def from_json(json):
        return Quaternion(json['a'],
                          json['i'],
                          json['j'],
                          json['k'])

    def to_json(self):
        return { 'a': self.a, 'i': self.i, 'j': self.j, 'k': self.k }

    def __add__(self, other):
        assert type(other) is Quaternion
        return Quaternion(self.a + other.a,
                          self.i + other.i,
                          self.j + other.j,
                          self.k + other.k)

    def __sub__(self, other):
        assert type(other) is Quaternion
        return Quaternion(self.a - other.a,
                          self.i - other.i,
                          self.j - other.j,
                          self.k - other.k)

    def __mul__(self, other):
        if type(other) is float:
            return Quaternion(self.a * other,
                              self.i * other,
                              self.j * other,
                              self.k * other)
        elif type(other) is Quaternion:
            r = self
            q = other
            return Quaternion(r.a*q.a - r.i*q.i - r.j*q.j - r.k*q.k,
                              r.a*q.i + r.i*q.a - r.j*q.k + r.k*q.j,
                              r.a*q.j + r.i*q.k + r.j*q.a - r.k*q.i,
                              r.a*q.k - r.i*q.j + r.j*q.i + r.k*q.a)
        else:
            raise TypeError()

    def __rmul__(self, other):
        assert type(other) is float
        return self * other

class Matrix3x3(object):
    def __init__(self, rows):
        assert type(rows) is tuple
        assert len(rows) is 3
        for i in range(0,3):
            assert len(rows[i]) is 3
            for j in range(0,3):
                assert type(rows[i][j]) is float
        self.rows = rows

    @staticmethod
    def zero():
        return Matrix3x3((0, 0, 0),
                         (0, 0, 0),
                         (0, 0, 0))

    @staticmethod
    def identity():
        return Matrix3x3(((1, 0, 0),
                          (0, 1, 0),
                          (0, 0, 1)))

    def __getitem__(self, key):
        if type(key) is tuple:
            row, column = key
            return self.rows[row][column]
        elif type(key) is int:
            return self.row_vector(key)
        else:
            raise TypeError()

    def __setitem__(self, key, value):
        if type(key) is tuple:
            assert type(value) is float
            row, column = key
            self.rows[row][column] = value
        elif type(key) is int:
            assert type(value) is Vector3
            self.rows[row] = value
        else:
            raise TypeError()

    def row_vector(self, index):
        assert type(index) is int
        assert index >= 0
        assert index < 3
        return Vector3.from_tuple(self.rows[index])

    def column_vector(self, index):
        assert type(index) is int
        assert index >= 0
        assert index < 3
        return Vector3(self.rows[0][index],
                       self.rows[1][index],
                       self.rows[2][index])

    @staticmethod
    def from_json(json):
        return Matrix3x3((Vector3.from_json(json[0]),
                          Vector3.from_json(json[1]),
                          Vector3.from_json(json[2])))

    def to_json(self):
        return [ self.row_vector(0).to_json(),
                 self.row_vector(1).to_json(),
                 self.row_vector(2).to_json() ]

    def __mul__(self, other):
        if type(other) is float:
            result = Matrix3x3.zero()
            for row in range(0, 3):
                for column in range(0, 3):
                    result.rows[row][column] = other * self.rows[row][column]
            return result
        elif type(other) is Vector3:
            return Vector3(self.row_vector(0).dot(other),
                           self.row_vector(1).dot(other),
                           self.row_vector(2).dot(other))
        elif type(other) is Matrix3x3:
            result = Matrix3x3.zero()
            for row in range(0, 3):
                for column in range(0, 3):
                    row_vector = self.row_vector(row)
                    column_vector = self.column_vector(column)
                    result[row][column] = row_vector.dot(column_vector)
            return result
        else:
            raise TypeError()

    def __rmul__(self, other):
        if type(other) is float:
            return self * other
        elif type(other) is Vector3:
            return self * other
        else:
            raise TypeError()

class Vector3(object):
    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        assert type(x) is float
        assert type(y) is float
        assert type(z) is float
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def from_tuple(tuple):
        return Vector4(tuple[0], tuple[1], tuple[2])

    def list(self):
        return [self.x, self.y, self.z]

    def tuple(self):
        return (self.x, self.y, self.z)

    def dot(self, other):
        assert type(other) is Vector3
        return self.x * other.x + self.y * other.y + self.z * other.z

    def distance(self, other):
        assert type(other) is Vector3
        return sqrt((self.x - other.x) ** 2 +
                    (self.y - other.y) ** 2 +
                    (self.z - other.z) ** 2)

    @staticmethod
    def from_json(json):
        return Vector3(json[0], json[1], json[2])

    def to_json(self):
        return [self.x, self.y, self.z]

    def __add__(self, other):
        assert type(other) is Vector3
        return Vector3(self.x + other.x,
                       self.y + other.y,
                       self.z + other.z)

    def __sub__(self, other):
        assert type(other) is Vector3
        return Vector3(self.x - other.x,
                       self.y - other.y,
                       self.z - other.z)

    def __mul__(self, other):
        assert type(other) is float
        return Vector3(self.x * other,
                       self.y * other,
                       self.z * other)

    def __rmul__(self, other):
        assert type(other) is float
        return self * other

class Orientation(object):
    def __init__(
            self,
            linear = Vector3(),
            angular = Quaternion.unit()):
        assert isinstance(linear, Vector3)
        assert isinstance(angular, Quaternion)
        self._linear = linear
        self._angular = angular

    def linear(self):
        return self._linear

    def angular(self):
        return self._angular

    @staticmethod
    def from_json(json):
        return Orientation(Vector3.from_json(json._linear),
                           Quaternion.from_json(json._angular))

    def to_json(self):
        return {
            'linear': self._linear.to_json(),
            'angular': self._angular.to_json()
        }

class Physics(object):
    def __init__():
        raise NotImplementedError()

    @staticmethod
    def entities_do_collide(
            position_0 = Vector3(),
            position_1 = Vector3(),
            distance_threshold = 0.0):
        assert isinstance(position_0, Vector3)
        assert isinstance(position_1, Vector3)
        assert type(distance_threshold) is float
        return Vector3.distance(position_0, position_1) <= distance_threshold

    @staticmethod
    def project(
            orientation = Orientation(),
            first_derivative = Orientation(),
            second_derivative = Orientation(),
            delta_time = 0.0):
        """
        Progress the specified 'orientation' along the specified 'velocity'
        by the specified 'delta_time'.
        """
        assert type(orientation) is Orientation
        assert type(velocity) is Velocity
        assert type(delta_time) is float
        linear_velocity_delta = first_derivative.linear() + \
                (second_derivative.linear() * delta_time)
        angular_velocity_delta = first_derivative.angular() * \
                (second_derivative.angular() * delta_time)
        linear = orientation.linear() + linear_velocity_delta * delta_time
        angular = orientation.angular() * (angular_velocity_delta * delta_time)
        return Orientation(linear, angular)

class Uuid(object):
    next = 0

    @staticmethod
    def generate():
        Uuid.next += 1
        return Uuid.next

class Bullet(object):
    def __init__():
        raise NotImplementedError()

    def orientation():
        raise NotImplementedError()

    def damage():
        raise NotImplementedError()

    def collision_radius():
        raise NotImplementedError()

    def advance():
        raise NotImplementedError()

    @staticmethod
    def from_json(json):
        if json['variant'] == 'DefaultBullet':
            return DefaultBullet.from_json(json)
        else:
            raise IllegalVariantError(json['variant'])

    def to_json():
        raise NotImplementedError()

class DefaultBullet(Bullet):
    def __init__(
            self,
            uuid,
            damage = 1,
            orientation = Orientation(),
            orientation_delta = Orientation()):
        assert type(uuid) is int
        assert type(damage) is int
        assert isinstance(orientation, Orientation)
        assert isinstance(orientation_delta, Orientation)
        self.uuid = uuid
        self.damage = damage
        self.orientation = orientation
        self.orientation_delta = orientation_delta

    def collision_radius(self):
        return 1.0

    @staticmethod
    def from_json(json):
        return DefaultBullet(json['uuid'],
                             json['damage'],
                             Orientation.from_json(json['orientation']),
                             Orientation.from_json(json['orientation_delta']))

    def to_json(self):
        return {
            'variant': 'DefaultBullet',
            'uuid': self.uuid,
            'damage': self.damage,
            'orientation': self.orientation.to_json(),
            'orientation_delta': self.orientation_delta.to_json()
        }

    def advance(self, delta_time):
        assert type(delta_time) is float
        orientation = Phsyics.project(orientation = self.orientation,
                                      first_derivative = self.orientation_delta,
                                      delta_time = delta_time)
        return DefaultBullet(self.uuid,
                             self.damage,
                             orientation,
                             self.orientation_delta)

class Weapon(object):
    def __init__():
        raise NotImplementedError()

    def uuid():
        raise NotImplementedError()

    def ammo():
        raise NotImplementedError()

    def fire():
        raise NotImplementedError()

    @staticmethod
    def from_json(json):
        if json['variant'] == 'DefaultWeapon':
            return DefaultWeapon.from_json(json)
        else:
            raise IllegalVariantError(json['variant'])

    def to_json():
        raise NotImplementedError()

class DefaultWeapon(Weapon):
    def __init__(
            self,
            uuid,
            ammo = 0,
            damage = 0):
        assert type(uuid) is int
        assert type(ammo) is int
        assert type(damage) is int
        self.uuid = uuid
        self.ammo = ammo
        self.damage = damage

    @staticmethod
    def from_json(self):
        return DefaultWeapon(json['uuid'],
                             json['ammo'],
                             json['damage'])

    def to_json(self):
        return {
            'variant': 'DefaultWeapon',
            'uuid': self.uuid,
            'ammo': self.ammo,
            'damage': self.damage
        }

    def fire(self, orientation = Orientation()):
        assert isinstance(orientation, Orientation)
        assert self.ammo >= 1
        velocity_magnitude = Vector3(1, 0, 0)
        velocity_angle = orientation.angular().matrix3x3()
        velocity = velocity_angle * velocity_magnitude
        orientation_delta = Orientation(linear = velocity)
        bullet = DefaultBullet(uuid = Uuid.generate(),
                               orientation = orientation,
                               orientation_delta = orientation_delta)
        default_weapon = DefaultWeapon(uuid = self.uuid,
                                       ammo = self.ammo - 1,
                                       damage = self.damage)
        return (default_weapon, bullet)

class Turret(object):
    def __init__(
            self,
            uuid,
            orientation = Orientation(),
            weapon = DefaultWeapon(Uuid.generate())):
        assert type(uuid) is int
        assert isinstance(orientation, Orientation)
        assert isinstance(weapon, Weapon)
        self._uuid = uuid
        self._orientation = orientation
        self._weapon = weapon

    def uuid(self):
        return self._uuid
    def orientation(self):
        return self._orientation
    def weapon(self):
        return self._weapon

    @staticmethod
    def from_json(json):
        return Turret(json['uuid'],
                      Orientation.from_json(json['orientation']),
                      Weapon.from_json(json['weapon']))

    def to_json(self):
        return {
            'uuid': self._uuid,
            'orientation': self._orientation.to_json(),
            'weapon': self._weapon.to_json()
        }

class Tank(object):
    def __init__(
            self,
            uuid,
            orientation = Orientation(),
            turret = Turret(Uuid.generate()),
            health = 10,
            btmac = "",
            motorspeeds = 0
            ):
        assert type(uuid) is int
        assert isinstance(orientation, Orientation)
        assert isinstance(turret, Turret)
        assert type(health) is int
        self._uuid = uuid
        self._orientation = orientation
        self._turret = turret
        self._health = health
        self._btmac = btmac
        self._motorspeeds = motorspeeds

    def uuid(self):
        return self._uuid

    def btmac(self):
        return self._btmac

    def is_alive(self):
        return self._health > 0

    def turret(self):
        return self._turret

    def health(self):
        return self._health

    def orientation(self):
        return self._orientation

    def motorspeeds(self):
        return self._motorspeeds

    @staticmethod
    def from_json(json):
        return Tank(json['uuid'],
                    Orientation.from_json(json['orientation']),
                    Turret.from_json(json['turret']),
                    json['health'],
                    json['btmac'],
                    json['motorspeeds'])

    def to_json(self):
        return {
            'uuid': self._uuid,
            'orientation': self._orientation.to_json(),
            'turret': self._turret.to_json(),
            'health': self._health,
            'btmac': self._btmac,
            'motorspeeds': self._motorspeeds
        }

    def take_damage(self, damage = 0):
        assert type(damage) is int
        if damage >= self.health():
            return Tank(uuid = self.uuid(),
                        orientation = self.orientation(),
                        turret = self.turret(),
                        health = 0)
        else:
            return Tank(uuid = self.uuid(),
                        orientation = self.orientation(),
                        turret = self.turret(),
                        health = self.health() - damage)

    def collision_radius(self):
        return 1.0

class Player(object):
    def __init__(
            self,
            uuid,
            tank = Tank(Uuid.generate()),
            btmac = ""):
        assert type(uuid) is int
        assert isinstance(tank, Tank)
        self._uuid = uuid
        self._btmac = btmac
        self._tank = tank

    def btmac(self):
        return self._btmac

    def tank(self):
        return self._tank

    def uuid(self):
        return self._uuid

    @staticmethod
    def from_json(json):
        return Player(json['uuid'],
                      Tank.from_json(json['tank']),
                      json['btmac'])

    def to_json(self):
        return {
            'uuid': self._uuid,
            'tank': self._tank.to_json(),
            'btmac': self._btmac
        }

class Prefab(object):
    @staticmethod
    def from_json(json):
        """
        TODO: we do not yet have any prefabs
        """
        raise IllegalVariantError(json['variant'])

    def to_json():
        raise NotImplementedError()


class IllegalVariantError(Exception):
    def __init__(variant):
        self._variant = variant

    def variant(self):
        return self._variant

    def __str__(self):
        return repr(self._variant)

class Event(object):
    def __init__():
        raise NotImplementedError()

    def uuid():
        raise NotImplementedError()

    @staticmethod
    def from_json(json):
        if json['variant'] == 'PlayerJoinEvent':
            return PlayerJoinEvent.from_json(json)
        elif json['variant'] == 'PlayerFireEvent':
            return PlayerFireEvent.from_json(json)
        elif json['variant'] == 'GameStartEvent':
            return GameStartEvent.from_json(json)
        else:
            raise IllegalVariantError()

    def to_json():
        raise NotImplementedError()

class BluetoothEvent(Event):
    def __init__():
        raise NotImplementedError()

    def uuid():
        raise NotImplementedError()

    @staticmethod
    def from_json(json, btmac):
        if json['variant'] == 'BluetoothTankSelectEvent':
            return BluetoothSelectTankEvent.from_json(json, btmac)
        elif json['variant'] == 'BluetoothFireEvent':
            return BluetoothFireEvent.from_json(json, btmac)
        elif json['variant'] == 'BluetoothTankMoveEvent':
            return BluetoothTankMoveEvent.from_json(json, btmac)
        elif json['variant'] == 'BluetoothTurretMoveEvent':
            return BluetoothTurretMoveEvent.from_json(json, btmac)
        else:
            raise IllegalVariantError()

    def to_json():
        raise NotImplementedError()

class BluetoothSelectTankEvent(BluetoothEvent):
    def __init__(
            self,
            uuid,
            phone_btmac,
            tank_btmac):
        assert type(uuid) is int
        self._uuid = uuid
        self._tank_btmac = tank_btmac
        self._phone_btmac = phone_btmac

    def uuid(self):
        return self._uuid

    def phone_btmac(self):
        return self._phone_btmac

    def tank_btmac(self):
        return self._tank_btmac

    @staticmethod
    def from_json(json, phone_btmac):
        return BluetoothSelectTankEvent(
                Uuid.generate(),
                phone_btmac,
                json['tank_btmac'])

    def to_json(self):
        return {
                'variant': 'BluetoothSelectTankEvent',
                'tank_btmac': self._tank_btmac
        }

class BluetoothFireEvent(BluetoothEvent):
    def __init__(
            self,
            uuid,
            phone_btmac):
        assert type(uuid) is int
        self._uuid = uuid
        self._phone_btmac = phone_btmac

    def uuid(self):
        return self._uuid

    def phone_btmac(self):
        return self._phone_btmac

    @staticmethod
    def from_json(json, phone_btmac):
        return BluetoothFireEvent(
                Uuid.generate(),
                phone_btmac)

    def to_json(self):
        return {
                'variant': 'BluetoothFireEvent'
        }

class BluetoothTankMoveEvent(BluetoothEvent):
    def __init__(
            self,
            uuid,
            phone_btmac,
            motorspeeds):
        assert type(uuid) is int
        self._uuid = uuid
        self._phone_btmac = phone_btmac
        self._motorspeeds = motorspeeds

    def uuid(self):
        return self._uuid

    def phone_btmac(self):
        return self._phone_btmac

    def motorspeeds(self):
        return self._motorspeeds

    @staticmethod
    def from_json(json, phone_btmac):
            return BluetoothTankMoveEvent(
                    Uuid.generate(),
                    phone_btmac,
                    json['motorspeeds'])

    def to_json(self):
        return {
                'variant': 'BluetoothTankMoveEvent',
                'uuid': self._uuid,
                'motorspeeds': self._motorspeeds
        }

class BluetoothTurretMoveEvent(BluetoothEvent):
    def __init__(
            self,
            uuid,
            phone_btmac,
            angle):
        assert type(uuid) is int
        self._uuid = uuid
        self._phone_btmac = phone_btmac
        self._angle = angle

    def uuid(self):
        return self._uuid

    def phone_btmac(self):
        return self._phone_btmac

    def angle(self):
        return self._angle

    @staticmethod
    def from_json(json, phone_btmac):
            return BluetoothTurretMoveEvent(
                    Uuid.generate(),
                    phone_btmac,
                    json['angle'])

    def to_json(self):
        return {
                'variant': 'BluetoothTurretMoveEvent',
                'angle': self._angle
        }

class SendAvailableTanks(Event):
    def __init__(
            self,
            uuid,
            initial_btmacs
            ):
        self._uuid = uuid
        self._inital_btmacs = initial_btmacs

    def uuid(self):
        return self._uuid

    def initial_btmacs(self):
        return self._initial_btmacs

    @staticmethod
    def from_json(json):
        return SendAvailableTanks(
                json['uuid'],
                json['initial_btmacs']
                )

    def to_json(json):
        return {
                'variant': 'SendAvailableTanks',
                'uuid': self._uuid,
                'initial_btmacs': self._initial_btmacs
        }

class DirectionalKeyPushEvent(Event):
    def __init__(
            self,
            uuid,
            keycode):
        assert type(uuid) is int
        self._uuid = uuid
        self._keycode = keycode

    @staticmethod
    def from_json(json):
        return DirectionalKeyPushEvent(json['uuid'],
                                       json['keycode'])

    def uuid(self):
        return self._uuid

    def keycode(self):
        return self._keycode

    def to_json(self):
        return {
            'variant': 'DirectionalKeyPushEvent',
            'uuid': self._uuid,
            'keycode': self._keycode
        }

class FireKeyPushEvent(Event):
    def __init__(
            self,
            uuid):
        assert type(uuid) is int
        self._uuid = uuid
        self._keycode = keycode

    @staticmethod
    def from_json(json):
        return FireKeyPushEvent(json['uuid'])

    def uuid(self):
        return self._uuid

    def to_json(self):
        return {
            'variant': 'FireKeyPushEvent',
            'uuid': self._uuid
        }

class PlayerJoinEvent(Event):
    def __init__(
            self,
            uuid,
            player = Player(Uuid.generate())):
        assert type(uuid) is int
        assert isinstance(player, Player)
        self._uuid = uuid
        self._player = player

    def uuid(self):
        return self._uuid

    def player(self):
        return self._player

    @staticmethod
    def from_json(json):
        return PlayerJoinEvent(json['uuid'],
                               Player.from_json(json['player']))

    def to_json(self):
        return {
            'variant': 'PlayerJoinEvent',
            'uuid': self._uuid,
            'player': self._player
        }

class PlayerFireEvent(Event):
    def __init__(
            self,
            uuid,
            player_uuid = 0):
        assert type(uuid) is int
        assert type(player_uuid) is int
        self._uuid = uuid
        self._player_uuid = player_uuid

    @staticmethod
    def from_json(json):
        return PlayerFireEvent(json['uuid'],
                               json['player_uuid'])

    def to_json(self):
        return {
            'variant': 'PlayerFireEvent',
            'uuid': self._uuid,
            'player_uuid': self._player_uuid
        }

class GameStartEvent(Event):
    def __init__(
            self,
            uuid):
        assert type(uuid) is int
        self._uuid = uuid

    def uuid(self):
        return self._uuid

    @staticmethod
    def from_json(json):
        return GameStartEvent(json['uuid'])

    def to_json(self):
        return {
            'variant': 'GameStartEvent',
            'uuid': self._uuid
        }

class State(object):
    def __init__():
        raise NotImplementedError()

    @staticmethod
    def initial():
        return LobbyState(Uuid.generate())

    def uuid(self):
        raise NotImplementedError()

    def next(self, events, time, elapsed_time):
        raise NotImplementedError()

    def is_running(self):
        raise NotImplementedError()

    @staticmethod
    def from_json(json):
        if json['variant'] == 'LobbyState':
            return LobbyState.from_json(json)
        elif json['variant'] == 'QuitState':
            return QuitState.from_json(json)
        elif json['variant'] == 'ActiveMatchState':
            return ActiveMatchState.from_json(json)
        else:
            raise IllegalVariantError(json['variant'])

    def to_json(self):
        raise NotImplementedError()

class LobbyState(State):
    def __init__(
            self,
            uuid,
            players = {},
            is_running = True):
        assert type(uuid) is int
        assert type(players) is dict
        assert type(is_running) is bool
        self._uuid = uuid
        self._players = players
        self._is_running = is_running

    def uuid(self):
        return self._uuid

    def next(self, event, time, elapsed_time):
        if isinstance(event, PlayerJoinEvent):
            self._players.update({event.player().uuid() : event.player()})
            return LobbyState(self._uuid, self._players)
        if isinstance(event, BluetoothSelectTankEvent):
            for uuid,player in self._players.iteritems():
                if player.btmac() == event.phone_btmac():
                    # TODO ensure a tank is only owned by one person
                    # TODO send json to all phones with updated tanks information
                    # for testing purposes (REMOVE)
                    if True or player.tank().btmac() == "":
                        self._players[uuid] = Player(player.uuid(),
                                                     btmac = player.btmac(),
                                                     tank = Tank(player.tank().uuid(),
                                                     btmac = event.tank_btmac()))
            return LobbyState(self._uuid, self._players)
        if isinstance(event, GameStartEvent):
            return ActiveMatchState(self._uuid, self._players)
        else:
            raise NotImplementedError()
        return LobbyState(self._uuid, self._players)
    def is_running(self):
        return self._is_running

    @staticmethod
    def from_json(json):
        return LobbyState(json['uuid'],
                          DictionaryUtil.from_json(json['players'],
                                                   value_type = Player))

    def to_json(self):
        return {
            'variant': 'LobbyState',
            'uuid': self._uuid,
            'players': DictionaryUtil.to_json(self._players)
        }

class QuitState(State):
    def __init__(
            self,
            uuid):
        assert type(uuid) is int
        self._uuid = uuid

    def uuid(self):
        return self._uuid

    def next(self, events, time, elapsed_time):
        return QuitState()

    def is_running(self):
        return False

    @staticmethod
    def from_json(json):
        return QuitState(json['uuid'])

    def to_json(self):
        return {
            'variant': 'QuitState',
            'uuid': self._uuid
        }

class ActiveMatchState(State):
    def __init__(
            self,
            uuid,
            players = {},
            projectiles = {},
            prefabs = {}):
        assert type(uuid) is int
        for player in players.itervalues():
            assert type(player) is Player
        self._uuid = uuid
        self._players = players
        self._projectiles = projectiles
        self._prefabs = prefabs
######### FIX FOR FINAL, SIMPLY FOR TESTING
        self._is_running = True

    def is_running(self):
        return self._is_running

    def uuid(self):
        return self._uuid

    def player(self, uuid):
        return self._players[uuid]

    def projectile(self, uuid):
        return self._projectiles[uuid]

    def prefab(self, uuid):
        return self._prefabs[uuid]

    def bluetooth_info(self):
        bluetooth_data = {}
        for player_uuid,player in self._players.iteritems():
            tank = player.tank()
            if True or tank.motorspeeds() != 0:
                bluetooth_data[tank.btmac()] = tank.motorspeeds()
                new_player = Player(
                            uuid = player.uuid(),
                            tank = Tank(
                                tank.uuid(),
                                orientation = tank.orientation(),
                                turret = tank.turret(),
                                health = tank.health(),
                                btmac = tank.btmac(),
                                motorspeeds = 0
                                ),
                           btmac = player.btmac()
                           )
                self._players[player_uuid] = new_player
        return bluetooth_data, ActiveMatchState(
                                        self._uuid,
                                        self._players,
                                        self._projectiles,
                                        self._prefabs
                                        )

    @staticmethod
    def from_json(json):
        return ActiveMatchState(json['uuid'],
                                DictionaryUtil.from_json(json['players'],
                                                         value_type = Player),
                                DictionaryUtil.from_json(json['projectiles'],
                                                         value_type = Bullet),
                                DictionaryUtil.from_json(json['prefabs'],
                                                         value_type = Prefab))

    def to_json(self):
        return {
            'variant': 'ActiveMatchState',
            'uuid': self._uuid,
            'players': DictionaryUtil.to_json(self._players),
            'projectiles': DictionaryUtil.to_json(self._projectiles),
            'prefabs': DictionaryUtil.to_json(self._prefabs)
        }

    def next(self, event, time, delta_time):
        """
        move the projectiles
        detect collisions between tanks and projectiles
        perform those operations
        """
        print time, delta_time
        projectiles = ActiveMatchState.advance_projectiles(self._projectiles, delta_time)
        tanks = {}
        for player_uuid, player in self._players.iteritems():
            tank = player.tank()
            tanks[tank.uuid()] = tank
        collisions = ActiveMatchState.tank_projectile_collisions(tanks, projectiles)
        damaged_tanks = {}
        for tank_uuid, tank in tanks.iteritems():
            if tank_uuid in collisions.iterkeys():
                projectile_uuid = collisions[tank_uuid]
                projectile = projeciles[projectile_uuid]
                damaged_tanks[tank_uuid] = tank.take_damage(projectile.damage)
            else:
                damaged_tanks[tank_uuid] = tank
        remaining_players = {}
        for player_uuid, player in self._players.iteritems():
            player_tank = damaged_tanks[player.tank().uuid()]
            remaining_players[player_uuid] = Player(uuid = player.uuid(),
                                                    tank = player_tank,
                                                    btmac = player.btmac())
        remaining_projectiles = {}
        for projectile_uuid, projectile in projectiles.iteritems():
            if projectile_uuid not in collisions.values():
                remaining_projectiles[projectile_uuid] = projectile

        if isinstance(event, BluetoothFireEvent):
            for player_uuid, player in self._players.iteritems():
                if player.btmac() == event.phone_btmac():
                    turret         = player.tank().turret()
                    orientation    = turret.orientation()
                    weapon, bullet = turret.weapon().fire(orientation)
                    new_player = Player(
                                uuid = player.uuid(),
                                tank = Tank(
                                    uuid = tank.uuid(),
                                    orientation = tank.orientation(),
                                    turret = Turret(
                                        turret.uuid(),
                                        orientation = turret.orientation(),
                                        weapon = weapon
                                        ),
                                    health = tank.health(),
                                    btmac = tank.btmac(),
                                    motorspeeds = tank.motorspeeds()
                                    ),
                               btmac = player.btmac()
                               )
                    remaining_players[player_uuid] = new_player
        if isinstance(event, BluetoothTankMoveEvent):
            for player_uuid, player in self._players.iteritems():
                if player.btmac() == event.phone_btmac():
                    tank = player.tank()
                    turret = tank.turret()
                    new_player = Player(
                                uuid = player.uuid(),
                                tank = Tank(
                                    uuid = tank.uuid(),
                                    orientation = tank.orientation(),
                                    turret = turret,
                                    health = tank.health(),
                                    btmac = tank.btmac(),
                                    motorspeeds = event.motorspeeds()
                                    ),
                               btmac = player.btmac()
                               )
                    remaining_players[player_uuid] = new_player
        if isinstance(event, BluetoothTurretMoveEvent):
            for player_uuid, player in self._players.iteritems():
                if player.btmac() == event.phone_btmac():
                    # event.angle() will give the angle of the turret
                    # update turret angle for the given player
                    if remaining_players.has_key(player_uuid):
                        # a whole lot of shit just to change the orientation of
                        # the turret, probably a bug or two in here
                        tank = player.tank()
                        turret = tank.turret()
                        orientation = Orientation(
                                            linear = turret.orientation().linear(),
                                            angular = Quaternion.from_axis_angle(
                                                0.0,
                                                1.0,
                                                0.0,
                                                -event.angle()*math.pi / 180.0)
                                                )
                        new_player = Player(
                                uuid = player.uuid(),
                                tank = Tank(
                                    tank.uuid(),
                                    orientation = tank.orientation(),
                                    turret = Turret(
                                        uuid = turret.uuid(),
                                        orientation = orientation,
                                        weapon = turret.weapon()
                                        ),
                                    health = tank.health(),
                                    btmac = tank.btmac(),
                                    motorspeeds = tank.motorspeeds()
                                    ),
                               btmac = player.btmac()
                               )
                        remaining_players[player_uuid] = new_player

        return ActiveMatchState(uuid = self.uuid(),
                                players = remaining_players,
                                projectiles = remaining_projectiles,
                                prefabs = self._prefabs)

    @staticmethod
    def advance_projectiles(projectiles, delta_time):
        assert type(projectiles) is dict
        assert type(delta_time) is float
        result = {}
        for uuid, projectile in projectiles.iteritems():
            assert type(uuid) is int
            assert isinstance(projectile, Bullet)
            result[uuid] = projectile.advance(delta_time)
        return result

    @staticmethod
    def tank_projectile_collisions(tanks, projectiles):
        collisions = {}
        for tank_uuid, tank in tanks.iteritems():
            for projectile_uuid, projectile in projectiles.iteritems():
                tank_position = tank.orientation().linear()
                projectile_position = projectile.orientation().linear()
                collision_radius = tank.collision_radius() + \
                                   projectile.collision_radius()
                if Phsyics.entities_do_collide(tank_position,
                                               projectile_position,
                                               collision_radius):
                    collisions[tank_uuid] = projectile_uuid
        return collisions

def __main__():
    time_prev = time.clock()
    time_next = None
    state_prev = State.initial()
    state_next = None
    while state_prev.is_running():
        time_next = time.clock()
        #state_next = state_prev.next({}, time_prev, time_next - time_prev)
        state_prev = state_next
        time_prev = time_next
        print json.dumps(state_next.to_json(),
                         sort_keys = True,
                         indent = 4,
                         separators = (', ', ': '))
#__main__()
