# AM I USING GIT TO CONTROL FILE VERSION? NOOO
import vlf
import vlf.engine as e
import math
import numpy as np
import pymunk
import checkpoints
from PIL import Image, ImageOps


FPS = 100
SIMUL_LEN = 10
#TICKS = int(FPS*SIMUL_LEN)*100
TICKS = 10000


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


def limit_velocity(body, gravity, damping, dt):
    vel = body.velocity.rotated(-body.angle)
    vel.x = 0
    body.velocity = vel.rotated(body.angle)

    body.angular_velocity *= 0.95
    body.velocity *= 0.95

    pymunk.Body.update_velocity(body, gravity, damping, dt)

robot.body.position = (20, 50)
robot.body.angle = math.radians(-155)

cur_checkpoint = 0
for i in range(TICKS):

    if robot.body.position.get_dist_sqrd(checkpoints.ch_list[cur_checkpoint]) < 10**2:
        cur_checkpoint = (cur_checkpoint + 1) % len(checkpoints.ch_list)
        prog = int(checkpoints.distances_acc[cur_checkpoint]/checkpoints.full_dist*100)
        print("PROGRESS:", prog, "%")
        #if prog == 100:
            #print("FINISHED")
            #break

    field.step(0.01)
    sensor_values = [sample_field.get_mean_from_point(pos)
            for pos in robot.get_sensors_pos()]

    pid = (sensor_values[0]+sensor_values[1]) - (sensor_values[2]+sensor_values[3])
    pid = -pid
    if pid > 0.5:
        pid = 0.5
    if pid < -0.5:
        pid = -0.5
    robot.simulate_motors(0.5-pid, 0.5+pid)

    #vis.draw_space(field)
    #vis.wait()

print("Finished")
#input()
