# nothing
import pygame
import pymunk.pygame_util
import pygame.color

class Visualisator:
    def __init__(self, width=800, height=600, fps=60):
        pygame.init()

        screen = pygame.display.set_mode((width,height)) 
        clock = pygame.time.Clock()

        self.clock = clock
        self.screen = screen
        self.draw_options = pymunk.pygame_util.DrawOptions(screen)
        self.fps = fps

    def wait(self):
        self.clock.tick(self.fps)

    def draw_space(self, field):
        self.screen.fill((255,255,255))
        field.space.debug_draw(self.draw_options)
        pygame.display.flip()
