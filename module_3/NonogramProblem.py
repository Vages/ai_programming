from module_2.CSProblem import CSProblem

CSP = CSProblem


class NonogramProblem(CSP):
    def __init__(self):
        super(NonogramProblem, self).__init__()

    @staticmethod
    def _fill_k_bits_in_array_from_position_i(array, k, i):
        array_copy = array[:]

        for j in range(k):
            array_copy[i+j] = 1

        return array_copy

    @staticmethod
    def _place_piece_in_every_possible_way(bit_vector, piece_size, first_legal_position):
        legal_combinations = len(bit_vector)-first_legal_position-piece_size+1

        combinations = []

        if legal_combinations >= 1:
            for i in range(legal_combinations):
                bit_vector_copy = bit_vector[:]
                filled_bit_vector_copy = NonogramProblem._fill_k_bits_in_array_from_position_i(bit_vector,
                                                                                               piece_size,
                                                                                               first_legal_position+i)

                combinations.append((filled_bit_vector_copy, first_legal_position+piece_size+i+1))

        return combinations

    @staticmethod
    def create_all_possible_combinations_from_line_spec(line_spec, line_length):
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
