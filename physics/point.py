from util.angle import Angle
from util.vector_2d import Vector2D
import math


class Point:
    def __init__(self, position):
        self.position = position
        self._distance_to_origin = position.magnitude()
        self._tangent_unit_vector = position.rotate(Angle(90)).unit()

    def total_velocity(self, translation_velocity, angular_velocity):
        rotation_velocity = self._calculate_velocity_from_rotation(
            angular_velocity)
        return translation_velocity.add(rotation_velocity)

    def _calculate_velocity_from_rotation(self, angular_velocity):

        if self.position.x != 0 or self.position.y != 0:

            magnitude = math.tan(math.radians(
                angular_velocity)) * self._distance_to_origin

            return self._tangent_unit_vector.scale(magnitude)
        else:
            # at origin - no rotation
            return Vector2D(0, 0)
