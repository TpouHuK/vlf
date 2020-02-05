# Physics engine for virtual line follower
# Power by pymunk
import pymunk as pk

def MEDIUM_MOTOR_TORQUE_RPM_CALC(rpm)
    """Torque in N.cm"""
    torque = -0.6*rpm + 15
    return min(torque, 0)

def create_offcentered_box(body, width, height, center, mass=None):
    """Return `pymunk.Poly` rectangle with center at `center`"""
    half_width = width/2
    half_height = height/2
    cx, cy = center
    vertices = (
            (-half_width+cx, -half_height+cy), #left upper
            (-half_width+cx, +half_height+cy), #left bottom
            (+half_width+cx, +half_height+cy), #right bottom
            (+half_width+cx, -half_height+cy), #right upper
            )
    rect = pk.Poly(body, vertices)
    rect.mass = mass
    return rect

class Field():
    """Basic simulation unit.
        
    Pymunk space enchated.
    """

    def __init__(self):
        self.space = pk.Space()

    def add(self, addendum):
        if isinstance(addendum, Robot):
            self._add_robot(addendum)

    def _add_robot(self, robot):
        self.space.add(robot.parts)

    def step(self, dt):
        # DO NOT LEAVE THIS LIKE THIS ONE
        self.space.step(dt)
        

class Robot():
    def __init__(
        self,
        case_width=100,
        case_height=100,
        case_mass=0.5,
        wheel_width=50,
        wheel_height=50,
        wheel_mass=0.3,
        wheel_distance_from_center=100,
            ):

        self.case_width = case_width
        self.case_height = case_height
        self.case_mass = case_mass
        self.wheel_width = wheel_width
        self.wheel_height = wheel_height
        self.wheel_mass = wheel_mass
        self.wheel_distance_from_center = wheel_distance_from_center

        main_body = pk.Body(mass=0, moment=0, body_type=pk.Body.DYNAMIC)
        left_wheel = create_offcentered_box(
                main_body,
                wheel_width, wheel_height,
                (-wheel_distance_from_center, 0),
                wheel_mass)
        right_wheel = create_offcentered_box(
                main_body,
                wheel_width, wheel_height,
                (+wheel_distance_from_center, 0),
                wheel_mass)
        case = create_offcentered_box(
                main_body,
                case_width, case_height,
                (0, 0),
                case_mass)

        self.left_wheel = left_wheel
        self.right_wheel = right_wheel
        self.case = case
        self.body = main_body

    @property
    def parts(self):
        """All objects thats need to be added into simulation to create a robot"""
        return self.left_wheel, self.right_wheel, self.case, self.body

    def _get_motor_speed(self):
        lwp = (-robot.wheel_distance_from_center, 0)
        rwp = (+robot.wheel_distance_from_center, 0)

        lw = body.velocity_at_local_point(lwp).rotated(-body.angle)
        rw = body.velocity_at_local_point(rwp).rotated(-body.angle)
    return lw, rw

    def _apply_motor_force(self, l, r):
        x = self.wheel_distance_from_center
        y = 0

        apply_point_l = (-x, y)
        apply_point_r = (+x, y)
        force_l = (0, l)
        force_r = (0, r)

        self.body.apply_force_at_local_point(force_l, apply_point_l)
        self.body.apply_force_at_local_point(force_r, apply_point_r)
