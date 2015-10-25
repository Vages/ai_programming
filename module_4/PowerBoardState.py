from copy import deepcopy
import itertools
from module_4.PowerBoard import PowerBoard


class PowerBoardState(PowerBoard):
    """
    Represents a search node in a 2048 agent.

    Based on https://codemyroad.wordpress.com/2014/05/14/2048-ai-the-intelligent-bot/
    """

    # Weight matrix found through optimization search
    ORIGINAL_WEIGHT_MATRIX = ((2**14, 2**13, 2**12, 2**11),
                              (2**7, 2**8, 2**9, 2**10),
                              (2**6, 2**5, 2**4, 2**3),
                              (2**(-1), 2**0, 2**1, 2**2))

    """ORIGINAL_WEIGHT_MATRIX = ((0.135759,  0.121925,   0.102812,   0.099937),
                              (0.0997992, 0.0888405,  0.076711,   0.0724143),
                              (0.060654,  0.0562579,  0.037116,   0.0161889),
                              (0.0125498, 0.00992495, 0.00575871, 0.00335193))"""

    WEIGHT_MATRICES = [ORIGINAL_WEIGHT_MATRIX]  # Will contain the matrix rotated
    NON_MONOTONIC_EVALUATION_SEQUENCES = PowerBoard.get_tile_evaluation_sequence('d').union(PowerBoard.get_tile_evaluation_sequence('r'))

    for i in range(3):
        temp = WEIGHT_MATRICES[i][::-1]
        WEIGHT_MATRICES.append(tuple(zip(*temp)))

    for i in range(4):
        transposed_matrix = tuple(zip(*(WEIGHT_MATRICES[i])))
        WEIGHT_MATRICES.append(transposed_matrix)

    for j in range(len(WEIGHT_MATRICES)):
        WEIGHT_MATRICES[j] = list(itertools.chain(*WEIGHT_MATRICES[j]))

    def __init__(self, recursion_depth):
        super(PowerBoardState, self).__init__((4, 4))
        self.recursion_depth = recursion_depth

    @staticmethod
    def get_recursion_depth_roof(empty_tiles):
        base = 2
        if empty_tiles < 5:
            return base+1
        return base

    def move_with_deep_copy(self, direction):
        """
        Makes a deep copy of this state and executes a move without placement of random tile.
        :param direction: u, d, l, or r
        :return:
        """
        new_board = deepcopy(self)
        new_board.move_pieces(direction)
        new_board.recursion_depth = min(self.recursion_depth - 1,
                                        PowerBoardState.get_recursion_depth_roof(len(new_board.get_empty_spaces())-1))
        return new_board

    def list_of_boards_after_random_tile_spawns(self):
        """
        Generates a list containing all boards that can be generated after a random tile spawn
        along with each board’s probability
        :return: [(board, probability), ...]
        """
        open_spaces = self.get_empty_spaces()
        board_list = []
        num_of_open_spaces = len(open_spaces)
        for space in open_spaces:
            two_board = deepcopy(self)
            two_board.place_value_at_coordinate(2, space)
            probability_of_two = 1

            if num_of_open_spaces < 5:
                probability_of_two = 1 - self.FREQUENCY_OF_FOURS
                four_board = deepcopy(self)
                four_board.place_value_at_coordinate(4, space)
                board_list.append((four_board, self.FREQUENCY_OF_FOURS))

            board_list.append((two_board, probability_of_two))

        return board_list

    def is_terminal(self):
        return self.is_game_over() or self.recursion_depth == 0

    def terminal_score(self):
        """
        Returns the score of the board if it is a terminal state.
        """
        scores = []
        for w in self.WEIGHT_MATRICES:
            product = self.entrywise_product(w)
            open_space_bonus = len(self.get_empty_spaces())
            scores.append(product+open_space_bonus)

        return max(scores)-self.get_non_monotonic_penalties()

    def entrywise_product(self, other):
        """
        Calculates the entrywise product of this board state by the class’s weight matrices.
        :param other: A weight matrix.
        """
        accumulator = 0

        for j in range(4):
            for i in range(4):
                c = self.get_value_at_coordinate((i, j))
                if c == self.ABSENCE:
                    continue
                accumulator += c * other[j*4+i]

        return accumulator

    def decision(self):
        directions = self.get_possible_move_directions()
        boards_after_move_in_direction = {}

        if len(directions) == 1:
            return directions[0]

        for d in directions:
            boards_after_move_in_direction[d] = self.move_with_deep_copy(d)

        direction_scores = {}

        for d in directions:
            direction_scores[d] = boards_after_move_in_direction[d].score()

        maximum = 0
        best_direction = None

        for d in direction_scores:
            score = direction_scores[d]
            if score > maximum:
                best_direction = d
                maximum = score

        return best_direction

    def score(self):
        accumulator = 0

        random_next_boards = self.list_of_boards_after_random_tile_spawns()

        for board, probability in random_next_boards:
            if board.is_terminal():
                s = board.terminal_score()
                accumulator += s * probability
            else:
                boards_after_additional_move = []
                for d in board.get_possible_move_directions():
                    boards_after_additional_move.append(board.move_with_deep_copy(d))

                optimal_board_after_move = max(boards_after_additional_move, key=lambda x: x.score())

                accumulator += optimal_board_after_move.score()*probability

        return accumulator

    def get_non_monotonic_penalties(self):

        accumulator = 0

        for seq in self.NON_MONOTONIC_EVALUATION_SEQUENCES:
            accumulator += self.non_monotonic_penalty(seq)

        return accumulator

    def non_monotonic_penalty(self, sequence):
        values = []

        for coordinate in sequence:
            values.append(self.get_value_at_coordinate(coordinate))

        greatest_value = max(values)

        sorted_values = sorted(values)
        reversed_sorted_values = reversed(sorted_values)

        if not (values == sorted_values or values == reversed_sorted_values):
            penalty = greatest_value*greatest_value
            return penalty

        return 0

    def largest_piece_not_in_corner_penalty(self):
        largest_piece = max(self.board)
        if self.get_value_at_coordinate((0, 0)) == largest_piece:
            return 0
        if self.get_value_at_coordinate((0, 3)) == largest_piece:
            return 0
        if self.get_value_at_coordinate((3, 0)) == largest_piece:
            return 0
        if self.get_value_at_coordinate((3, 3)) == largest_piece:
            return 0
        return largest_piece*largest_piece
