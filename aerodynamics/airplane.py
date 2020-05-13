from util.vector_2d import Vector2D
from physics.force import Force
from physics.rigid_body import RigidBody


class Airplane(RigidBody):

    def __init__(self, initial_state, mass, mass_moment_of_inertia):
        RigidBody.__init__(self, mass,
                           mass_moment_of_inertia, initial_state)
        self.debug = False

    def apply_pitch_control(self, percent):
        raise NotImplementedError

    def set_throttle(self, percent):
        for engine in self.engines():
            engine.set_throttle(percent)

    def engines(self):
        raise NotImplementedError

    def surfaces(self):
        raise NotImplementedError

    def cg(self):
        return Vector2D(0, 0)

    def current_state(self):
        return self.state.copy()

    def pos(self):
        return self.state.pos

    def orientation(self):
        return self.state.theta

    def calculate_forces(self, state):

        forces = []

        for surface in self.surfaces():
            # TODO - get forces in local coordinates and translate in physics
            forces.extend(surface.calculate_forces(self.state))

        for engine in self.engines():
            thrust = engine.get_thrust()

            # TODO - make airplane operate in local coordinates and translate
            # in physics
            thrust.vector = thrust.vector.rotate(self.state.theta)
            print(thrust.vector)
            forces.append(thrust)

        forces.extend(self.get_force_fields())

        return forces

    def weight(self):
        return Vector2D(0, -9.8 * self.mass())

    def get_force_fields(self):
        ''' Using force fields as a name for things that apply to all particles in an object
            equally. So they work on the object's cg and are independent of the object's mass.
            So... pretty much gravity. But allow descendants to override for flexibility.'''

        force_fields = []
        gravity = Force(Force.Source.gravity,
                        "gravity", self.cg(), self.weight())
        force_fields.append(gravity)
