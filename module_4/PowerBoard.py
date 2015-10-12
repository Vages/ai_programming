from copy import deepcopy
import random


class PowerBoard:
    """
    Class representing a 2048 board. The reason for the name PowerBoard is that the pieces have values that are
    powers of 2. And the name also has a certain awesomeness to it.
    """

    ABSENCE = 0  # Value of a tile representing absence.
    FREQUENCY_OF_FOURS = 0.1  # How often fours spawn instead of twos

    def __init__(self, size):
        """
        Creates a 2048-board

        :param size: tuple (x-size, y-size)
        :return:
        """

        self.x_size, self.y_size = size
        self.board = []
        self.score = 0  # The points scored. The sum of the values of tiles resulting from combinations.
        self.tile_evaluation_sequence_dict = {}  # Used for memoization
        self.last_random_coordinate = (0, 0)

        for j in range(self.y_size):
            temp = []
            for i in range(self.x_size):
                temp.append(self.ABSENCE)

            self.board.append(temp)

    def get_board(self):
        return deepcopy(self.board)

    def get_value_at_coordinate(self, coordinate):
        """
        Returns value at a coordinate (x, y)
        """
        x, y = coordinate
        return self.board[y][x]

    def place_value_at_coordinate(self, piece, coordinate):
        x, y = coordinate
        self.board[y][x] = piece

    def move_pieces(self, direction):
        tile_sequences = self.get_tile_evaluation_sequence(direction)
        for seq in tile_sequences:
            defendant_counter = 0
            for i in range(1, len(seq)):
                defendant_coordinate = seq[defendant_counter]
                defendant_value = self.get_value_at_coordinate(defendant_coordinate)
                attacker_coordinate = seq[i]
                attacker_value = self.get_value_at_coordinate(attacker_coordinate)
                if attacker_value == self.ABSENCE:
                    continue

                if defendant_value == self.ABSENCE:
                    if attacker_value == self.ABSENCE:
                        continue
                    else:
                        self.place_value_at_coordinate(attacker_value, defendant_coordinate)
                        self.place_value_at_coordinate(self.ABSENCE, attacker_coordinate)
                else:
                    if defendant_value == attacker_value:
                        self.place_value_at_coordinate(2*attacker_value, defendant_coordinate)
                        self.score += 2*attacker_value
                        self.place_value_at_coordinate(self.ABSENCE, attacker_coordinate)
                        defendant_counter += 1
                    else:
                        defendant_counter += 1
                        if defendant_counter == i:
                            continue
                        defendant_coordinate = seq[defendant_counter]
                        self.place_value_at_coordinate(attacker_value, defendant_coordinate)
                        self.place_value_at_coordinate(self.ABSENCE, attacker_coordinate)

    def get_empty_spaces(self):
        """
        Returns coordinates of all empty spaces on the board.
        """
        empties = set()

        for j in range(self.y_size):
            for i in range(self.x_size):
                t = (i, j)
                if self.get_value_at_coordinate(t) == self.ABSENCE:
                    empties.add(t)

        return empties

    def add_random_tile(self):
        """
        Adds a tile at one of the open spaces, picked at random (uniform distribution).
        Value is either 2 or 4.
        """
        empties = self.get_empty_spaces()
        chosen_coordinate = random.sample(empties, 1)[0]

        value = 2
        if random.random() < self.FREQUENCY_OF_FOURS:
            value = 4

        self.last_random_coordinate = chosen_coordinate
        self.place_value_at_coordinate(value, chosen_coordinate)

    def move_and_add_random_tile(self, direction):
        """
        Executes a move in a direction if that is possible.
        :param direction: u, d, l, or r
        """
        if self.is_move_possible_in_direction(direction):
            self.move_pieces(direction)
            self.add_random_tile()
            self.print_to_console()

    def print_to_console(self):
        for line in self.board:
            print(line)

        print(self.score, '\n')

    def get_tile_evaluation_sequence(self, direction):
        """
        Gets the sequence of evaluation for the tiles given a move in a direction.
        :param direction: u, d, l, or r
        :return: a set of the sequences
        """
        if direction in self.tile_evaluation_sequence_dict:
            return self.tile_evaluation_sequence_dict[direction]
        else:
            sequences = set()
            if direction in ('l', 'r'):
                for j in range(self.y_size):
                    t_seq = []
                    for i in range(self.x_size):
                        t_seq.append((i, j))

                    if direction == 'r':
                        t_seq.reverse()

                    sequences.add(tuple(t_seq))
            else:
                for i in range(self.x_size):
                    t_seq = []
                    for j in range(self.y_size):
                        t_seq.append((i, j))

                    if direction == 'd':
                        t_seq.reverse()

                    sequences.add(tuple(t_seq))

            self.tile_evaluation_sequence_dict[direction] = sequences
            return sequences

    def is_move_possible_in_direction(self, direction):
        """
        Checks if it is possible to execute a move in the given direction.
        :param direction: u, d, l, or r
        """
        tile_sequences = self.get_tile_evaluation_sequence(direction)
        for seq in tile_sequences:
            values = []

            for item in seq:
                values.append(self.get_value_at_coordinate(item))

            if self.ABSENCE in values:
                start = values.index(self.ABSENCE) + 1
                for i in range(start, len(values)):
                    if values[i] != self.ABSENCE:
                        return True

            for i in range(len(values)-1):
                if values[i] != 0 and values[i] == values[i+1]:
                    return True

        return False