from util.angle import Angle
from util.vector_2d import Vector2D
from physics.state import State
from physics.force import Force
from physics.rigid_body import RigidBody


class PointKite(RigidBody):
    def __init__(self):
        state = State(Vector2D(-10, 1), Vector2D(0, 0), Angle(40), 0)

        mass = 0.005  # TODO
        self.area = 2 * (.9 * .35 * .2)
        RigidBody.__init__(self, mass, mass, state)

    def calculate_lift(self, CL, velocity_magnitude):
        air_density = 0.30267
        return (air_density * velocity_magnitude**2 * self.area * CL) \
            / 2

    def calculate_drag(self, CD, velocity_magnitude):
        air_density = 0.30267
        return CD * self.area * (air_density * velocity_magnitude**2) \
            / 2

    def calculate_forces(self, state):
        velocity = Vector2D(state.vel.x + 3, state.vel.y)
        velocity_magnitude = velocity.magnitude()

        CL = 1
        lift_mag = self.calculate_lift(CL, velocity_magnitude)
        lift_dir = velocity.rotate(Angle(90)).unit()
        lift_force = lift_dir.scale(lift_mag)

        CD = .3
        drag_mag = self.calculate_drag(CD, velocity_magnitude)
        drag_dir = velocity.reverse().unit()
        drag_vector = drag_dir.scale(drag_mag)

        forces = []
        forces.append(Force(
            Force.Source.lift, "lift", Vector2D(0, 0), lift_force))
        forces.append(Force(
            Force.Source.drag, "drag", Vector2D(0, 0), drag_vector))
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

        distance = state.pos.magnitude()
        print("distance: " + str(round(distance, 2)))

        scaling_constant = (t1 - t2 - t3) / distance
        N = state.pos.scale(1 / distance)

        return N.scale(scaling_constant)
