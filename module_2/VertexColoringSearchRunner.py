import sys
import module_1.BestFirstSearch as BFS
import module_2.VertexColoringProblem as VertexColoringProblem
from GraphicsModule2 import Gfx
from time import sleep

VCP = VertexColoringProblem.VertexColoringProblem


if __name__ == '__main__':
    f = open(sys.argv[1])
    k = int(sys.argv[2])

    spec = f.readlines()

    for i in range(len(spec)):
        spec[i] = spec[i].strip().split()

    vcp = VCP(spec, k)

    gfx = Gfx(vcp, 10, (800, 800))

    result = BFS.a_star(vcp, VCP.all_domains_have_size_one, lambda x, y: 0, VCP.domain_sizes_minus_one,
                        mode='best_first', gui_function=gfx.draw)

    sleep(5)