from util.vector_2d import Vector2D
from physics.force import Force


class Engine:

    def __init__(self, name, pos, angle, idle_thrust, max_thrust):
        self.pos = pos
        self.angle = angle
        self.idle_thrust = idle_thrust
        self.max_thrust = max_thrust
        self.name = name

        self._current_thrust = idle_thrust
        self._current_throttle = 0

        self._throttle_range = max_thrust - idle_thrust
        self._orientation_unit = Vector2D(1, 0).rotate(angle)

    def set_throttle(self, percent):

        if percent < 0 or percent > 100:
            raise ValueError()

        self._current_throttle = percent
        above_throttle = self._throttle_range * (percent / 100.0)
        self._current_thrust = self.idle_thrust + above_throttle

    def get_thrust(self):
        thrust = self._orientation_unit.scale(self._current_thrust)
        return Force(Force.Source.thrust, self.name, self.pos, thrust)
