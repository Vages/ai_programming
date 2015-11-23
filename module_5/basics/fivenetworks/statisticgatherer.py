__author__ = 'eirikvageskar'

import statistics

if __name__ == '__main__':
    filenames = ["100.txt", "200.txt", "100_100.txt", "200_200.txt", "200_150_100.txt"]

    for fn in filenames:
        f = open(fn, 'r')

        test_case_pcts = []
        training_case_pcts = []
        error_rates = []
        times_elapsed = []
        for line in f.readlines():
            if line.startswith('Percentage wrong on test cases'):
                data = line.split(": ")
                test_case_pcts.append(float(data[1]))

            elif line.startswith('Percentage wrong on training cases'):
                data = line.split(': ')
                training_case_pcts.append(float(data[1]))

            elif line.startswith('Training error rates'):
                data = line.split(': ')
                error_rates.append(eval(data[1]))

            elif line.startswith('Time elapsed'):
                data = line.split(': ')
                times_elapsed.append(int(data[1]))


        sum_of_error_rates = [0]*20

        for error_rate_collection in error_rates:
            for i in range(len(error_rate_collection)):
                sum_of_error_rates[i] += error_rate_collection[i][1]

        for i in range(len(sum_of_error_rates)):
            sum_of_error_rates[i] /= len(sum_of_error_rates)

        print(fn)
        print("Average error on test cases:", statistics.mean(test_case_pcts))
        print("Average error on training cases:", statistics.mean(training_case_pcts))
        print("Average training time:", statistics.mean(times_elapsed))
        print("Average error during epochs", list(enumerate(sum_of_error_rates, 1)))
        for s in sum_of_error_rates:
            print(s)
        print()
