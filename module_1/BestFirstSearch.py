from collections import defaultdict as defdict
import heapq as hq


def a_star(start, goal, neighbour_nodes, dist_between, heuristic_cost_estimate):
    # Based on the pseudocode from Wikipedia: https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

    closed_set = set()
    open_set = [(0, start)]  # Heap. Tuples sort lexicographically. First argument is f_score
    came_from = dict()

    g_score = defdict(lambda: float('inf'))
    g_score[start] = 0

    f_score = defdict(lambda: float('inf'))
    f_score[start] = g_score[start] + heuristic_cost_estimate(start, goal)

    while open_set:
        _, current = hq.heappop(open_set)

        if current in closed_set:
            continue

        if current == goal:
            return reconstruct_path(came_from, goal)

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

                hq.heappush(open_set, (tentative_f_score, neighbour))

    return False


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)

    total_path.reverse()

    return tuple(total_path)
