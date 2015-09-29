import sys, pygame

pygame.init()


class Gfx(object):
    """
    This class takes care of drawing the state of the search to a window using pygame
    """
    safe_zone = 10  # Used as a buffer around screen edges
    size = width, height = 960, 540

    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    GREY = 128, 128, 128

    # Colors taken from the Kids Toys color scheme at Adobe Color CC
    # https://color.adobe.com/Kids-Toys-color-theme-6954050/

    ADOBE_BLUE = 32, 89, 168
    ADOBE_GREEN = 161, 226, 0
    ADOBE_YELLOW = 255, 237, 81
    ADOBE_ORANGE = 255, 149, 2
    ADOBE_RED = 230, 13, 6
    ADOBE_PINK = 230, 22, 207

    # Put the colors in an array to get a mapping from number to color
    ADOBE_COLORS = [ADOBE_BLUE, ADOBE_GREEN, ADOBE_YELLOW, ADOBE_ORANGE, ADOBE_RED, ADOBE_PINK]

    def __init__(self, vertex_coloring_problem, fps, width_height):
        self.size = self.width, self.height = width_height
        self.vcp = vertex_coloring_problem

        self.x_min, self.x_max, self.y_min, self.y_max = self.vcp.x_min, self.vcp.x_max, self.vcp.y_min, self.vcp.y_max
        self.x_coordinate_span = self.x_max-self.x_min
        self.y_coordinate_span = self.y_max-self.y_min

        self.screen = pygame.display.set_mode(self.size)

        self.clock = pygame.time.Clock()  # used for limiting the fps, so one can see each step
        self.fps = fps

    def _get_screen_vertical_position(self, y_coordinate):
        return round((y_coordinate-self.y_min+self.safe_zone)*self.height/(self.y_coordinate_span+2*self.safe_zone))

    def _get_screen_horizontal_position(self, x_coordinate):
        return round((x_coordinate-self.x_min+self.safe_zone)*self.width/(self.x_coordinate_span+2*self.safe_zone))

    def convert_coordinate_to_screen_position(self, coordinate):
        x, y = coordinate
        return self._get_screen_horizontal_position(x), self._get_screen_vertical_position(y)

    def _draw_edge(self, edge):
        start_name, end_name = edge
        start, end = self.vcp.vertices[start_name], self.vcp.vertices[end_name]
        start, end = self.convert_coordinate_to_screen_position(start), self.convert_coordinate_to_screen_position(end)

        pygame.draw.line(self.screen, self.GREY, start, end, 5)

    def draw_edges(self):
        for edge in self.vcp.edges:
            self._draw_edge(edge)

    def draw_nodes(self):
        for var_name in self.vcp.domains:
            var_domain = self.vcp.domains[var_name]
            var_coordinate = self.vcp.vertices[var_name]

            if len(var_domain) == 1:
                color = self.ADOBE_COLORS[list(var_domain)[0]]
            else:
                color = self.BLACK

            var_screen_pos = self.convert_coordinate_to_screen_position(var_coordinate)

            pygame.draw.circle(self.screen, color, var_screen_pos, 10)

    def draw(self, data_dict):
        self.vcp = data_dict['current']

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

        self.screen.fill(self.WHITE)
        self.draw_edges()
        self.draw_nodes()

        pygame.display.flip()
