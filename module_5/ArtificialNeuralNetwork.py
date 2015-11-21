__author__ = 'eirikvageskar'

import theano
import theano.tensor as T
import theano.tensor.nnet as Tann
import numpy as np

class ArtificialNeuralNetwork:
    def __init__(self, input_nodes_no, hidden_nodes_topology, output_nodes_no, training_cases, test_cases, learning_rate=0.1):
        self.learning_rate = learning_rate
        self.trainer = None
        self.test_cases = test_cases
        self.training_cases = training_cases
        self.build_artificial_neural_network(input_nodes_no, hidden_nodes_topology, output_nodes_no)

    def build_artificial_neural_network(self, no_of_input_nodes, hidden_nodes_topology, output_nodes_no):
        network_topology = [no_of_input_nodes] + hidden_nodes_topology + [output_nodes_no]

        weights = []
        biases = []

        for i in range(len(network_topology) - 1):
            weights.append(theano.shared(np.random.uniform(-.1, .1, size=(network_topology[i], network_topology[i+1]))))

        input_vector = T.dvector('input')
        expected_output_vector = T.dvector('expected_output')

        for i in range(1, len(network_topology)):
            biases.append(theano.shared(np.random.uniform(-.1, .1, size=network_topology[i])))

        outputs = [Tann.sigmoid(T.dot(input_vector, weights[0]) + biases[0])]

        for i in range(1, len(network_topology)-1):
            print(i)
            outputs.append(Tann.sigmoid(T.dot(outputs[i-1], weights[i]) + biases[i]))

        error = T.sum((expected_output_vector - outputs[-1])**2)

        params = []

        for i in range(len(network_topology) - 1):
            params.append(weights[i])
            params.append(biases[i])

        gradients = T.grad(error, params)
        back_propagation_activations = [(p, p-self.learning_rate*g) for p, g in zip(params, gradients)]

        self.trainer = theano.function([input_vector, expected_output_vector], error, updates=back_propagation_activations)
        self.predictor = theano.function([input_vector], outputs[-1])

    def output_for_input(self, input_vector):
        """
        Returns the neural network’s output for this input.

        :param input_vector: Some valid input vector
        :return: The network’s output
        """

        return self.predictor(input_vector)

    def train_for_one_example(self, input_vector, expected_output_vector):
        """
        Trains the network using one input-output example pair.

        :param input_vector: The example input.
        :param expected_output_vector: The example output.
        :return: The distance-squared error for all outputs.
        """

        return self.trainer(input_vector, expected_output_vector)

    def do_training(self, epochs=10000):
        """
        Trains the network on all its built-in training cases for the given number of epochs.

        :param epochs: The number of epochs to train for.
        :return: A list of the sum of errors squared for each session.
        """

        errors = []

        for i in range(epochs):
            error = 0
            for c in self.training_cases:
                error += self.train_for_one_example(c, c)

            errors.append(error)
            print(i)

        return errors

    def do_testing(self):
        """
        Does a test for all test test_cases.

        :return: The output activations for each example.
        """
        output_activations = []

        for c in self.test_cases:
            output_activations.append(self.output_for_input(c))

        return output_activations


def gen_all_bit_cases(num_bits):
    def bits(n):
        s = bin(n)[2:]
        return [int(b) for b in '0'*(num_bits - len(s))+s]

    return [bits(i) for i in range(2**num_bits)]

if __name__ == '__main__':
    input_no = 3
    output_no = 3
    hidden_top = [3, 2]
    bit_cases = gen_all_bit_cases(3)
    ann = ArtificialNeuralNetwork(input_no, hidden_top, output_no, bit_cases, bit cases)
    errors = ann.do_training()
    for e in errors:
        print(e)

    a = ann.predictor([1, 0, 0])
    for b in a:
        print(round(b))