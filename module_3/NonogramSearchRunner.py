import sys
import module_1.BestFirstSearch as BFS
import module_3.NonogramProblem as NonogramProblem
from time import sleep, time
from tabulate import tabulate

NGP = NonogramProblem.NonogramProblem


def print_statistics_to_console(results, start_time, end_time):
        """
        Prints statistics about the three runs to console.
        :return:
        """
        table_data = []

        closed_nodes = len(results['closed_set'])
        open_nodes = len(results['open_set'])
        passed_nodes = results['nodes_passed_over']
        total_nodes = passed_nodes+closed_nodes+open_nodes
        table_data.append([total_nodes,
                           closed_nodes,
                           open_nodes,
                           passed_nodes,
                           len(results['solution'])-1,
                           round(end_time-start_time, 2)])

        print(tabulate(table_data, headers=['Total', 'Closed',
                                            'Open', 'Passed', 'Assumptions for solution', 'Time (secs)']))


if __name__ == '__main__':
    f = open(sys.argv[1])

    spec = f.readlines()

    for i in range(len(spec)):
        row_as_strings = spec[i].strip().split()
        for j in range(len(row_as_strings)):
            row_as_strings[j] = int(row_as_strings[j])

        spec[i] = row_as_strings

    a = time()
    ngp = NGP(spec)

    result = BFS.a_star(ngp, NGP.all_domains_have_size_one, lambda x, y: 0, NGP.domain_sizes_minus_one)
    b = time()
    result['current'].print_final_solution()
    print_statistics_to_console(result, a, b)
    sleep(5)
