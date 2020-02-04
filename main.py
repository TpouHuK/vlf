import vlf
import vlf.engine as e

DT = 1

field = e.Field()
robot = e.Robot()

field.add(robot)
field.step(1)
field.step(1)

vis = vlf.visualise.Visualisator()
while True:
    vis.wait()
    robot._apply_motor_force(1)
    field.step(1)
    robot.body.angle -= 0.01
    vis.draw_space(field)

