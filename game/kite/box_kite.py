from util.angle import Angle
from util.vector_2d import Vector2D
from physics.state import State
from physics.force import Force
from physics.rigid_body import RigidBody
from game.kite.cell import Cell
from game.kite.bridle import Bridle


class BoxKite(RigidBody):
    def __init__(self, string_length, length, width, cell_length,
                 bridle_length, knot_length):

        mass = self.calculate_mass(length, width, cell_length, cell_length)

        state = State(Vector2D(-string_length, 1),
                      Vector2D(0, 0), Angle(20), 0)

        self.string_length = string_length

        mass_moment_of_inertia = mass * (length**2 + width**2) / 12

        RigidBody.__init__(self, mass, mass_moment_of_inertia, state)

        # get positions relative to
        bottom_back = Vector2D(-length / 2.0, -width / 2.0)
        bridle = Bridle(bridle_length, knot_length, length)
        bridle_position = bottom_back.add(bridle.get_position())
        front_surface_position = Vector2D(bottom_back.x + length, 0)
        back_surface_position = Vector2D(bottom_back.x + cell_length, 0)

        # adjust all positions so bridle position is at 0
        # to make torque calculations easier
        self.front_cell = Cell(
            "front", front_surface_position.subtract(bridle_position),
            cell_length, width)

        self.back_cell = Cell(
            "back", back_surface_position.subtract(bridle_position),
            cell_length, width)

        self._surfaces = []
        self._surfaces.append(self.front_cell)
        self._surfaces.append(self.back_cell)

        self.kite_cg = Vector2D(0, 0).subtract(bridle_position)

    def calculate_local_forces(self, local_velocity, angular_velocity):
        local_forces = []
        for surface in self._surfaces:
            local_forces.extend(
                surface.calculate_forces(
                    local_velocity,
                    angular_velocity))
        return local_forces

    def calculate_mass(self, length, width, cell_length1, cell_length2):
        dowel_weight = .00216  # kg/m
        plastic_weight = .004752  # kg/m2

        cell_1_weight = cell_length1 * width * 4 * plastic_weight
        cell_2_weight = cell_length2 * width * 4 * plastic_weight
        stick_weight = dowel_weight * length * 4
        cross_piece_weight = dowel_weight * width * 4

        return cell_1_weight + cell_2_weight + \
            stick_weight + cross_piece_weight

    def calculate_global_forces(self, state):
        forces = []
        gravity = Force(Force.Source.gravity,
                        "gravity", self.kite_cg.rotate(state.theta),
                        self.weight())
        forces.append(gravity)
        return forces

    def convert_local_forces_to_global(self, state, local_forces):
        global_forces = []
        for local_force in local_forces:
            global_forces.append(local_force.rotate(state.theta))
        return global_forces

    def calculate_forces(self, state):

        wind_speed = Vector2D(5, 0)
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

        print("FORCES:")
        for force in forces:
            print("\t" + force.name + " " +
                  str(round(force.vector.magnitude(), 2)))

        print("Orientation: " + str(round(state.theta, 2)))
        print("Height: " + str(round(state.pos.y, 2)))

        return forces

    def weight(self):
        return Vector2D(0, self.mass() * -9.8)

    def sum_forces(self, forces):
        sum = Vector2D(0, 0)
        for force in forces:
            sum = sum.add(force.vector)
        return sum

    def calculate_string_force(self, state, other_forces_sum):
        alpha = 1
        beta = 1

        distance = state.pos.magnitude()
        if distance < (self.string_length - 1):
            # TODO - how small a number under string length
            # we can get away with. 1 is too big
            return Vector2D(0, 0)  # don't apply force
        else:
            N = state.pos.scale(1/distance)

            print("distance: " + str(round(distance)))

            N_dot_term = state.pos.dot(state.vel) / state.pos.dot(state.pos)
            N_dot = state.vel.subtract(state.pos.scale(N_dot_term))
            N_dot = N_dot.scale(1 / distance)

            N_dot_N = N.dot(N)

            C = distance - self.string_length
            C_dot = N.dot(state.vel)

            t1 = self.mass() * N_dot.dot(state.vel)
            t2 = N.dot(other_forces_sum)
            feedback_term = self.mass() * (alpha * C + beta * C_dot)

            scaling_constant = (-t1 - t2 - feedback_term) / N_dot_N

            return N.scale(scaling_constant)
