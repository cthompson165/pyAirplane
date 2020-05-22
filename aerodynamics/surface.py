from physics.force import Force
from physics.point import Point
from util.angle import Angle


class Surface:
    ''' A plane has multiple services that generate lift
    and drag forces'''

    # the  density is of air at 12,192 meters
    # is approximately 0.30267 kg/m3
    air_density = 0.30267

    def __init__(self, name, relative_pos,
                 angle, area, lift_curve, drag_curve):

        self._point = Point(relative_pos)

        self.name = name
        self.angle = angle
        self.area = area

        self.lift_curve = lift_curve
        self.drag_curve = drag_curve

    def aoa(self, velocity):

        vel_angle = velocity.angle()
        return self.angle.minus(vel_angle)

    def calculate_forces(self, translation_velocity, angular_velocity):

        surface_velocity = self._point.total_velocity(
            translation_velocity,
            angular_velocity)

        velocity_magnitude = surface_velocity.magnitude()
        aoa = self.aoa(surface_velocity)

        forces = []

        CL = 0
        if self.lift_curve is not None:
            CL = self.lift_curve.calculate_lift_coefficient(aoa)
            lift_mag = self.calculate_lift(CL, velocity_magnitude)
            lift_dir = surface_velocity.rotate(Angle(90)).unit()
            lift_force = lift_dir.scale(lift_mag)
            forces.append(Force(Force.Source.lift, "lift",
                                self._point.position, lift_force))

        CD = 0
        if self.drag_curve is not None:
            CD = self.drag_curve.calculate_drag_coefficient(aoa, CL)
            drag_mag = self.calculate_drag(CD, velocity_magnitude)
            drag_dir = surface_velocity.reverse().unit()
            drag_vector = drag_dir.scale(drag_mag)
            drag_force = Force(Force.Source.drag, "drag",
                               self._point.position, drag_vector)
            forces.append(drag_force)

        return forces

    def calculate_lift(self, CL, velocity_magnitude):
        return (Surface.air_density * velocity_magnitude**2 * self.area * CL) \
            / 2

    def calculate_drag(self, CD, velocity_magnitude):
        return CD * self.area * (Surface.air_density * velocity_magnitude**2) \
            / 2
