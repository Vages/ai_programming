__author__ = 'eirikvageskar'

import ArtificialNeuralNetwork

Ann = ArtificialNeuralNetwork.ArtificialNeuralNetwork


class MnistNetwork(ArtificialNeuralNetwork.ArtificialNeuralNetwork):
    """
    Subclass of Artificial Neural Network class which implements some helper methods useful for the
    Mnist-classification task
    """
    @staticmethod
    def normalize_list(input_list):
        """
        Normalizes a list of numbers
        :param input_list:
        :return:
        """
        factor = max(input_list)
        return [entry/factor for entry in input_list]

    @staticmethod
    def convert_int_to_unary_list(integer, max_value=9):
        temp = [0]*(max_value+1)

        temp[integer] = 1

        return temp

    def __init__(self, input_nodes_no, hidden_nodes_topology, output_nodes_no, training_inputs=None,
                 training_outputs=None, test_inputs=None, test_outputs=None, learning_rate=0.1,
                 activation_function='sigmoid', error_function='binary_cross'):

        normalized_training_inputs = [MnistNetwork.normalize_list(l) for l in training_inputs]
        normalized_test_inputs = [MnistNetwork.normalize_list(l) for l in test_inputs]

        vectorized_training_outputs = [MnistNetwork.convert_int_to_unary_list(label) for label in training_outputs]
        vectorized_test_outputs = [MnistNetwork.convert_int_to_unary_list(label) for label in test_outputs]

        super(MnistNetwork, self).__init__(input_nodes_no, hidden_nodes_topology, output_nodes_no, normalized_training_inputs,
                                           vectorized_training_outputs, normalized_test_inputs, vectorized_test_outputs, learning_rate,
                                           activation_function, error_function)

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
            if self.find_maximum_list_entry_index(network_output) != output_v.index(1):
                no_of_errors += 1

        return no_of_errors/len(test_inputs)

    def blind_test(self, feature_sets):
        """
        Implements the blind_test function required in the report
        """

        outputs = []

        feature_sets = [MnistNetwork.normalize_list(fs) for fs in feature_sets]

        for input_v in feature_sets:
            outputs.append(self.output_for_input(input_v))

        numbers = []

        for o in outputs:
            numbers.append(self.find_maximum_list_entry_index(o))

        return numbers

    @staticmethod
    def find_maximum_list_entry_index(number_list):
        """
        Finds the index of the item with the highest value in a list.

        :param number_list: A list of numbers or some other comparable.
        :return: The index of the maximum valued item.
        """

        return max(enumerate(number_list), key=lambda x: x[1])[0]



