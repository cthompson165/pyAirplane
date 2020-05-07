class Surface:

    air_density = 0.30267

    def __init__(self, name, relative_pos, relative_degrees, area):

        self.name = name
        self.relative_pos = relative_pos  # relative to CG
        self.relative_degrees = relative_degrees
        self.area = area
        
        self.distance_to_cg = relative_pos.magnitude()

    def AoA(self, airplane_angle, velocity):
        absoluteAngle = airplane_angle.plusConstant(self.relative_degrees)

        velAngle = velocity.angle()
        return absoluteAngle.minus(velAngle)

    def calculate_lift(self, airplane_angle, velocity):

        # equation from
        # http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml
        CL =  self.calculate_lift_coefficient(airplane_angle, velocity)

        vel_mag = velocity.magnitude()
        lift = (Surface.air_density * vel_mag**2 * self.area * CL) / 2

        return lift

    def calculate_drag(self, airplane_angle, velocity):

        # equation from
        # https://wright.nasa.gov/airplane/drageq.html
        CD = self.calculate_drag_coefficient(airplane_angle, velocity)
        
        vel_mag = velocity.magnitude()
        drag = CD * self.area * (Surface.air_density * vel_mag**2) / 2

        return drag

    def calculate_lift_coefficient(self, airplane_angle, velocity):
        pass

    def calculate_drag_coefficient(self, airplane_angle, velocity):
        pass

