from math import ceil
import time
import datetime
from math import log
from module_4 import PowerBoard

pb = PowerBoard.PowerBoard

dt = datetime.datetime

__author__ = 'eirikvageskar'

import pickle
import os

from module_5 import ArtificialNeuralNetwork

Ann = ArtificialNeuralNetwork.ArtificialNeuralNetwork


class PowerBoardAnn(Ann):
    def __init__(self, input_nodes_no, hidden_nodes_topology, output_nodes_no, training_inputs=None,
                 training_outputs=None, test_inputs=None, test_outputs=None, learning_rate=0.1,
                 activation_function='sigmoid', error_function='binary_cross',
                 preprocessing_method=None):

        super(PowerBoardAnn, self).__init__(input_nodes_no, hidden_nodes_topology, output_nodes_no, training_inputs,
                                            training_outputs, test_inputs, test_outputs, learning_rate,
                                            activation_function, error_function)

        if preprocessing_method is None:
            preprocessing_method = PowerBoardAnn.flatten_lists_and_normalize

        self.preprocessing_method = preprocessing_method

    def read_pickle(self):
        board_values = []
        moves = []
        file_names = next(os.walk('./runs'))[2]
        for file_name in file_names:
            if file_name.startswith('run_') and file_name.endswith('.pickle'):
                arr = pickle.load(open('./runs/' + file_name, "rb"))  # [board_states, moves]

                processed_x_vectors = []
                for board_state in arr[0]:
                    processed_x = self.preprocessing_method(board_state)
                    processed_x_vectors.append(processed_x)
                board_values += processed_x_vectors
                moves += arr[1]
                print(file_name)

        split_point = ceil(len(board_values)*0.8)

        self.training_inputs, self.test_inputs = board_values[:split_point], board_values[split_point:]

        processed_moves = [PowerBoardAnn.convert_int_to_unary_list(x) for x in moves]
        self.training_outputs, self.test_outputs = processed_moves[:split_point], processed_moves[split_point:]

    def get_percentage_of_tests_wrong(self, test_inputs=None, test_outputs=None):
        """
        Returns the percentage of tests that give another output node than they should have done.
        """
        no_of_errors = 0

        if test_inputs is None:
            test_inputs = self.test_inputs

        if test_outputs is None:
            test_outputs = self.test_outputs

        for i in range(len(test_inputs)):
            input_v, output_v = test_inputs[i], test_outputs[i]
            network_output = self.output_for_input(input_v)
            if PowerBoardAnn.find_maximum_list_entry_index(network_output) != output_v.index(1):
                no_of_errors += 1

        return no_of_errors/len(test_inputs)

    def evaluate_one_board(self, input_vector):
        output = self.output_for_input(self.preprocessing_method(input_vector))

        pb_game = pb((4, 4))
        pb_game.board = self.flatten_lists(input_vector)
        dirs = pb_game.get_possible_move_directions()
        numeric_dirs = []
        for d in dirs:
            if d == 'u':
                numeric_dirs.append(0)
            elif d == 'r':
                numeric_dirs.append(1)
            elif d == 'd':
                numeric_dirs.append(2)
            elif d == 'l':
                numeric_dirs.append(3)

        enumerated_output = enumerate(output)

        sorted_enumerated_output = sorted(enumerated_output, key=lambda x: -x[1])

        for elem in sorted_enumerated_output:
            if elem[0] in numeric_dirs:
                return elem[0]

    @staticmethod
    def get_best_possible_move_from_output():

    @staticmethod
    def _number_of_merges_horizontally(board_2d):
        merges = 0

        for row in board_2d:
            already_merged_in_row = []
            for i in range(len(row)):
                if i in already_merged_in_row:
                    continue
                row_i = row[i]

                if row_i == 0:
                    continue
                for j in range(i+1, len(row)):
                    row_j = row[j]
                    if row_j == row_i:
                        merges += 1
                        already_merged_in_row.append(j)
                    elif row_j == 0:
                        continue
                    else:
                        break

        return merges/8

    @staticmethod
    def _number_of_merges_vertically(board_2d):
        return PowerBoardAnn._number_of_merges_horizontally(zip(*board_2d))  #Transposes the matrix

    @staticmethod
    def _open_spaces_in_each_row(board_2d):

        open_spaces = []

        for row in board_2d:
            accumulator = 0
            for space in row:
                if space == 0:
                    accumulator += 1

            open_spaces.append(accumulator/4)

        return open_spaces

    @staticmethod
    def _open_spaces_in_each_column(board_2d):
        return PowerBoardAnn._open_spaces_in_each_row(zip(*board_2d))

    @staticmethod
    def flatten_lists_and_normalize(x):
        #max_bonus = has_max_tile_in_corner(x)
        a = PowerBoardAnn.flatten_lists(x)

        mock_board = pb((4,4))
        mock_board.board = a
        dirs = mock_board.get_possible_move_directions()

        directions = []

        for c in ['u', 'r', 'd', 'l']:
            if c in dirs:
                directions.append(1)
            else:
                directions.append(0)

        b = a[:]

        for t in range(len(a)):
            if a[t] != 0:
                b[t] = log(a[t], 2)
        return PowerBoardAnn.normalize_list(b) \
               + [PowerBoardAnn._number_of_merges_horizontally(x),
                  PowerBoardAnn._number_of_merges_vertically(x)] \
               + PowerBoardAnn._open_spaces_in_each_row(x) + PowerBoardAnn._open_spaces_in_each_column(x) \
               + PowerBoardAnn.find_number_of_nodes_with_neighbours_of_equal_value(x) \
               + PowerBoardAnn.max_tile_present_in_corner(a) + directions

    @staticmethod
    def convert_int_to_unary_list(integer, max_value=3):
        temp = [0]*(max_value+1)

        temp[integer] = 1

        return temp

    @staticmethod
    def normalize_list(x):
        m = max(x)
        return [entry/m for entry in x]

    @staticmethod
    def flatten_lists(x):
        return [item for sublist in x for item in sublist]

    @staticmethod
    def find_maximum_list_entry_index(number_list):
        """
        Finds the index of the item with the highest value in a list.

        :param number_list: A list of numbers or some other comparable.
        :return: The index of the maximum valued item.
        """

        return max(enumerate(number_list), key=lambda x: x[1])[0]

    @staticmethod
    def find_number_of_nodes_with_neighbours_of_equal_value(two_d_list):

        neighbours_relative = ((-1, 0), (1, 0), (0, -1), (0, 1))

        nodes_neighbour_status = [0]*16

        for i in range(4):
            for j in range(4):
                inaccessible_neighbour_tiles = 0
                for r_i, r_j in neighbours_relative:
                    n_i, n_j = i+r_i, j+r_j

                    if 0 <= n_i < 4 and 0 <= n_j < 4:
                        if two_d_list[j][i] == two_d_list[n_i][n_j]:
                            nodes_neighbour_status[j*4+i] += 1
                    else:
                        inaccessible_neighbour_tiles += 1

                nodes_neighbour_status[j*4+i] /= (4-inaccessible_neighbour_tiles)

        return nodes_neighbour_status

    @staticmethod
    def max_tile_present_in_corner(one_d_list):
        m = max(one_d_list)

        corners = (0, 3, -1, -4)
        max_in_corners = [0]*5

        for c in range(len(corners)):
            if one_d_list[corners[c]] == m:
                max_in_corners[c] = 1

        if 1 in max_in_corners:
            max_in_corners[-1] = 1

        return max_in_corners

