from util.angle import Angle
from util.vector_2d import Vector2D
from physics.state import State
from physics.force import Force
from physics.rigid_body import RigidBody


class PointKite(RigidBody):
    def __init__(self):
        state = State(Vector2D(-20, 1), Vector2D(0, 0), Angle(80), 0)

        mass = 0.005  # TODO

        RigidBody.__init__(self, mass, mass, state)

    def calculate_forces(self, state):

        forces = []
        forces.append(Force(
            Force.Source.lift, "lift", Vector2D(0, 0), Vector2D(0, 1)))
        forces.append(Force(
            Force.Source.drag, "drag", Vector2D(0, 0), Vector2D(-1, 0)))
        forces.append(Force(
            Force.Source.gravity, "gravity", Vector2D(0, 0), self.weight()))

        force_sum = self.sum_forces(forces)

        string_force = self.calculate_string_force(state, force_sum)

        forces.append(Force(
             Force.Source.other, "String", Vector2D(0, 0), string_force))

        return forces

    def weight(self):
        return Vector2D(0, self.mass() * -9.8)

    def sum_forces(self, forces):
        # adding these all to CG. I think that's valid...
        sum = Vector2D(0, 0)
        for force in forces:
            sum = sum.add(force.vector)
        return sum

    def calculate_string_force(self, state, other_forces_sum):
        t1 = self.mass() * (state.pos.dot(state.vel))**2 \
            / state.pos.dot(state.pos)
        t2 = self.mass() * state.vel.dot(state.vel)
        t3 = state.pos.dot(other_forces_sum)

        scaling_constant = (t1 - t2 - t3) / state.pos.magnitude()
        N = state.pos.scale(1 / state.pos.magnitude())

        return N.scale(scaling_constant)
