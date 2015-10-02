import sys
import pygame

pygame.init()


class Gfx(object):
    """
    This class takes care of drawing the state of the search to a window using pygame
    """
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    GREY = 128, 128, 128

    NONOGRAM_COLORS = [WHITE, BLACK]

    def __init__(self, nonogram_problem, fps, width_height):
        self.ngp = nonogram_problem

        self.width, self.height = width_height
        self.ground_unit = min(self.height//self.ngp.y_size, self.width//self.ngp.x_size)
        self.size = self.width, self.height = self.ground_unit*self.ngp.x_size, self.ground_unit*self.ngp.y_size

        self.screen = pygame.display.set_mode(self.size)

        self.clock = pygame.time.Clock()  # used for limiting the fps, so one can see each step
        self.fps = fps

    def draw_cell(self, x_pos, y_pos, value):
        pygame.draw.rect(self.screen, self.NONOGRAM_COLORS[value],
                         (self.ground_unit*x_pos, self.ground_unit*y_pos, self.ground_unit, self.ground_unit))

    def draw_for_one_domain(self, var_name):
        orientation = var_name[0]
        coordinate = int(var_name[1:])

        bit_vector = list(self.ngp.domains[var_name])[0]

        if orientation == 'x':
            for i in range(len(bit_vector)):
                self.draw_cell(coordinate, i, bit_vector[i])
        else:
            for i in range(len(bit_vector)):
                self.draw_cell(i, coordinate, bit_vector[i])

    def draw_domains(self):
        for d in self.ngp.domains:
            if len(self.ngp.domains[d]) == 1:
                self.draw_for_one_domain(d)

    def draw(self, data_dict):
        self.ngp = data_dict['current']

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.fps /= 2  # halve the fps
                if event.key == pygame.K_UP:
                    self.fps *= 2  # double the fps
                    if self.fps > 256.0:
                        self.fps = 256.0

        self.clock.tick(self.fps)

        self.screen.fill(self.GREY)
        self.draw_domains()

        pygame.display.flip()
