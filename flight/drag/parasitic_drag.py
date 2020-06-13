class ParasiticDrag:

    def __init__(self, drag_coefficient):
        self._cd = drag_coefficient

    def calculate_drag_coefficient(self, aoa, CL):
        return self._cd

    class _ShapeCoefficients():
        # TODO - there's a big range for sphere, might want more
        # sub types (smooth, rough, dimpled, etc...)
        BULLET = .295
        SPHERE = 0.47
        PLATE = 1.28
