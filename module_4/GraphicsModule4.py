from collections import defaultdict
from math import log
import pygame
from module_4.PowerBoard import PowerBoard

pygame.init()


class Gfx(object):
    """
    This class takes care of drawing the state of the search to a window using pygame
    """

    # This color scheme is taken directly from the official version
    BACKGROUND = "0xFAF8EF"
    BORDER = "0xBBADA0"
    TILE_COLORS = defaultdict(lambda: "0x3c3a32")
    TILE_COLORS.update({PowerBoard.ABSENCE: "0xCDC1B4",
                        2: "0xeee4da",
                        4: "0xede0c8",
                        8: "0xf2b179",
                        16: "0xf59563",
                        32: "0xf67c5f",
                        64: "0xf65e3b",
                        128: "0xedcf72",
                        256: "0xedcc61",
                        512: "0xedc850",
                        1024: "0xedc53f",
                        2048: "0xedc22e"})

    FONT_COLORS = defaultdict(lambda: "0xf9f6f2")
    FONT_COLORS.update({2: "0x776e65",
                        4: "0x776e65"})

    def __init__(self, power_board, fps, width_height):
        self.pb = power_board

        self.width, self.height = width_height
        self.ground_unit = min(self.height//(self.pb.y_size+2), self.width//(self.pb.x_size+2))
        self.width, self.height = self.ground_unit*(self.pb.x_size+2), self.ground_unit*(self.pb.y_size+2)
        self.size = self.width, self.height

        self.screen = pygame.display.set_mode(self.size)

        self.clock = pygame.time.Clock()  # used for limiting the fps, so one can see each step
        self.fps = fps

    def draw_cell(self, x_pos, y_pos, value):
        x_pix, y_pix = self.ground_unit*(x_pos+1),self.ground_unit*(y_pos+1)
        pygame.draw.rect(self.screen, self.hex_to_dec_tuple(self.TILE_COLORS[value]),
                         (x_pix, y_pix, self.ground_unit, self.ground_unit))
        if pygame.font and value != PowerBoard.ABSENCE:
            font_size = int(72/(log(len(str(value)), 20)+1))
            font = pygame.font.Font(None, font_size)
            text = font.render(str(value), 1, self.hex_to_dec_tuple(self.FONT_COLORS[value]))
            textpos = text.get_rect(centerx=x_pix+self.ground_unit/2, centery=y_pix+self.ground_unit/2)
            self.screen.blit(text, textpos)

    def draw(self):
        self.clock.tick(self.fps)

        self.screen.fill(self.hex_to_dec_tuple(self.BACKGROUND))
        self.draw_cells_for_values()
        self.draw_grid()

        pygame.display.flip()

    def draw_cells_for_values(self):
        for j in range(self.pb.y_size):
            for i in range(self.pb.x_size):
                self.draw_cell(i, j, self.pb.get_value_at_coordinate((i, j)))

    def draw_grid(self):
        pygame.draw.rect(self.screen, self.hex_to_dec_tuple(self.BORDER), (self.ground_unit, self.ground_unit,
                                                     self.pb.x_size*self.ground_unit, self.pb.y_size*self.ground_unit), 10)

        for i in range(self.pb.x_size):
            for j in range(self.pb.y_size):
                pygame.draw.rect(self.screen, self.hex_to_dec_tuple(self.BORDER),
                                 (self.ground_unit*(i+1), self.ground_unit*(j+1), self.ground_unit, self.ground_unit),
                                 10)

    @staticmethod
    def hex_to_dec_tuple(s):
        return int(s[2:4], 16), int(s[4:6], 16), int(s[6:8], 16), 0
