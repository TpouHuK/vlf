import vlf
import vlf.engine as e
import pymunk

WF = 0.15

field = e.Field()
robot = e.Robot()

field.add(robot)
field.step(1)
field.step(1)

vis = vlf.visualise.Visualisator()

def limit_velocity(body, gravity, damping, dt):
    # omg what i have wroten
    lwp = (-robot.wheel_distance_from_center, 0)
    rwp = (+robot.wheel_distance_from_center, 0)

    lw = body.velocity_at_local_point(lwp).rotated(-body.angle)
    rw = body.velocity_at_local_point(rwp).rotated(-body.angle)

    if rw.length != 0:
        rw.length = min(rw.length, WF)
    if lw.length != 0:
        lw.length = min(lw.length, WF)

    body.apply_impulse_at_local_point(lw*body.mass*-1, lwp)
    body.apply_impulse_at_local_point(rw*body.mass*-1, rwp)

    vel = body.velocity.rotated(-body.angle)
    vel.x = 0
    print(vel)
    body.velocity = vel.rotated(body.angle)

    pymunk.Body.update_velocity(body, gravity, damping, dt)

robot.body.velocity_func = limit_velocity
robot.body.position = (400, 300)

for i in range(1000):
    vis.wait()
    robot._apply_motor_force(0.6, 0.5)
    field.step(1)
    vis.draw_space(field)
