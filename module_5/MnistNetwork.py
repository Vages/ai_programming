__author__ = 'eirikvageskar'

import ArtificialNeuralNetwork

Ann = ArtificialNeuralNetwork.ArtificialNeuralNetwork


class MnistNetwork(ArtificialNeuralNetwork.ArtificialNeuralNetwork):
    """
    Subclass of Artificial Neural Network class which implements some helper methods useful for the
    Mnist-classification task
    """

    def __init__(self, input_nodes_no, hidden_nodes_topology,
                 output_nodes_no, training_cases, test_cases, learning_rate=0.1):

        super(MnistNetwork, self).__init__(input_nodes_no, hidden_nodes_topology, output_nodes_no, training_cases,
                                           test_cases, learning_rate)

    def get_percentage_of_tests_wrong(self, test_set=None):
        """
        Returns the percentage of tests that give another output node than they should have done.
        """
        no_of_errors = 0

        if test_set is None:
            test_set = self.test_cases

        for input_v, output_v in test_set:
            network_output = self.output_for_input(input_v)
            if find_maximum_list_entry_index(network_output) != output_v.index(1):
                no_of_errors += 1

        return no_of_errors/len(test_set)

    def blind_test(self, feature_sets):
        """
        Implements the blind_test function required in the report
        """

        outputs = []

        for input_v in feature_sets:
            outputs.append(self.output_for_input(input_v))

        return outputs


def find_maximum_list_entry_index(number_list):
    """
    Finds the index of the item with the highest value in a list.

    :param number_list: A list of numbers or some other comparable.
    :return: The index of the maximum valued item.
    """

    return max(enumerate(number_list), key=lambda x: x[1])[0]



