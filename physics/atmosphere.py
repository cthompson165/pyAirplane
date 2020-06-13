from physics.vector_2d import Vector2D


class Atmosphere:
    def __init__(self):
        self.wind_speed = Vector2D(0, 0)

        # from
        # https://www.engineeringtoolbox.com/standard-atmosphere-d_604.html
        # (except 13000 which is from nasa exercises
        # saying air at 12,192 meters is approximately
        # 0.30267 kg/m3)
        self.air_density = {-1000: 1.347,
                            0: 1.225,
                            1000: 1.112,
                            2000: 1.007,
                            3000: 0.9093,
                            4000: 0.8194,
                            5000: 0.7364,
                            6000: 0.6601,
                            7000: 0.59,
                            8000: 0.5258,
                            9000: 0.4671,
                            10000: 0.4135,
                            11000: 0.30267,  # from nasa boeing exercise
                            15000: 0.1948,
                            20000: 0.08891,
                            25000: 0.04008,
                            30000: 0.01841,
                            40000: 0.003996,
                            50000: 0.001027,
                            60000: 0.0003097,
                            70000: 0.00008283,
                            80000: 0.00001846}

    def get_air_density(self, altitude):
        last_density = 1.347
        for reference_altitude, density in self.air_density.items():
            if altitude < reference_altitude:
                return last_density
            else:
                last_density = density

        return last_density