if __name__ == '__main__':
    hidden_layer_topology = [20, 20]
    error_function = 'binary_cross'
    pba = PowerBoardAnn(51, hidden_layer_topology, 4, error_function='binary_cross')
    pba.read_pickle()
    print(pba.get_percentage_of_tests_wrong())

    a = time.time()

    no_of_epochs = 40
    error_rates = pba.do_training(no_of_epochs)
    print("Error rates:", error_rates)
    percentage_wrong_on_test_set = pba.get_percentage_of_tests_wrong()
    print("Error rate on test_set:", pba.get_percentage_of_tests_wrong())
    percentage_wrong_on_training_set = \
        pba.get_percentage_of_tests_wrong(pba.training_inputs, pba.training_outputs)

    print("Error rate on training_set:", percentage_wrong_on_training_set)

    b = time.time()

    time_elapsed = round(b-a)
    print('Time elapsed during training and testing:', time_elapsed)

    with open("2048_log.txt", "a") as logfile:
        timestamp = dt.fromtimestamp(a)
        readable_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        logfile.write("\n\nTest started at " + readable_timestamp)
        logfile.write("\nTime elapsed: " + str(time_elapsed))
        logfile.write("\nHidden layer topology: " + str(hidden_layer_topology))
        logfile.write("\nError function: " + error_function)
        logfile.write("\nNumber of epochs: " + str(no_of_epochs))
        logfile.write("\nTraining error rates: " + str(list(enumerate(error_rates, 1))))
        logfile.write("\nPercentage wrong on test cases: " + str(percentage_wrong_on_test_set))
        logfile.write("\nPercentage wrong on training cases: " + str(percentage_wrong_on_training_set))
