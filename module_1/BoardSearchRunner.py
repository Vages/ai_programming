import sys

import BestFirstSearch as Bfs
import Board as B

from tabulate import tabulate
from Graphics import Gfx

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
        self.start = self.board_specification[1]
        self.goal = self.board_specification[2]
        self.search_modes = search_modes
        self.results = dict()
        self.gfx = Gfx(self.board, 10, self.start, self.goal)


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
                                            mode=mode,
                                            gui_function=self.gfx.draw)

    def solution_cost(self, solution):
        accum = 0
        for i in range(1, len(solution)):
            accum += Board.distance_between(solution[i-1], solution[i])

        return accum

    def print_statistics_to_console(self):
        """
        Prints statistics about the three runs to console.
        :return:
        """
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
                               round(self.results[key]['solution_cost'], 2),
                               round(self.solution_cost(self.results[key]['solution']), 2)])

        print(tabulate(table_data, headers=['Search type', 'Total', 'Closed', 'Open', 'Passed', 'Cost', 'Calculated cost']))


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
    bsr.print_statistics_to_console()
