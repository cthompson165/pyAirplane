from util.vector_2d import Vector2D
from util.angle import Angle
from physics.atmosphere import Atmosphere
from physics.state import State
from physics.flying_object import FlyingObject
from physics.stationary_object import StationaryObject
import pymunk
import math


class Simulator:

    def __init__(self):
        self._flying_objects = {}
        self._stationary_objects = {}
        self._tethers = {}
        self._current_key = 0
        self.atmosphere = Atmosphere()
        self.space = pymunk.Space()
        self.preview_forces = []

    def register_flying_object(self, flying_object):

        body = pymunk.Body(flying_object.mass(), flying_object.moment())
        body.position = flying_object.position().array()
        body.velocity = flying_object.velocity().array()
        body.angle = flying_object.orientation().radians()

        poly = pymunk.Poly.create_box(body)
        flying_object.body = body
        self.space.add(body, poly)

        self._current_key += 1
        flying_object.key = self._current_key
        self._flying_objects[flying_object.key] = \
            _PhysicalObject(flying_object, body)

    def unregister(self, object):

        self.untether(object)

        if isinstance(object, FlyingObject):
            physical_object = self._flying_objects.pop(object.key)
            self.space.remove(physical_object.body)
        elif isinstance(object, StationaryObject):
            physical_object = self._stationary_objects.pop(object.key)
            self.space.remove(physical_object.body)

    def register_stationary_object(self, stationary_object, position):

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = position.array()
        self.space.add(body)

        self._current_key += 1
        stationary_object.key = self._current_key
        self._stationary_objects[stationary_object.key] = \
            _PhysicalObject(stationary_object, body)

    def tether(self, object1, object2, position1, position2, length):
        body1 = self._find_body(object1)
        body2 = self._find_body(object2)

        joint = pymunk.SlideJoint(body1, body2, position1.array(),
                                  position2.array(), 0, length)

        self.space.add(joint)

        tether = _Tether(object1, object2, joint)
        self._tethers[object1.key] = tether
        self._tethers[object2.key] = tether

    def untether(self, object1):
        if object1.key in self._tethers:
            tether = self._tethers[object1.key]
            self._tethers.pop(tether.object1.key)
            self._tethers.pop(tether.object2.key)
            self.space.remove(tether.joint)

    def _find_body(self, object):
        if object.key in self._flying_objects:
            return self._flying_objects[object.key].body
        elif object.key in self._stationary_objects:
            return self._stationary_objects[object.key].body
        else:
            raise LookupError()

    @staticmethod
    def get_local_airspeed(state):
        return state.airspeed().rotate(state.orientation.times_constant(-1))

    def add_forces(self):
        for physical_object in self._flying_objects.values():
            flying_object = physical_object.object
            body = physical_object.body

            state = flying_object._state

            local_airspeed = Simulator.get_local_airspeed(state)
            flying_object.calculate_surface_forces(
                local_airspeed, state.angular_velocity)

            flying_object.calculate_thrust_forces()
            flying_object.calculate_weight_force(state)

            for force in flying_object.local_forces():
                body.apply_force_at_local_point(
                    force.vector.array(),
                    force.position.array())

            for force in flying_object.global_forces():
                body.apply_force_at_world_point(
                    force.vector.array(),
                    force.position.array())

    def apply_forces(self, time):
        self.space.step(time)

        for physical_object in self._flying_objects.values():
            flying_object = physical_object.object
            body = physical_object.body

            previous_state = flying_object._state

            flying_object._state = State(
                Vector2D(body.position.x, body.position.y),
                Vector2D(body.velocity.x, body.velocity.y),
                Angle(math.degrees(body.angle)),
                math.degrees(body.angular_velocity),
                previous_state.atmosphere)

            flying_object.clear_forces()

    def step(self, time):
        self.add_forces()
        self.apply_forces(time)


class _PhysicalObject:
    def __init__(self, object, body):
        self.object = object
        self.body = body


class _Tether:
    def __init__(self, object1, object2, joint):
        self.object1 = object1
        self.object2 = object2
        self.joint = joint
