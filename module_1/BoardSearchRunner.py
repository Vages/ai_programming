import sys

import BestFirstSearch as Bfs
import Board as B
import pygame

from tabulate import tabulate

Board = B.Board


class BoardSearchRunner:
    def __init__(self, board_specification, search_modes):
        """
        Initialises its board.

        :param board_specification: The same format as required by Board class.
        :param search_modes: List of search modes to be used for solving.
        """
        self.board_specification = board_specification
        self.board = Board(board_specification)
        self.search_modes = search_modes
        self.results = dict()

    def run_search(self):
        """
        Runs search and puts result in self.results.
        """
        for mode in self.search_modes:
            self.results[mode] = Bfs.a_star(self.board_specification[1],
                                            self.board_specification[2],
                                            self.board.get_neighbours,
                                            Board.distance_between,
                                            Board.distance_between,
                                            mode=mode)

    @staticmethod
    def draw_centered_dot(surface, color, origin_tuple, cell_offset_tuple, cell_width, size):
        """
        Draws a dot in the center of a cell.
        """
        x_origin, y_origin = origin_tuple
        x_offset, y_offset = cell_offset_tuple

        pygame.draw.circle(surface, color,
                           (round(x_origin+x_offset*cell_width+cell_width/2),
                            round(y_origin+y_offset*cell_width+cell_width/2)),
                           size)

    @staticmethod
    def draw_centered_line(surface, color, origin_tuple, parent_tuple, child_tuple, cell_width, size):
        """
        Draws a line from one cell center to another.
        """
        x_origin, y_origin = origin_tuple
        p_x, p_y = parent_tuple
        c_x, c_y = child_tuple
        p_x, p_y = round(x_origin+p_x*cell_width+cell_width/2), round(y_origin+p_y*cell_width+cell_width/2)
        c_x, c_y = round(x_origin+c_x*cell_width+cell_width/2), round(y_origin+c_y*cell_width+cell_width/2)
        pygame.draw.line(surface, color, (p_x, p_y), (c_x, c_y), size)

    def draw_board_on_surface(self, surface, position_tuple, size_tuple, result):
        """
        Draws a board on a surface.
        :param surface: Pygame surface.
        :param position_tuple: The position of the origin of this board (x, y)
        :param size_tuple: (width, height)
        :param result: results from a search.
        """
        x_origin, y_origin = position_tuple
        width, height = size_tuple

        # Some colors
        white = (0xFF, 0xFF, 0xFF)
        grey = (0xD3, 0xD3, 0xD3)
        red = (0xFF, 0, 0)
        green = (0, 0xFF, 0)
        blue = (0, 0, 0xFF)
        black = (0, 0, 0)

        # The relative size of a result
        cell_width = int(min(height/self.board.y_size, width/self.board.x_size))

        # Draw open spaces and walls
        for i in range(self.board.y_size):
            for j in range(self.board.x_size):
                if self.board.get_cell((j, i)) == 1:
                    color = red
                else:
                    color = white
                pygame.draw.rect(surface, color, [x_origin+j*cell_width, y_origin+i*cell_width, cell_width, cell_width])

        # Draw paths corresponding to search tree.
        for child in result['came_from']:
            parent = result['came_from'][child]
            self.draw_centered_line(surface, grey, position_tuple, parent, child, cell_width, round(cell_width/16))

        # Draw dots in open spaces
        for i in range(self.board.y_size):
            for j in range(self.board.x_size):
                if self.board.get_cell((j, i)) == 0:
                    self.draw_centered_dot(surface, black, position_tuple, (j, i), cell_width, round(cell_width/16))

        # Mark nodes in closed set
        for node in result['closed_set']:
            self.draw_centered_dot(surface, green, position_tuple, node, cell_width, round(cell_width/8))

        # Mark nodes in open set
        for node in result['open_set']:
            self.draw_centered_dot(surface, blue, position_tuple, node, cell_width, round(cell_width/8))

        # Draw solution path
        pointlist = []
        for i in range(len(result['solution'])):
            x, y = result['solution'][i]
            pointlist.append((x_origin+x*cell_width+int(cell_width/2), y_origin+y*cell_width+int(cell_width/2)))

        pygame.draw.lines(surface, red, False, pointlist, int(cell_width/8))

    def draw_board_and_solution(self, width, height):
        """
        Prints some statistics and draws three boards, one for each solution
        :param width: Window width
        :param height: Window height
        """
        # Print statistics to console
        table_data = []

        for key in self.results:
            closed_nodes = len(self.results[key]['closed_set'])
            open_nodes = len(self.results[key]['open_set'])
            passed_nodes = self.results[key]['nodes_passed_over']
            total_nodes = passed_nodes+closed_nodes+open_nodes
            table_data.append([key,
                               total_nodes,
                               closed_nodes,
                               open_nodes,
                               passed_nodes,
                               round(self.results[key]['solution_cost'], 2)])

        print(tabulate(table_data, headers=['Search type', 'Total', 'Closed', 'Open', 'Passed', 'Cost']))

        # GUI stuff from here on
        cell_width = round(min(height/self.board.y_size, width/self.board.x_size))
        # Cut away superfluous space
        width, height = self.board.x_size*cell_width, self.board.y_size*cell_width
        size_of_one_board = (width/2, height/2)

        # Pygame stuff
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Search visualization")

        clock = pygame.time.Clock()

        self.draw_board_on_surface(screen, (0, 0), size_of_one_board, self.results["best_first"])
        self.draw_board_on_surface(screen, (width/2, 0), size_of_one_board, self.results["depth_first"])
        self.draw_board_on_surface(screen, (0, height/2), size_of_one_board, self.results["breadth_first"])

        pygame.draw.line(screen, (0, 0, 0), (0, height/2), (width, height/2), 2)
        pygame.draw.line(screen, (0, 0, 0), (width/2, 0), (width/2, height), 2)
        pygame.display.flip()

        # Loop until the user clicks the close button.
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            clock.tick(10)


if __name__ == '__main__':
    f = open(sys.argv[1])

    # Format input file
    spec_raw = f.readline().split(';')
    spec_final = []
    for i in range(len(spec_raw)):
        split_data = spec_raw[i].split()
        for j in range(len(split_data)):
            split_data[j] = int(split_data[j])

        spec_final.append(tuple(split_data))

    spec_final = tuple(spec_final)

    bsr = BoardSearchRunner(spec_final, ['best_first', 'depth_first', 'breadth_first'])
    bsr.run_search()
    bsr.draw_board_and_solution(1280, 1024)
