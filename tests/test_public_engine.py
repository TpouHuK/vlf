import vlf

def test_field_creation():
    field = vlf.engine.Field()
    assert field != None

def test_robot_creation():
    robot = vlf.engine.Robot()

def test_robot_properties():
    robot = vlf.engine.Robot()
    assert len(robot.parts) != 0

def test_rect_creation():
    width, height = 10, 30
    c_x, c_y = 50, 90
    mass = 11455
    rect = vlf.engine.create_offcentered_box(None, width, height, (c_x, c_y), mass)
    assert rect.mass == mass
    assert rect.area == width*height
    assert rect.center_of_gravity.x == c_x
    assert rect.center_of_gravity.y == c_y

def test_robot_and_field():
    field = vlf.engine.Field()
    robot = vlf.engine.Robot()
    field.add(robot)

def test_movement():
    dt = 1
    trust = 10

    field = vlf.engine.Field()
    robot = vlf.engine.Robot()
    
    field.add(robot)
    robot._apply_motor_force(10, 10)

    first_pos = robot.body.position
    # First step sets velocity
    field.step(dt)
    second_pos = robot.body.position
    # Second step moves robot and actualy changes position
    field.step(dt)
    third_pos = robot.body.position

    assert first_pos == second_pos #This assert fails if apply_impulse used in motors
    assert first_pos != third_pos
