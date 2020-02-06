import vlf
import vlf.engine as e
import math
import pymunk

FPS = 30
SIMUL_LEN = 10
TICKS = int(FPS*SIMUL_LEN)

field = e.Field()
robot = e.Robot()

field.add(robot)
field.step(1)
field.step(1)

#vis = vlf.visualise.Visualisator(fps=FPS)

def limit_velocity(body, gravity, damping, dt):
    vel = body.velocity.rotated(-body.angle)
    vel.x = 0
    body.velocity = vel.rotated(body.angle)

    body.angular_velocity *= 0.95
    body.velocity *= 0.95

    pymunk.Body.update_velocity(body, gravity, damping, dt)

robot.body.velocity_func = limit_velocity
robot.body.position = (400, 300)
x = field.space.shape_query(pymunk.Circle(None, 5))
sqi = x[0]
shape = sqi[0]
polyset = sqi[1]
print(polyset.normal)
print(polyset.points)

exit()
for i in range(TICKS):
    robot.simulate_motors(0.3, 1)
    field.step(1/FPS)
    vis.draw_space(field)
    vis.wait()

print("Finished")
input()
