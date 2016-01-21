import pickle
import time
import basics.mnist_basics as mb
import MnistNetwork
import datetime
import sys
import basics.mnistdemo as md

dt = datetime.datetime

mn = MnistNetwork.MnistNetwork

__author__ = 'eirikvageskar'


if __name__ == '__main__':
    no_of_epochs = int(sys.argv[1])
    raw_topologies = sys.argv[2]
    error_function = sys.argv[3]
    activation_function = sys.argv[4]

    hidden_layer_topology = [int(raw) for raw in raw_topologies.split(";")]

    training_inputs, training_outputs = mb.load_cases('all_flat_mnist_training_cases', nested=False)
    test_inputs, test_outputs = mb.load_cases('all_flat_mnist_testing_cases', nested=False)

    mnist_neural_net = mn(784, hidden_layer_topology, 10, training_inputs, training_outputs, test_inputs,
                          test_outputs, activation_function=activation_function, error_function=error_function)

    print("created net")
    a = time.time()

    error_rates = mnist_neural_net.do_training(no_of_epochs)
    md.major_demo(mnist_neural_net, 1691, "/Users/eirikvageskar/PycharmProjects/ai_programming/module_5/basics/")
    print(mnist_neural_net.blind_test(mb.load_cases('demo100', nested=False)[0]))
    print("Error rates:", error_rates)
    percentage_wrong_on_test_set = mnist_neural_net.get_percentage_of_tests_wrong()
    print("Error rate on test_set:", mnist_neural_net.get_percentage_of_tests_wrong())
    percentage_wrong_on_training_set = \
        mnist_neural_net.get_percentage_of_tests_wrong(mnist_neural_net.training_inputs,
                                                       mnist_neural_net.training_outputs)


    print("Error rate on training_set:", percentage_wrong_on_training_set)


    b = time.time()

    time_elapsed = round(b-a)
    print('Time elapsed during training and testing:', time_elapsed)

    logfile = open("mnist_log.txt", "a")

    timestamp = dt.fromtimestamp(a)
    readable_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    logfile.write("\n\nTest started at " + readable_timestamp)
    logfile.write("\nTime elapsed: " + str(time_elapsed))
    logfile.write("\nHidden layer topology: " + str(hidden_layer_topology))
    logfile.write("\nError function: " + error_function)
    logfile.write("\nActivation function: " + activation_function)
    logfile.write("\nNumber of epochs: " + str(no_of_epochs))
    logfile.write("\nTraining error rates: " + str(list(enumerate(error_rates, 1))))
    logfile.write("\nPercentage wrong on test cases: " + str(percentage_wrong_on_test_set))
    logfile.write("\nPercentage wrong on training cases: " + str(percentage_wrong_on_training_set))

    logfile.close()
