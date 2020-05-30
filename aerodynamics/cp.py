from util.vector_2d import Vector2D


class CP:
    def __init__(self, leading_edge_position, chord_length, stall_angle):
        self.leading_edge_position = leading_edge_position
        self.chord_length = chord_length
        self.stall_angle = stall_angle

        self.quarter_chord_length = chord_length / 4.0
        self._quarter_point = Vector2D(
            self.leading_edge_position.x - self.quarter_chord_length,
            self.leading_edge_position.y)  # TODO - account for wing angle?

        self._three_quarter_point = Vector2D(
            self.leading_edge_position.x - self.quarter_chord_length * 3,
            self.leading_edge_position.y)  # TODO - account for wing angle?

    def calculate(self, aoa):
        if self.chord_length < 0 or self.stall_angle is None:
            return self.leading_edge_position

        relative_degrees = aoa.relative_degrees()
        backward = False
        if relative_degrees > 90:
            backward = True
            from_0 = 180 - relative_degrees
        elif relative_degrees < -90:
            backward = True
            from_0 = 180 + relative_degrees
        elif relative_degrees < 0:
            from_0 = -relative_degrees
        else:
            from_0 = relative_degrees

        stall_degrees = self.stall_angle.degrees()
        if from_0 <= stall_degrees:
            if not backward:
                return self._quarter_point
            else:
                return self._three_quarter_point

        else:
            percent_to_90 = ((from_0 - stall_degrees)
                             / (90.0 - stall_degrees))

            y = self._quarter_point.y
            from_aero_center = self.quarter_chord_length * percent_to_90

            if not backward:
                x = self._quarter_point.x - from_aero_center
            else:
                x = self._three_quarter_point.x + from_aero_center

            return Vector2D(x, y)
