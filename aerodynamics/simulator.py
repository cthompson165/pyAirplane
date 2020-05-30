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

        self._rigid_bodies.append(rigid_body)
        body = pymunk.Body(rigid_body.mass(), rigid_body.moment())
        body.position = rigid_body._state.pos.array()
        body.velocity = rigid_body._state.vel.array()
        poly = pymunk.Poly.create_box(body)
        rigid_body.body = body
        self.space.add(body, poly)

    @staticmethod
    def get_local_airspeed(state):
        return state.airspeed().rotate(state.theta.times_constant(-1))

    def step(self, time):
        for rigid_body in self._rigid_bodies:

            body = rigid_body.body
            state = rigid_body._state
            state.wind_speed = self.atmosphere.wind_speed

            local_airspeed = Simulator.get_local_airspeed(state)
            surface_forces = rigid_body.calculate_surface_forces(
                local_airspeed, state.theta_vel)

            if surface_forces is not None:
                for surface_force in surface_forces:
                    body.apply_force_at_local_point(
                        surface_force.vector.array(),
                        surface_force.pos.array())

            thrust_forces = rigid_body.calculate_thrust_forces()
            if thrust_forces is not None:
                for thrust_force in thrust_forces:
                    body.apply_force_at_local_point(
                        thrust_force.vector.array(),
                        thrust_force.pos.array())

            weight_force = rigid_body.calculate_weight_force(state)
            if weight_force is not None:
                body.apply_force_at_world_point(
                    weight_force.vector.array(),
                    weight_force.pos.array())

        self.space.step(time)

        for rigid_body in self._rigid_bodies:
            body = rigid_body.body
            rigid_body._state = State(
                Vector2D(body.position.x, body.position.y),
                Vector2D(body.velocity.x, body.velocity.y),
                Angle(math.degrees(body.angle)),
                body.angular_velocity)
