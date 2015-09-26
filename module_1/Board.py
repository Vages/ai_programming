from math import sqrt


class Board:
    """
    Contains a board that the algorithm can navigate.
    """
    def __init__(self, board_specification):
        """
        Constructs a board from specification.

        :param board_specification: On the tuple form given in the task.
        :return:
        """
        size_params = board_specification[0]
        self.x_size = size_params[0]
        self.y_size = size_params[1]

        self.board = []
        self.inaccessible_tiles = []

        for i in range(self.y_size):
            self.board.append([0]*self.x_size)

        for j in range(3, len(board_specification)):
            obstacle_spec = board_specification[j]

            x_start = obstacle_spec[0]
            y_start = obstacle_spec[1]
            x_size = obstacle_spec[2]
            y_size = obstacle_spec[3]

            for k in range(y_start, y_start+y_size):
                for l in range(x_start, x_start+x_size):
                    self.board[k][l] = 1
                    self.inaccessible_tiles.append((l, k))

    def get_board(self):
        return self.board

    def get_cell(self, cell):
        x, y = cell

        return self.board[y][x]

    @staticmethod
    def distance_between(a, b):
        """
        Euclidian distance between points a and b.

        :param a: Form (x, y)
        :param b: Form (x, y)
        :return:
        """
        a_x, a_y = a
        b_x, b_y = b

        return sqrt((b_x-a_x)**2+(b_y-a_y)**2)

    def get_neighbours(self, a):
        """
        Returns all squares that one can move to from this square, including diagonal neighbours.

        :param a: Coordinate of square, of form (x, y)
        :return: Unordered set of possible candidates.
        """
        if self.get_cell(a) == 1:  # There is no way to move out of an occupied cell
            return set()

        a_x, a_y = a

        neighboring_cells = (
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
        )

        candidates = set()

        for b in neighboring_cells:
            b_x, b_y = b

            c_x, c_y = a_x + b_x, a_y + b_y

            candidates.add((c_x, c_y))

        unsuited_candidates = set()

        for c in candidates:
            c_x, c_y = c

            if 0 <= c_x < self.x_size and 0 <= c_y < self.y_size and self.get_cell(c) != 1:
                continue

            unsuited_candidates.add(c)

        return candidates - unsuited_candidates
