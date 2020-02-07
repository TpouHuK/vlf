import pygame
import pymunk.pygame_util
import pygame.color
pymunk.pygame_util.positive_y_is_up = False

class Visualisator:
    def __init__(self, width=300, height=160, fps=60):
        pygame.init()

        screen = pygame.display.set_mode((width,height)) 
        clock = pygame.time.Clock()

        self.clock = clock
        self.screen = screen
        self.draw_options = pymunk.pygame_util.DrawOptions(screen)
        self.fps = fps
        self.image = None

    def wait(self):
        self.clock.tick(self.fps)

    def set_image(self, image):
        raw_str = image.tobytes("raw", 'RGBA')
        pygame_surface = pygame.image.fromstring(raw_str, image.size, 'RGBA')
        self.image = pygame_surface

    def draw_space(self, field):
        self.screen.fill((255,255,255))
        if self.image:
            self.screen.blit(self.image, (0,0))
            field.space.debug_draw(self.draw_options)
        pygame.display.flip()
