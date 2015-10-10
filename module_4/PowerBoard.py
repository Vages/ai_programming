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

        for j in range(self.y_size):
            temp = []
            for i in range(self.x_size):
                temp.append(self.ABSENCE)

            self.board.append(temp)

    def get_board(self):
        return deepcopy(self.board)

    def get_piece(self, coordinate):
        x, y = coordinate
        return self.board[y][x]

    def place_piece_at_coordinate(self, piece, coordinate):
        x, y = coordinate
        self.board[y][x] = piece

    def move_pieces(self, direction):

        if direction is 'l' or 'r':
            x, y = self.x_size, self.y_size
        else:
            x, y = self.y_size, self.x_size

        for j in range(y):
            attack_counter = 0

            for i in range(1, x):
                attack_coordinate = self._rotate_coordinate_for_direction((attack_counter, j), direction)
                examined_coordinate = self._rotate_coordinate_for_direction((i, j), direction)
                piece_to_be_moved = self.get_piece(examined_coordinate)
                piece_at_attack_field = self.get_piece(attack_coordinate)

                if piece_to_be_moved is self.ABSENCE:
                    continue

                if piece_at_attack_field is self.ABSENCE:
                    self.place_piece_at_coordinate(piece_to_be_moved, attack_coordinate)
                    self.place_piece_at_coordinate(self.ABSENCE, examined_coordinate)
                elif piece_at_attack_field == piece_to_be_moved:
                    self.place_piece_at_coordinate(2*piece_at_attack_field, attack_coordinate)
                    self.place_piece_at_coordinate(self.ABSENCE, examined_coordinate)
                    attack_counter += 1
                    self.score += 2*piece_at_attack_field
                else:
                    attack_counter += 1
                    attack_coordinate = self._rotate_coordinate_for_direction((attack_counter, j), direction)
                    self.place_piece_at_coordinate(piece_to_be_moved, attack_coordinate)
                    self.place_piece_at_coordinate(self.ABSENCE, examined_coordinate)

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
                if self.get_piece(t) == self.ABSENCE:
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
        self.move_pieces(direction)
        self.add_random_tile()
