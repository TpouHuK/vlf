# Physics engine for virtual line follower
# Power by pymunk
import pymunk as pk

def create_offcentered_box(width, height, center, mass=None):
    """Return pymunk.Poly rectangle with center at center"""
    half_width = width/2
    half_height = height/2
    cx, cy = center
    vertices = (
            (-half_width+cx, -half_height+cy), #left upper
            (-half_width+cx, +half_height+cy), #left bottom
            (+half_width+cx, +half_height+cy), #right bottom
            (+half_width+cx, -half_height+cy), #right upper
            )
    rect = pk.Poly(None, vertices)
    rect.mass = mass
    return rect

class Field():
    """Basic simulation unit.
        
    Pymunk space enchated.
    """

    def __init__(self):
        self.space = pk.Space()

class Robot():
    """Robot class."""
    def __init__(
        self,
        case_width=0.05,
        case_height=0.08,
        case_mass=0.03,
        wheel_width=0.01,
        wheel_height=0.09,
        wheel_mass=0.01,
        wheel_distance_from_center=0.05,
            ):
        main_body = pk.Body(mass=0, moment=0, body_type=pk.Body.DYNAMIC)
        

        left_wheel = create_offcentered_box(
                wheel_width, wheel_height,
                (-wheel_distance_from_center, 0),
                wheel_mass)
        right_wheel = create_offcentered_box(
                wheel_width, wheel_height,
                (+wheel_distance_from_center, 0),
                wheel_mass)

        case = create_offcentered_box(
                case_width, case_height,
                (0, 0),
                case_mass)

        left_wheel.body = main_body
        right_wheel.body = main_body
        case.body = main_body

        self.left_wheel = left_wheel
        self.right_wheel = right_wheel
        self.case = case
        self.body = main_body
