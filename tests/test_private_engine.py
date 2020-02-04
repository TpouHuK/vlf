import vlf

def test_robot_motor():
    robot = vlf.engine.Robot()
    robot._apply_motor_force(10)
