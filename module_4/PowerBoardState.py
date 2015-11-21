from copy import deepcopy
import itertools
from module_4.PowerBoard import PowerBoard


class PowerBoardState(PowerBoard):
    """
    Represents a search node in a 2048 agent. The agent uses expectimax search.

    Based in part on https://codemyroad.wordpress.com/2014/05/14/2048-ai-the-intelligent-bot/
    """

    # Essential to the algorithm is a weighting matrix, the use of which will be explained now:

    # In order to win a game of 2048, it is important that the high valued pieces are kept out of the way.
    # This is because the larger pieces are the ones who are combined less frequently.
    # A large piece in the middle of the board will block opportunities to combine pieces of lower value.
    # By keeping the highest valued piece in a corner and the pieces of decreasing following it in a snake shape,
    # the game is played optimally:
    # The new pieces that appear will appear in the open area outside the end of the "snake",
    # and because the larger pieces are locked in the snake, it will be simple to combine a newly appearing piece
    # with a piece of equally low value at the end of the snake.

    # The matrix consists of such weighting values, ordered in a snake shape.
    # The weighting values are powers of some number r (radix)

    # Because all corners and snake shapes are equally optimal, it is important that we consider the matrix rotated
    # and transposed in all eight possible ways.

    r = 4  # Radix should be higher than 2, in order to encourage mergings of more important tiles

    ORIGINAL_WEIGHT_MATRIX = ((r ** 14, r ** 13, r ** 12, r ** 11),
                              (r ** 7, r ** 8, r ** 9, r ** 10),
                              (r ** 6, r ** 5, r ** 4, r ** 3),
                              (r ** (-1), r ** 0, r ** 1, r ** 2))

    WEIGHT_MATRICES = [ORIGINAL_WEIGHT_MATRIX]  # Will contain the matrix, rotated and transposed in all 8 ways

    # Create three copies of the matrix, each rotated 90 degrees from the last
    for i in range(3):
        temp = WEIGHT_MATRICES[i][::-1]
        WEIGHT_MATRICES.append(tuple(zip(*temp)))

    # Create a transposed copy of the matrix
    for i in range(4):
        transposed_matrix = tuple(zip(*(WEIGHT_MATRICES[i])))
        WEIGHT_MATRICES.append(transposed_matrix)

    # Make the matrices one dimensional for performance reasons
    for j in range(len(WEIGHT_MATRICES)):
        WEIGHT_MATRICES[j] = list(itertools.chain(*WEIGHT_MATRICES[j]))

    def __init__(self, recursion_depth):
        """
        Generates an empty PowerBoard and sets a recursion depth, which is a limit on the number of moves that can
        be made before returning a score.

        :param recursion_depth: The number of moves that can be made before an expectimax evaluation is forced.
        """

        super(PowerBoardState, self).__init__((4, 4))
        self.recursion_depth = recursion_depth

    @staticmethod
    def get_recursion_depth_roof(empty_tiles):
        """
        Is used to set the initial recursion depth based on the number of empty tiles on the board.
        "roof" is part of the function name because a move may yield a board with a considerably higher number of empty
        tiles, which may result in an unnecessarily high running time due to the large fan-out effect of a board with
        many empty tiles.

        :param empty_tiles: Number of empty tiles on the board.
        :return: Recursion depth
        """

        base = 1

        if empty_tiles < 6:
            return base + 1
        if empty_tiles < 3:
            return base + 2
        return base

    def move_with_deep_copy(self, direction):
        """
        Makes a deep copy of this state and executes a move without placement of random tile.

        :param direction: u, d, l, or r
        """

        new_board = deepcopy(self)
        new_board.move_pieces(direction)
        new_board.recursion_depth = min(self.recursion_depth - 1,
                                        PowerBoardState.get_recursion_depth_roof(len(new_board.get_empty_spaces()) - 1))
        return new_board

    def list_of_boards_after_random_tile_spawns(self):
        """
        Generates a list containing all boards that can be generated after a random tile spawn
        along with each board’s probability of being spawned.

        :return: [(board, probability), ...]
        """

        open_spaces = self.get_empty_spaces()
        board_list = []
        num_of_open_spaces = len(open_spaces)

        for space in open_spaces:
            two_board = deepcopy(self)
            two_board.place_value_at_coordinate(2, space)

            four_board = deepcopy(self)
            four_board.place_value_at_coordinate(4, space)

            board_list.append((four_board, self.FREQUENCY_OF_FOURS / num_of_open_spaces))

            board_list.append((two_board, (1 - self.FREQUENCY_OF_FOURS) / num_of_open_spaces))

        return board_list

    def is_terminal(self):
        """
        Tells if the state is terminal, i.e. that no more moves shall be executed on it.
        This happens when the board is in a game over state or the recursion depth has reached 0.
        """

        return self.is_game_over() or self.recursion_depth == 0

    def terminal_score(self):
        """
        Returns the score of the board if it is a terminal state. This is maximum result of an entrywise multiplication
        of the board with any of the weight matrices.
        """

        scores = []
        for w in self.WEIGHT_MATRICES:
            product = self.entrywise_product(w)
            open_space_bonus = len(self.get_empty_spaces())
            scores.append(product + open_space_bonus)

        return max(scores)

    def entrywise_product(self, other):
        """
        Calculates the entrywise product of this board state by the class’s weight matrices.
        An entrywise product is like a scalar product for two dimensions: The values of the same coordinate in two
        different, equally sized matrices are multiplied together. All of these products are added together.

        :param other: A weight matrix.
        """
        accumulator = 0

        for j in range(4):
            for i in range(4):
                c = self.get_value_at_coordinate((i, j))
                if c == self.ABSENCE:
                    continue
                accumulator += c * other[j * 4 + i]

        return accumulator

    def decision(self):
        """
        Makes a decision about what move seems optimal.

        :return: The optimal direction. u, d, l, or r
        """
        directions = self.get_possible_move_directions()
        boards_after_move_in_direction = {}

        if len(directions) == 1:  # Only one move possible; no evaluation needed
            return directions[0]

        for d in directions:
            boards_after_move_in_direction[d] = self.move_with_deep_copy(d)

        direction_scores = {}

        for d in directions:
            direction_scores[d] = boards_after_move_in_direction[d].expectimax_score()

        maximum = float('-inf')
        best_direction = None

        for d in direction_scores:
            score = direction_scores[d]
            if score > maximum:
                best_direction = d
                maximum = score

        return best_direction

    def expectimax_score(self):
        """
        A recursive score function, which could be said to perform an expectimax calculation.

        :return: The score of this state, given a random tile spawn
        """
        accumulator = 0

        random_next_boards = self.list_of_boards_after_random_tile_spawns()  # Spawn a random tile on the board

        for board, probability in random_next_boards:
            if board.is_terminal():
                # This node is either a game over state or we have reached the recursion depth
                s = board.terminal_score()
                accumulator += s * probability  # Score is multiplied by probability of this resulting from random spawn
            else:
                # Perform expectimax evaluations of all boards with random spawns
                boards_after_additional_move = []
                for d in board.get_possible_move_directions():
                    boards_after_additional_move.append(board.move_with_deep_copy(d))

                # Find the best board score and add it to the expected values
                max_score = float('-inf')

                for next_board in boards_after_additional_move:
                    next_board_score = next_board.expectimax_score()
                    if next_board_score > max_score:
                        max_score = next_board_score

                accumulator += max_score * probability

        return accumulator
