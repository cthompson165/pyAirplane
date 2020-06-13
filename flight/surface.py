from flight.cp import CP
from flight.atmosphere import Atmosphere
from physics.force import Force
from physics.point import Point
from physics.angle import Angle
from physics.vector_2d import Vector2D


class Surface:
    ''' A plane has multiple services that generate lift
    and drag forces'''

    def __init__(self, name,
                 relative_pos=Vector2D(0, 0),
                 chord_length=0,
                 angle=Angle(0),
                 area=0,
                 lift_curve=None,
                 drag_curve=None,
                 atmosphere=Atmosphere()):

        self._point = Point(relative_pos)

        self.name = name
        self.angle = angle
        self.area = area
        self._atmosphere = atmosphere

        self.lift_curve = lift_curve
        self.drag_curve = drag_curve

        if lift_curve is not None:
            stall_angle = lift_curve.stall_angle()
        else:
            stall_angle = None

        self.cp = CP(relative_pos, chord_length, stall_angle)

        self.velocity = Vector2D(0, 0)
        self.current_cp = Vector2D(0, 0)

    def aoa(self, velocity):
        vel_angle = velocity.angle()
        return self.angle.minus(vel_angle)

    def calculate_forces(self, translation_velocity,
                         angular_velocity, altitude):

        surface_velocity = self._point.total_velocity(
            translation_velocity,
            angular_velocity)

        self.velocity = surface_velocity
        air_density = self._atmosphere.get_air_density(altitude)

        velocity_magnitude = surface_velocity.magnitude()
        aoa = self.aoa(surface_velocity)

        forces = []

        current_cp = self.cp.calculate(aoa)
        self.current_cp = current_cp

        CL = 0
        if self.lift_curve is not None:
            CL = self.lift_curve.calculate_lift_coefficient(aoa)
            lift_mag = self.calculate_lift(CL, velocity_magnitude, air_density)
            lift_dir = Surface.get_lift_unit(aoa, surface_velocity)
            lift_force = lift_dir.scale(lift_mag)
            forces.append(Force("lift", Force.LIFT,
                                current_cp, lift_force))

        CD = 0
        if self.drag_curve is not None:
            CD = self.drag_curve.calculate_drag_coefficient(aoa, CL)
            drag_mag = self.calculate_drag(
                CD, velocity_magnitude, air_density)
            drag_dir = surface_velocity.reverse().unit()
            drag_vector = drag_dir.scale(drag_mag)
            drag_force = Force("drag", Force.DRAG,
                               current_cp, drag_vector)
            forces.append(drag_force)

        return forces

    def get_lift_unit(aoa, surface_velocity):
        if abs(aoa.relative_degrees()) <= 90:
            return surface_velocity.rotate(Angle(90)).unit()
        else:
            # trailing edge is leading so velocity vector is reversed
            return surface_velocity.rotate(Angle(-90)).unit()

    def calculate_lift(self, CL, velocity_magnitude, air_density):
        return (air_density * velocity_magnitude**2 * self.area * CL) \
            / 2

    def calculate_drag(self, CD, velocity_magnitude, air_density):
        return CD * self.area * (air_density * velocity_magnitude**2) \
            / 2
