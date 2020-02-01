import vlf

def test_field_creation():
    field = vlf.engine.Field()
    assert field != None

def test_robot_creation():
    robot = vlf.engine.Robot()

def test_rect_creation():
    width, height = 10, 30
    c_x, c_y = 50, 90
    mass = 11455
    rect = vlf.engine.create_offcentered_box(width, height, (c_x, c_y), mass)
    assert rect.mass == mass
    assert rect.area == width*height
    assert rect.center_of_gravity.x == c_x
    assert rect.center_of_gravity.y == c_y
