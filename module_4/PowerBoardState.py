from copy import deepcopy
from module_4.PowerBoard import PowerBoard


class PowerBoardState(PowerBoard):
    """
    Represents a search node in a 2048 agent.

    Based on https://codemyroad.wordpress.com/2014/05/14/2048-ai-the-intelligent-bot/
    """

    # Weight matrix found through optimization search
    ORIGINAL_WEIGHT_MATRIX = ((0.135759,  0.121925,   0.102812,   0.099937),
                              (0.0997992, 0.0888405,  0.076711,   0.0724143),
                              (0.060654,  0.0562579,  0.037116,   0.0161889),
                              (0.0125498, 0.00992495, 0.00575871, 0.00335193))

    WEIGHT_MATRICES = [ORIGINAL_WEIGHT_MATRIX]  # Will contain the matrix rotated

    for i in range(3):
        temp = WEIGHT_MATRICES[i][::-1]
        WEIGHT_MATRICES.append(tuple(zip(*temp)))

    def __init__(self, recursion_depth):
        super(PowerBoardState, self).__init__((4, 4))
        self.recursion_depth = recursion_depth
        self.children = {}
        self.random_next_states = []

    def move_with_deep_copy(self, direction):
        """
        Makes a deep copy of this state and executes a move without placement of random tile.
        :param direction: u, d, l, or r
        :return:
        """
        new_board = deepcopy(self)
        new_board.move_pieces(direction)
        new_board.recursion_depth = self.recursion_depth - 1
        return new_board

    def list_of_boards_after_random_tile_spawns(self):
        """
        Generates a list containing all boards that can be generated after a random tile spawn
        along with each board’s probability
        :return: [(board, probability), ...]
        """
        open_spaces = self.get_empty_spaces()
        board_list = []
        for space in open_spaces:
            two_board = deepcopy(self)
            four_board = deepcopy(self)

            two_board.place_value_at_coordinate(2, space)
            four_board.place_value_at_coordinate(4, space)

            board_list.append((two_board, 1-self.FREQUENCY_OF_FOURS))
            board_list.append((four_board, self.FREQUENCY_OF_FOURS))

        return board_list

    def is_terminal(self):
        return self.is_game_over() or self.recursion_depth == 0

    def terminal_score(self):
        """
        Returns the score of the board if it is a terminal state.
        """
        scores = []
        for w in self.WEIGHT_MATRICES:
            scores.append(self.entrywise_product(w))

        return max(scores)

    def entrywise_product(self, other):
        """
        Calculates the entrywise product of this board state by the class’s weight matrices.
        :param other: A weight matrix.
        """
        accumulator = 0

        for j in range(len(other)):
            for i in range(len(other[0])):
                c = self.board[j][i]
                if c == self.ABSENCE:
                    continue
                accumulator += c * other[j][i]

        return accumulator

    def decision(self):
        directions = self.get_possible_move_directions()
        boards_after_move_in_direction = {}

        for d in directions:
            boards_after_move_in_direction[d] = self.move_with_deep_copy(d)

        direction_scores = {}

        for d in directions:
            direction_scores[d] = boards_after_move_in_direction[d].score()

        maximum = 0
        best_direction = None

        for d, score in direction_scores:
            if score > maximum:
                best_direction = d
                maximum = score

        return best_direction

    def score(self):
        accumulator = 0

        random_next_boards = self.list_of_boards_after_random_tile_spawns()

        for board, probability in random_next_boards:
            if board.is_terminal:
                accumulator += board.terminal_score() * probability
            else:
                boards_after_additional_move = []
                for d in board.get_possible_move_directions:
                    boards_after_additional_move.append(board.move_with_deep_copy(d))

                optimal_board_after_move = max(boards_after_additional_move, key=lambda x: x.score())

                accumulator += optimal_board_after_move*probability

        return accumulator
