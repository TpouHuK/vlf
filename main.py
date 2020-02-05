import vlf
import vlf.engine as e
import pymunk

FPS = 30

WF = 0.15

field = e.Field()
robot = e.Robot()

field.add(robot)
field.step(1)
field.step(1)

vis = vlf.visualise.Visualisator(fps=FPS)

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
    body.velocity = vel.rotated(body.angle)

    pymunk.Body.update_velocity(body, gravity, damping, dt)

robot.body.velocity_func = limit_velocity
robot.body.position = (400, 300)

for i in range(int(5*FPS)):
    if (i % FPS) == 0:
        print("SEC OF SIMUL:", i // FPS)
    if (i // FPS) < 1:
        robot.simulate_motors(1, -1)
    else:
        robot.simulate_motors(-1, 1)
    field.step(1/FPS)
    vis.draw_space(field)
    vis.wait()
print("Finished")
