import vlf
import vlf.engine as e
import math
import pymunk


FPS = 30
WF = 1000000
SIMUL_LEN = 1

field = e.Field()
robot = e.Robot()

field.add(robot)
field.step(1)
field.step(1)

vis = vlf.visualise.Visualisator(fps=FPS-20)

def limit_velocity(body, gravity, damping, dt):
    # omg what i have wroten
    lwp = (-robot.wheel_distance_from_center, 0)
    rwp = (+robot.wheel_distance_from_center, 0)

    lw = body.velocity_at_local_point(lwp).rotated(-body.angle)
    rw = body.velocity_at_local_point(rwp).rotated(-body.angle)
    print(math.degrees(lw.angle, rw.angle)
    print(lw, rw)

    #body.apply_force_at_local_point(lw*body.mass*dt, lwp)
    #body.apply_force_at_local_point(rw*body.mass*dt, rwp)

    print(math.degrees(body.angle))
    print(math.degrees(body.velocity.angle))
    
    a = math.degrees(body.angle)
    b = math.degrees(body.velocity.angle)

    vel = body.velocity.rotated(-body.angle)
    vel.x = 0
    body.velocity = vel.rotated(body.angle)

    pymunk.Body.update_velocity(body, gravity, damping, dt)

robot.body.velocity_func = limit_velocity
robot.body.position = (400, 300)
#robot.simulate_motors(2, -2)

for i in range(int(SIMUL_LEN*FPS)):
    robot.simulate_motors(1, 1)
    #robot.body.angle = math.radians(-i)
    if (i % FPS) == 0:
        pass
        #print("SEC OF SIMUL:", i // FPS)
    field.step(1/FPS)
    vis.draw_space(field)
    vis.wait()
print("Finished")
input()
