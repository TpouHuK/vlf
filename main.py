import vlf
import vlf.engine as e
import math
import numpy as np
import pymunk
from PIL import Image, ImageOps


FPS = 100
SIMUL_LEN = 10
TICKS = int(FPS*SIMUL_LEN)*100
#TICKS = 1


field = e.Field()
robot = e.Robot()

field.add(robot)
field.step(1)
field.step(1)


vis = vlf.visualise.Visualisator(fps=FPS)

field_image = Image.open("field.png")
field_image = field_image.resize((300, 160))
vis.set_image(field_image)
sample_field = vlf.sensors.SampleField(field_image)

print()

def limit_velocity(body, gravity, damping, dt):
    vel = body.velocity.rotated(-body.angle)
    vel.x = 0
    body.velocity = vel.rotated(body.angle)

    body.angular_velocity *= 0.95
    body.velocity *= 0.95

    pymunk.Body.update_velocity(body, gravity, damping, dt)

robot.body.position = (20, 50)
#robot.body.position = (280, 140)
robot.body.angle = math.radians(-155)

for i in range(TICKS):
    field.step(0.01)
    robot.simulate_motors(0, 0)

    #print(robot.get_sensors_pos())
    sensor_values = [sample_field.get_mean_from_point(pos)
            for pos in robot.get_sensors_pos()]

    #print(sensor_values)
    #print("===")

    pid = (sensor_values[0]+sensor_values[1]) - (sensor_values[2]+sensor_values[3])
    pid = -pid
    if pid > 0.2:
        pid = 0.2
    if pid < -0.2:
        pid = -0.2
    robot.simulate_motors(0.1-pid, 0.1+pid)

    vis.draw_space(field)
    #vis.wait()

print("Finished")
input()
