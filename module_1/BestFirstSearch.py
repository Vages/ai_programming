from collections import defaultdict
import heapq as hq


class UnsolvableError(Exception):
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def __str__(self):

        return 'No possible path from ' + str(self.start) + ' to ' + str(self.goal)


def a_star(start, goal, neighbour_nodes, dist_between, heuristic_cost_estimate, mode="best_first"):
    # Based on the pseudocode from Wikipedia: https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

    closed_set = set()
    open_set = [(0, start)]  # Heap. Tuples sort lexicographically. First argument is f_score
    came_from = dict()

    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0

    f_score = defaultdict(lambda: float('inf'))
    f_score[start] = g_score[start] + heuristic_cost_estimate(start, goal)

    depth_or_breadth_first_priority = 0

    while open_set:
        _, current = hq.heappop(open_set)

        if current in closed_set:  # Node already examined. No need to do it again due to heap optimality.
            continue

        if current == goal:
            return {'solution': reconstruct_path(came_from, goal)}

        closed_set.add(current)

        for neighbour in neighbour_nodes(current):
            if neighbour in closed_set:
                continue

            tentative_g_score = g_score[current] + dist_between(current, neighbour)

            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score

                tentative_f_score = tentative_g_score + heuristic_cost_estimate(neighbour, goal)
                f_score[neighbour] = tentative_f_score

                if mode == 'best_first':
                    priority = tentative_f_score
                if mode == 'depth_first':
                    depth_or_breadth_first_priority -= 1
                    priority = depth_or_breadth_first_priority
                if mode == 'breadth_first':
                    depth_or_breadth_first_priority += 1
                    priority = depth_or_breadth_first_priority

                hq.heappush(open_set, (priority, neighbour))

    raise UnsolvableError(start, goal)


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)

    total_path.reverse()

    return tuple(total_path)
