# Physics engine for virtual line follower
# Power by pymunk
import pymunk as pk
import math

def MEDIUM_MOTOR_TORQUE_RPM_CALC(rpm):
    """Torque in N.cm"""
    torque = (-0.06*rpm + 15)*0.7 #70% of power bcs 7.5 volts
    return max(torque, 0)

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
        # Distance -> cm
        # Mass -> kg
        case_width=7,
        case_height=11,
        case_mass=0.4,
        wheel_width=2,
        wheel_height=9,
        wheel_mass=0.125,
        wheel_distance_from_center=10,
        wheel_radius=9,
        torque_rpm_func=MEDIUM_MOTOR_TORQUE_RPM_CALC,
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
        self.torque_rpm_func = torque_rpm_func
        self.wheel_radius=wheel_radius

    @property
    def parts(self):
        """All objects thats need to be added into simulation to create a robot"""
        return self.left_wheel, self.right_wheel, self.case, self.body

    def simulate_motors(self, l_ts, r_ts):
        """l_ts, r_ts -> speed [-1..1] where 1 max power forward, 0 no power, -1 max power backward"""
        ls, rs = self._get_motor_speed()

        # Current rpm of motor, can be negative if motor turns backward
        l_rpm = ls / (self.wheel_radius*math.pi) * 60
        r_rpm = rs / (self.wheel_radius*math.pi) * 60

        # If we trying to brake with motor, then torque_rpm acts like we stalled motor
        # Idk propper calculation for motor braking, so ill go with this
        
        # If l_rpm and l_ts both >0 or <0
        # Else act like we stalled
        #print("rpm", l_rpm, r_rpm)
        if (l_rpm * l_ts) >= 0:
            l_torq = self.torque_rpm_func(abs(l_rpm))
        else:
            l_torq = self.torque_rpm_func(0)
            #never()
        l_torq = l_torq * self.wheel_radius * l_ts

        if (r_rpm * r_ts) >= 0:
            r_torq = self.torque_rpm_func(abs(r_rpm))
        else:
            r_torq = self.torque_rpm_func(0)
            #never()
        r_torq = r_torq * self.wheel_radius * r_ts
        #print("torq", l_torq, r_torq)

        self._apply_motor_force(l_torq, r_torq)

    def _get_motor_speed(self):
        lwp = (-self.wheel_distance_from_center, 0)
        rwp = (+self.wheel_distance_from_center, 0)

        #TODO unsure about this func, check me
        lw = self.body.velocity_at_local_point(lwp).rotated(-self.body.angle)
        rw = self.body.velocity_at_local_point(rwp).rotated(-self.body.angle)
        return lw.y, rw.y

    def _apply_motor_force(self, l, r):
        x = self.wheel_distance_from_center
        y = 0

        apply_point_l = (-x, y)
        apply_point_r = (+x, y)
        force_l = (0, l)
        force_r = (0, r)

        self.body.apply_force_at_local_point(force_l, apply_point_l)
        self.body.apply_force_at_local_point(force_r, apply_point_r)
