__author__ = 'eirikvageskar'

import theano
import theano.tensor as T
import theano.tensor.nnet as Tann
import numpy as np

class ArtificialNeuralNetwork:
    def __init__(self, input_nodes_no, hidden_nodes_topology, output_nodes_no,
                 training_cases, test_cases, learning_rate=0.1, act_func='sigmoid', error_func='squared'):
        self.learning_rate = self.original_learning_rate = learning_rate
        self.trainer = None
        self.test_cases = test_cases
        self.training_cases = training_cases
        self.error_function = error_func
        self.build_artificial_neural_network(input_nodes_no, hidden_nodes_topology, output_nodes_no, act_func, error_func)

    def build_artificial_neural_network(self, no_of_input_nodes, hidden_nodes_topology, output_nodes_no, act_func, error_func):
        network_topology = [no_of_input_nodes] + hidden_nodes_topology + [output_nodes_no]

        weights = []
        biases = []

        for i in range(len(network_topology) - 1):
            weights.append(theano.shared(np.random.uniform(-.1, .1, size=(network_topology[i], network_topology[i+1]))))

        input_vector = T.dvector('input')
        expected_output_vector = T.dvector('expected_output')

        for i in range(1, len(network_topology)):
            biases.append(theano.shared(np.random.uniform(-.1, .1, size=network_topology[i])))

        activation_function = Tann.sigmoid

        if act_func == 'sigmoid':
            activation_function = Tann.sigmoid
        elif act_func == 'tanh':
            activation_function = T.tanh
        else:
            raise ValueError('Activation function must be "sigmoid" or "tanh"')

        outputs = [activation_function(T.dot(input_vector, weights[0]) + biases[0])]

        for i in range(1, len(network_topology)-1):
            outputs.append(activation_function(T.dot(outputs[i-1], weights[i]) + biases[i]))

        if error_func == 'squared':
            error = T.sum((expected_output_vector - outputs[-1])**2)
        elif error_func == 'binary_cross':
            error = Tann.binary_crossentropy(outputs[-1], expected_output_vector).mean()
        else:
            raise ValueError('Error function must be "squared" or "binary_cross"')

        params = []

        for i in range(len(network_topology) - 1):
            params.append(weights[i])
            params.append(biases[i])

        gradients = T.grad(error, params)
        back_propagation_activations = [(p, p-self.learning_rate*g) for p, g in zip(params, gradients)]

        self.trainer = theano.function([input_vector, expected_output_vector], error, updates=back_propagation_activations)
        self.predictor = theano.function([input_vector], outputs[-1])
        self.error_for_input = theano.function([input_vector, expected_output_vector], error)

    def output_for_input(self, input_vector):
        """
        Returns the neural network’s output for this input.

        :param input_vector: Some valid input vector
        :return: The network’s output
        """

        return self.predictor(input_vector)

    def error_for_one_example(self, input_vector, expected_output_vector):
        return self.error_for_input(input_vector, expected_output_vector)

    def train_for_one_example(self, input_vector, expected_output_vector):
        """
        Trains the network using one input-output example pair.

        :param input_vector: The example input.
        :param expected_output_vector: The example output.
        :return: The distance-squared error for all outputs.
        """

        return self.trainer(input_vector, expected_output_vector)

    def do_training(self, epochs=20):
        """
        Trains the network on all its built-in training cases for the given number of epochs.

        :param epochs: The number of epochs to train for.
        :return: A list of the sum of errors squared for each session.
        """

        errors = []

        for i in range(epochs):
            self.learning_rate = max(self.original_learning_rate, 1/(i+1))
            error = 0

            for input_v, output_v in self.training_cases:
                error += self.train_for_one_example(input_v, output_v)

            errors.append(error)
            print("Epoch:", i+1)
            print("\tError rate:", error)

        return errors

    def do_testing(self):
        """
        Does a test for all test test_cases.

        :return: The output activations for each example.
        """
        output_activations = []

        for input_v, output_v in self.test_cases:
            output_activations.append(self.output_for_input(input_v))

        return output_activations
