import sys
import module_1.BestFirstSearch as BFS
import module_2.VertexColoringProblem as VertexColoringProblem
from GraphicsModule2 import Gfx
from time import sleep, time
from tabulate import tabulate

VCP = VertexColoringProblem.VertexColoringProblem


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
                           len(results['solution']),
                           round(end_time-start_time, 2)])

        print(tabulate(table_data, headers=['Total', 'Closed',
                                            'Open', 'Passed', 'Assumptions for solution', 'Time (secs)']))


if __name__ == '__main__':
    f = open(sys.argv[1])
    k = int(sys.argv[2])

    spec = f.readlines()

    for i in range(len(spec)):
        spec[i] = spec[i].strip().split()

    vcp = VCP(spec, k)

    gfx = Gfx(vcp, 10, (800, 800))

    a = time()
    result = BFS.a_star(vcp, VCP.all_domains_have_size_one, lambda x, y: 0, VCP.domain_sizes_minus_one,
                        mode='best_first', gui_function=gfx.draw)
    b = time()
    print_statistics_to_console(result, a, b)
    sleep(5)
