import sys, pygame

pygame.init()


class Gfx(object):
    """
    This class takes care of drawing the state of the search to a window using pygame
    """
    size = width, height = 960, 540
    WHITE = 255, 255, 255  # undiscovered tiles
    BLACK = 0, 0, 0  # closed tiles
    YELLOW = 255, 236, 193  # open tiles
    GREEN = 47, 160, 19  # goal
    GREY = 128, 128, 128  # barriers
    BLUE = 109, 142, 224  # start
    PINK = 255, 130, 234  # current node
    DARK_PINK = 178, 110, 149  # nodes backtracked from current node

    def __init__(self, board, fps, start, goal):
        self.board = board
        self.start = start
        self.goal = goal

        self.GU_X = self.width / float(board.x_size)
        self.GU_Y = self.height / float(board.y_size)

        self.screen = pygame.display.set_mode(self.size)

        self.clock = pygame.time.Clock()  # used for limiting the fps, so one can see each step
        self.fps = fps

    def flip_vertically(self, y):
        """
        We need to use this because in the specification, (0, 0) is the lower left corner
        and not the upper left corner, which is the default when drawing stuff in pygame
        :param y:
        """
        return self.board.y_size - 1 - y

    def draw_tile(self, x, y, color):
        rect = pygame.Rect(
            x * self.GU_X + 1,
            self.flip_vertically(y) * self.GU_Y + 1,
            self.GU_X - 2,
            self.GU_Y - 2
        )
        pygame.draw.rect(self.screen, color, rect)

    def draw_barriers(self):
        for tile in self.board.inaccessible_tiles:
            self.draw_tile(tile[0], tile[1], self.GREY)

    def draw_closed_list(self, closed_list):
        for tile in closed_list:
            x, y = tile
            self.draw_tile(x, y, self.BLACK)

    def draw_open_list(self, open_list):
        for tile in open_list:
            x, y = tile
            self.draw_tile(x, y, self.YELLOW)

    def draw_start(self):
        x, y = self.start
        self.draw_tile(x, y, self.BLUE)

    def draw_goal(self):
        x, y = self.goal
        self.draw_tile(x, y, self.GREEN)

    def draw_current_node(self, node):
        x, y = node
        self.draw_tile(x, y, self.PINK)

    def draw_ancestors(self, ancestors):
        for ancestor in ancestors:
            x, y = ancestor
            self.draw_tile(x, y, self.DARK_PINK)

    def draw(self, data_dict):
        current_node = data_dict['current']
        closed_list = data_dict['closed_set']
        open_list = data_dict['closed_set']
        ancestors = data_dict['solution']
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

        self.draw_barriers()
        self.draw_closed_list(closed_list)
        self.draw_open_list(open_list)
        self.draw_goal()
        self.draw_ancestors(ancestors)
        self.draw_current_node(current_node)
        self.draw_start()

        pygame.display.flip()