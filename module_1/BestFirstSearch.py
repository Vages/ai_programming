from collections import defaultdict
import heapq as hq


class UnsolvableError(Exception):
    """
    Raised when there is no possible solution from the given start state.
    """
    def __init__(self, start):
        self.start = start

    def __str__(self):
        return 'No possible solution starting from ' + str(self.start)


def a_star(start, goal_test, move_cost, heuristic_cost_estimate, mode="best_first",
           solvability_test=False, gui_function=False):
    """
    Implementation of the A* best-first-search algorithm, based on the pseudocode from Wikipedia:
    https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

    :param start: Start state
    :param goal_test: Function which tests if a state is the goal
    :param neighbour_nodes: Returns all possible next states given a current state.
    :param move_cost: Computes the cost of a move from the current state to one of its successors.
    :param heuristic_cost_estimate: Estimates cost of moving from given state to a goal state.
    :param mode: Controls search behaviour. Can also be set to depth_first or breadth_first.
    :param solvability_test: For some domains, e.g. N-puzzle, we can determine with a simple function what whether one
    state is reachable from the other.
    :return:
    """

    def return_current_data():
        # Remove priority from elements in open set
        open_set_return_elements = set()
        for element in open_set:
            _, node = element
            if node in closed_set:
                continue
            open_set_return_elements.add(node)

        return {'solution': reconstruct_path(came_from, current),
                'solution_cost': g_score[current],
                'closed_set': closed_set,
                'open_set': open_set_return_elements,
                'came_from': came_from,
                'nodes_passed_over': nodes_passed_over,
                'current': current}

    if solvability_test:
        if not solvability_test(start):
            raise UnsolvableError(start)

    closed_set = set()  # Nodes whose successors have been added to open set.
    open_set = [(0, start)]  # Min-heap. First argument is f_score in best-first search
    came_from = dict()  # Predecessors.

    g_score = defaultdict(lambda: float('inf'))  # g_score[n] == Cost of moving to node n
    g_score[start] = 0

    depth_or_breadth_first_priority = 0  # Controls priority when mode is set to depth- or breadth-first.
    nodes_passed_over = 0

    while open_set:
        _, current = hq.heappop(open_set)

        if current in closed_set:  # Node already examined.
            nodes_passed_over += 1
            continue

        if gui_function:
            gui_function(return_current_data())
        if goal_test(current):
            return return_current_data()

        closed_set.add(current)

        for neighbour in current.get_successors():
            if neighbour in closed_set:
                continue

            tentative_g_score = g_score[current] + move_cost(current, neighbour)

            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score

                if mode == 'best_first':
                    priority = tentative_g_score + heuristic_cost_estimate(neighbour)
                if mode == 'depth_first':
                    depth_or_breadth_first_priority -= 1
                    priority = depth_or_breadth_first_priority
                if mode == 'breadth_first':
                    depth_or_breadth_first_priority += 1
                    priority = depth_or_breadth_first_priority

                hq.heappush(open_set, (priority, neighbour))

    raise UnsolvableError(start)


def reconstruct_path(came_from, current):
    """
    Returns sequence of states from start to goal state, inclusively.

    :param came_from: Dictionary mapping each node to its immediate predecessor.
    :param current:
    :return: The path, sorted from start to goal.
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)

    total_path.reverse()

    return total_path

