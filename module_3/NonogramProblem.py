from module_2.CSProblem import CSProblem
from module_2.Constraint import Constraint

CSP = CSProblem


class NonogramProblem(CSP):
    """
    Subclass of the constraint satisfaction problem class of module 2 used for nonograms, a visual puzzle.
    """
    def __init__(self, spec):
        super(NonogramProblem, self).__init__()

        self.x_size, self.y_size = spec[0]  # Numbers of columns and rows respectively

        # Initialize the rows. This is done in reverse because the bottommost line is defined first in the format.
        # It is easier to work with a representation that defines the topmost row first.
        for i in range(self.y_size):
            row_name = 'y'+str(i)
            row_spec = spec[self.y_size-i]
            self.domains[row_name] = set(self.create_all_possible_combinations_from_line_spec(row_spec, self.x_size))

        # Initialize columns
        for i in range(self.x_size):
            col_name = 'x'+str(i)
            col_spec = spec[1+self.y_size+i]
            self.domains[col_name] = set(self.create_all_possible_combinations_from_line_spec(col_spec, self.y_size))

        # Initialize constraints
        # These specify that every cell on the board must have the same value in the column and the row domains.
        for j in range(self.x_size):
            for k in range(self.y_size):
                line_expression = 'x[' + str(k) + '] == y[' + str(j) + ']'
                line_constraint = Constraint(['x', 'y'], line_expression, ('x' + str(j), 'y' + str(k)))
                self.constraints.append(line_constraint)

        # The usual inialization and filtering
        self.initialize_queue()
        self.domain_filtering()

    def print_final_solution(self):
        """
        Prints final result as pure text. Letter B
        :return:
        """
        for i in range(self.y_size):
            row_name = 'y'+str(i)
            row = list(self.domains[row_name])[0]
            row_string = ''
            for val in row:
                if val:
                    row_string += 'B'
                else:
                    row_string += ' '

            print(row_string)


    @staticmethod
    def _fill_k_bits_in_array_from_position_i(array, k, i):
        """
        Helper method that helps when filling out the pieces
        :param array: an array of 0s and 1s.
        :param k: Number of bits to be filled.
        :param i: Position of first cell to be filled.
        :return:
        """
        array_copy = array[:]

        for j in range(k):
            array_copy[i+j] = 1

        return array_copy

    @staticmethod
    def _place_piece_in_every_possible_way(bit_vector, piece_size, first_legal_position):
        """
        Returns every possible way to place a piece of 1s into the bit vector, starting at
        or after first_legal_position.

        :param bit_vector: Bit vector. Should have all 0s after first_legal_position
        :param piece_size: Number of positions to be filled with 1s
        :param first_legal_position: First position which is legal to fill with a 1.
        :return: List of tuples of form (bit vector, first_legal_position)
        """
        legal_combinations = len(bit_vector)-first_legal_position-piece_size+1

        combinations = []

        if legal_combinations >= 1:
            for i in range(legal_combinations):
                filled_bit_vector_copy = NonogramProblem._fill_k_bits_in_array_from_position_i(bit_vector,
                                                                                               piece_size,
                                                                                               first_legal_position+i)

                combinations.append((filled_bit_vector_copy, first_legal_position+piece_size+i+1))

        return combinations

    @staticmethod
    def create_all_possible_combinations_from_line_spec(line_spec, line_length):
        """
        Takes line spec and line length and creates all possible bit vectors that can fulfill the requirements.

        :param line_spec: Line spec of form [x1, x2, ... , xj]
        :param line_length: Integer that specifies line length
        :return:
        """
        bit_vectors = [([0]*line_length, 0)]

        for num in line_spec:
            vectors_with_this_number = []
            for vector, first_pos in bit_vectors:
                vectors_with_this_number += NonogramProblem._place_piece_in_every_possible_way(vector, num, first_pos)

            bit_vectors = vectors_with_this_number

        to_be_returned = []

        for vector, first_pos in bit_vectors:
            to_be_returned.append(tuple(vector))

        return to_be_returned
