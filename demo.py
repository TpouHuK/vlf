from vlf import get_fitness, visualise
import checkpoints
from PIL import Image

class PD:
    def __init__(self, p, d, power):
        self.p = p
        self.d = d
        self.power = power
        self.last_error = 0

    def __call__(self, sensors):
        error = (sensors[0] + sensors[1]) - (sensors[2] + sensors[3])
        error = -error
        last_error = self.last_error

        error_correction = self.p*error + (error - last_error)*self.d
        self.last_error = error
        return (self.power - error_correction), (self.power + error_correction)

c = get_fitness.Course(checkpoints.ch_list)

field_image = Image.open("field.png")
field_image = field_image.resize((300, 160))
v = visualise.Visualisator()
v.set_image(field_image)

max_p = 0
max_d = 0
max_o = 0

max_score = 0

#score = c.check_fitness(PD(10/3, 4, 20), visualiser=v)
for power in range(1, 5):
    for p in range(1, 20):
        for d in range(0, 5, 2):
            score = c.check_fitness(PD(p/3, d, power*20))
            #score = c.check_fitness(PD(p/3, d, power*20), visualiser=v)
            if score > max_score:
                max_score = score
                max_p = p
                max_d = d
                max_o = power
                print()
                print("NEW MAXIMUM!", score)
                print("PDO:", p, d, power)
                print("====")
            else:
                print(".", end="", flush=True)
