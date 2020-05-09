import math
from physics.force import Force
from util.vector_2d import Vector2D
from util.angle import Angle


class Surface:
    ''' A plane has multiple services that generate lift
    and drag forces'''

    air_density = 0.30267

    def __init__(self, name, relative_pos,
                 relative_degrees, area, lift_curve, drag_curve):

        self.name = name
        self.relative_pos = relative_pos  # relative to CG
        self.relative_degrees = relative_degrees
        self.area = area

        self.lift_curve = lift_curve
        self.drag_curve = drag_curve

        self.distance_to_cg = relative_pos.magnitude()

        self._tangent_unit_vector = self.relative_pos.rotate(Angle(90)).unit()

    def aoa(self, airplane_angle, velocity):
        absolute_angle = airplane_angle.plus_constant(self.relative_degrees)

        velAngle = velocity.angle()
        return absolute_angle.minus(velAngle)

    def calculate_forces(self, state):

        rotation_velocity = self.calculate_velocity_from_rotation(state)
        total_velocity = state.vel.add(rotation_velocity)
        velocity_magnitude = total_velocity.magnitude()

        aoa = self.aoa(state.theta, total_velocity)
        CL = self.lift_curve.calculate_lift_coefficient(aoa)
        CD = self.drag_curve.calculate_drag_coefficient(CL)

        lift_mag = self.calculate_lift(CL, velocity_magnitude)
        lift_dir = total_velocity.rotate(Angle(90)).unit()
        lift_force = lift_dir.scale(lift_mag)

        drag_mag = self.calculate_drag(CD, velocity_magnitude)
        drag_dir = total_velocity.reverse().unit()
        drag_force = drag_dir.scale(drag_mag)

        forces = []
        forces.append(Force(Force.Source.lift, "lift",
                            self.relative_pos, lift_force))
        forces.append(Force(Force.Source.drag, "drag",
                            self.relative_pos, drag_force))

        return forces

    def calculate_lift(self, CL, velocity_magnitude):
        return (Surface.air_density * velocity_magnitude**2 * self.area * CL) \
            / 2

    def calculate_drag(self, CD, velocity_magnitude):
        return CD * self.area * (Surface.air_density * velocity_magnitude**2) \
            / 2

    def calculate_velocity_from_rotation(self, state):

        if self.relative_pos.x != 0 or self.relative_pos.y != 0:

            magnitude = math.tan(math.radians(
                state.theta_vel)) * self.distance_to_cg

            return self._tangent_unit_vector.scale(magnitude)
        else:
            # at CG - no rotation
            return Vector2D(0, 0)
