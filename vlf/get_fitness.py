import engine as e

import numpy as np
import pymunk
import vlf
from PIL import Image, ImageOps

import math
from itertools import accumulate

class Course:
    def __init__(self, checkpoints):

        field_image = Image.open("field.png")
        field_image = field_image.resize((300, 160))

        self.simulation_len = 10_000
        self.simulation_step = 0.01
        self.sample_field = vlf.sensors.SampleField(field_image)
        self.check_on_line = vlf.sensors.SampleField(field_image, r=7)
        self.checkpoint_range = 10**2 #10cm to reach checkpoint with center of robot
        self.checkpoints = checkpoints

        distances_between_checkpoints = [
                a.get_distance(b) for a, b in zip(checkpoints, checkpoints[1:])]
        distances_between_checkpoints.insert(0, 0)
        self.distances_until_checkpoint = list(accumulate(distances_between_checkpoints))
        self.track_distance = sum(distances_between_checkpoints)

    def check_fitness(self, rule_func, visualiser=None):
        field = e.Field()
        robot = e.Robot()
        field.add(robot)

        #TODO remove hardcoded
        robot.body.position = (20, 50)
        robot.body.angle = math.radians(-155)

        cur_checkpoint = 0
        for i in range(self.simulation_len):
            robot_position = robot.body.position
            # fix names please, too long var names....
            if robot_position.get_dist_sqrd(self.checkpoints[cur_checkpoint])< self.checkpoint_range:
                cur_checkpoint += 1
                progress = int(self.distances_until_checkpoint[cur_checkpoint]/self.track_distance*100)
                if progress == 100:
                    fitness = self.track_distance*(self.simulation_len/i)
                    break

            sensor_values = [self.sample_field.get_mean_from_point(pos)
                    for pos in robot.get_sensors_pos()]
            # If we left line
            if self.check_on_line.get_any_from_point(robot.body.position) == 0:
                fitness = (self.distances_until_checkpoint[cur_checkpoint+1]
                        -robot.body.position.get_distance(self.checkpoints[cur_checkpoint]))
                assert fitness < self.track_distance
                break

            l, r = rule_func(sensor_values)
            l = max(min(l, 100), -100)
            r = max(min(r, 100), -100)

            #if l < 0:
                #panic()
            #if r < 0:
                #panic()
            #print(l, r)

            robot.simulate_motors(l/100, r/100)
            field.step(self.simulation_step)
            if visualiser:
                visualiser.draw_space(field)
            if abs(robot.body.angle) > 50:
                fitness = (self.distances_until_checkpoint[cur_checkpoint+1]
                        -robot.body.position.get_distance(self.checkpoints[cur_checkpoint]))
                assert fitness < self.track_distance
                break
        else:
            fitness = (self.distances_until_checkpoint[cur_checkpoint+1]
                    -robot.body.position.get_distance(self.checkpoints[cur_checkpoint]))
            assert fitness < self.track_distance


        return fitness
