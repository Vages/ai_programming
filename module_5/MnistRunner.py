import pickle

__author__ = 'eirikvageskar'

import time
import basics.mnist_basics as mb
import MnistNetwork
import datetime
import sys

dt = datetime.datetime

mn = MnistNetwork.MnistNetwork



def apply_division_to_all_lists(list_of_lists, factor=255):
    """
    Downscales a lists of lists by a certain factor

    :param list_of_lists:
    :param factor:
    :return:
    """
    new_list = []
    for number_list in list_of_lists:
        new_list.append([entry/factor for entry in number_list])

    return new_list


def convert_int_to_unary_list(integer, max_value=9):
    temp = [0]*(max_value+1)

    temp[integer] = 1

    return temp


def convert_all_labels_to_unary_lists(label_list, max_value=9):
    return [convert_int_to_unary_list(i, max_value) for i in label_list]


if __name__ == '__main__':

    topologies = [[100],
                  [200],
                  [300],
                  [100, 100],
                  [200, 200]]


    try:
        f_test = open('test_cases.pickle', 'rb')
        f_training = open('training_cases.pickle', 'rb')
        test_cases = pickle.load(f_test)
        training_cases = pickle.load(f_training)
        f_test.close()
        f_test.close()
        print('Loaded training and test sets with pickle')

    except FileNotFoundError:
        training_input_raw, training_labels_raw = mb.load_cases('all_flat_mnist_training_cases', nested=False)
        test_input_raw, test_labels_raw = mb.load_cases('all_flat_mnist_testing_cases', nested=False)

        training_input = apply_division_to_all_lists(training_input_raw)
        training_labels = convert_all_labels_to_unary_lists(training_labels_raw)

        test_input = apply_division_to_all_lists(test_input_raw)
        test_labels = convert_all_labels_to_unary_lists(test_labels_raw)

        test_cases = list(zip(test_input, test_labels))
        training_cases = list(zip(training_input, training_labels))

        f_test = open('test_cases.pickle', 'wb')
        f_training = open('training_cases.pickle', 'wb')
        pickle.dump(test_cases, f_test)
        pickle.dump(training_cases, f_training)
        f_test.close()
        f_training.close()
        print('Saved training and test sets with pickle')

    print('creating network')

    for t in topologies:
        for i in range(20):
            hidden_layer_topology = t
            error_function = 'binary_cross'
            mnist_neural_net = mn(784, hidden_layer_topology, 10, training_cases, test_cases, error_func=error_function)

            a = time.time()

            no_of_epochs = 20
            error_rates = mnist_neural_net.do_training(no_of_epochs)
            print("Error rates:", error_rates)
            percentage_wrong_on_test_set = mnist_neural_net.get_percentage_of_tests_wrong()
            print("Error rate on test_set:", mnist_neural_net.get_percentage_of_tests_wrong())
            percentage_wrong_on_training_set = mnist_neural_net.get_percentage_of_tests_wrong(mnist_neural_net.training_cases)
            print("Error rate on training_set:", percentage_wrong_on_training_set)

            b = time.time()

            time_elapsed = round(b-a)
            print('Time elapsed during training and testing:', time_elapsed)

            with open("mnist_log.txt", "a") as logfile:
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

