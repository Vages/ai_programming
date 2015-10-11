from copy import deepcopy
import random


class PowerBoard:
    ABSENCE = 0
    FREQUENCY_OF_FOURS = 0.1

    def __init__(self, size):
        """
        Creates a 2048-board

        :param size: tuple (x-size, y-size)
        :return:
        """

        self.x_size, self.y_size = size
        self.board = []
        self.score = 0
        self.tile_evaluation_sequence_dict = {}

        for j in range(self.y_size):
            temp = []
            for i in range(self.x_size):
                temp.append(self.ABSENCE)

            self.board.append(temp)

    def get_board(self):
        return deepcopy(self.board)

    def get_value_at_coordinate(self, coordinate):
        x, y = coordinate
        return self.board[y][x]

    def place_piece_at_coordinate(self, piece, coordinate):
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
                        self.place_piece_at_coordinate(attacker_value, defendant_coordinate)
                        self.place_piece_at_coordinate(self.ABSENCE, attacker_coordinate)
                else:
                    if defendant_value == attacker_value:
                        self.place_piece_at_coordinate(2*attacker_value, defendant_coordinate)
                        self.score += 2*attacker_value
                        self.place_piece_at_coordinate(self.ABSENCE, attacker_coordinate)
                        defendant_counter += 1
                    else:
                        defendant_counter += 1
                        if defendant_counter == i:
                            continue
                        defendant_coordinate = seq[defendant_counter]
                        self.place_piece_at_coordinate(attacker_value, defendant_coordinate)
                        self.place_piece_at_coordinate(self.ABSENCE, attacker_coordinate)

    def _rotate_coordinate_for_direction(self, coordinate, direction):

        if direction == 'l':
            return coordinate

        x, y = coordinate

        if direction == 'r':
            n_x = self.x_size - 1 - x
            n_y = self.y_size - 1 - y

        elif direction == 'u':
            n_x = self.x_size - 1 - y
            n_y = x

        elif direction == 'd':
            n_x = y
            n_y = self.y_size - 1 - x

        return n_x, n_y

    def get_empty_spaces(self):
        empties = set()

        for j in range(self.y_size):
            for i in range(self.x_size):
                t = (i, j)
                if self.get_value_at_coordinate(t) == self.ABSENCE:
                    empties.add(t)

        return empties

    def add_random_tile(self):
        empties = self.get_empty_spaces()
        chosen_coordinate = random.sample(empties, 1)[0]

        value = 2
        if random.random() < self.FREQUENCY_OF_FOURS:
            value = 4

        self.place_piece_at_coordinate(value, chosen_coordinate)

    def move_and_add_random_tile(self, direction):
        if self.is_move_possible_in_direction(direction):
            self.move_pieces(direction)
            self.add_random_tile()
            self.print_to_console()

    def print_to_console(self):
        for line in self.board:
            print(line)

        print(self.score, '\n')

    def get_tile_evaluation_sequence(self, direction):
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
