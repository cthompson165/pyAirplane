from util.vector_2d import Vector2D
from util.angle import Angle
from physics.atmosphere import Atmosphere
from physics.state import State
import pymunk
import math


class Simulator:

    def __init__(self):
        self._rigid_bodies = []
        self.atmosphere = Atmosphere()
        self.space = pymunk.Space()

    def register(self, rigid_body):
        # TODO - make this a keyed collection and add deregister
        self._rigid_bodies.append(rigid_body)
        body = pymunk.Body(rigid_body.mass(), rigid_body.moment())
        body.position = rigid_body._state.pos.array()
        body.velocity = rigid_body._state.vel.array()
        poly = pymunk.Poly.create_box(body)
        rigid_body.body = body
        self.space.add(body, poly)

    def step(self, time):
        for rigid_body in self._rigid_bodies:
            body = rigid_body.body
            state = rigid_body._state
            state.wind_speed = self.atmosphere.wind_speed
            forces = rigid_body.calculate_forces(state, self.atmosphere)
            for force in forces:
                world_pos = force.pos.add(state.pos)
                body.apply_force_at_world_point(
                    force.vector.array(),
                    world_pos.array())

        self.space.step(time)

        for rigid_body in self._rigid_bodies:
            body = rigid_body.body
            rigid_body._state = State(
                Vector2D(body.position.x, body.position.y),
                Vector2D(body.velocity.x, body.velocity.y),
                Angle(math.degrees(body.angle)),
                body.angular_velocity)
