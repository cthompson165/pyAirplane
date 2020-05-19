from util.angle import Angle
from util.vector_2d import Vector2D
from physics.state import State
from physics.force import Force
from physics.rigid_body import RigidBody
from aerodynamics.lift_curves.lifting_line_lift import LiftingLineLift
from aerodynamics.drag_curves.lifting_line_drag import LiftingLineDrag
from aerodynamics.surface import Surface
import math


class BoxKite(RigidBody):
    def __init__(self, length, width, cell_length, bridle_length, knot_length):
        state = State(Vector2D(-10, 1), Vector2D(0, 0), Angle(80), 0)

        mass = 0.005  # TODO
        mass_moment_of_inertia = mass * (length**2 + width**2) / 12

        RigidBody.__init__(self, mass, mass_moment_of_inertia, state)

        # put bridle point at 0, 0 with kite above it at 0 aoa
        cos_bridle_angle = (knot_length**2 + length**2
                            - (bridle_length - knot_length)**2) \
            / (2 * knot_length * length)

        self.bridle_angle = math.acos(cos_bridle_angle)

        # back bottom corner
        back_of_kite_x = -knot_length * math.cos(self.bridle_angle)
        back_of_kite_y = knot_length * math.sin(self.bridle_angle)

        self.kite_cg = Vector2D(
            back_of_kite_x + length / 2.0, back_of_kite_y + width / 2.0)

        # surface pos is the aerodynamic center of the surface
        # ac is 1/4 of chord from front of surface
        # TODO - move this calculation to surface?
        front_cell_cp = Vector2D(
            back_of_kite_x + length - cell_length / 4.0,
            self.kite_cg.y)

        back_cell_cp = Vector2D(
            back_of_kite_x + 3 * cell_length / 4.0,
            self.kite_cg.y)

        cell_span = self._cell_span(width)
        cell_area = self._cell_area(cell_span, cell_length)
        cell_aspect_ratio = self._cell_aspect_ratio(cell_span, cell_area)

        cell_lift_curve = LiftingLineLift(cell_aspect_ratio)
        cell_drag_curve = LiftingLineDrag(cell_aspect_ratio)

        self._surfaces = []
        self._surfaces.append(Surface("front", front_cell_cp,
                                      Angle(0), cell_area,
                                      cell_lift_curve, cell_drag_curve))
        self._surfaces.append(Surface("back", back_cell_cp,
                                      Angle(0), cell_area,
                                      cell_lift_curve, cell_drag_curve))

    def _cell_span(self, width):
        return 2 * width * math.cos(45)

    def _cell_area(self, span, cell_length):
        cell_area = cell_length * span
        return 2 * cell_area

    def _cell_aspect_ratio(self, span, area):
        return span**2 / area

    def calculate_local_forces(self, local_velocity, angular_velocity):
        local_forces = []
        for surface in self._surfaces:
            local_forces.extend(
                surface.calculate_forces(
                    local_velocity,
                    angular_velocity))
        return local_forces

    def calculate_global_forces(self, state):
        forces = []
        gravity = Force(Force.Source.gravity,
                        "gravity", self.kite_cg, self.weight())
        forces.append(gravity)
        return forces

    def convert_local_forces_to_global(self, state, local_forces):
        global_forces = []
        for local_force in local_forces:
            global_forces.append(local_force.rotate(state.theta))
        return global_forces

    def calculate_forces(self, state):

        wind_speed = Vector2D(3.2, 0)
        wind_state = State(
            state.pos, state.vel.add(wind_speed),
            state.theta, state.theta_vel)

        local_velocity = RigidBody.get_local_velocity(wind_state)
        angular_velocity = state.theta_vel

        local_forces = self.calculate_local_forces(
            local_velocity, angular_velocity)

        forces = self.convert_local_forces_to_global(state, local_forces)
        forces.extend(self.calculate_global_forces(state))

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
