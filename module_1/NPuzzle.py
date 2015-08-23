from copy import deepcopy
from module_1.BestFirstSearch import a_star


class NPuzzle:
    """
    Contains a sliding puzzle, known as the n-puzzle (n-by-n board size).
    A 3-by-3 n-puzzle is solved in about a second. 4-by-4
    """
    def __init__(self, goal_state):
        self.x_size = len(goal_state[0])
        self.y_size = len(goal_state)
        self.goal_state = goal_state
        self.goal_map = {}
        self.directions = ((-1, 0),
                      (1, 0),
                      (0, -1),
                      (0, 1))

        # Make a map from value to coordinate for faster lookup
        for i in range(len(self.goal_state)):
            for j in range(len(self.goal_state[i])):
                self.goal_map[goal_state[i][j]] = (j, i)

    def manhattan_distance(self, current_state, *unused_arguments):
        current_map = {}

        for i in range(self.y_size):
            for j in range(self.x_size):
                current_map[current_state[i][j]] = (j, i)

        total_distance = 0

        for i in current_map:
            if i == 0:
                continue

            x1, y1 = current_map[i]
            x2, y2 = self.goal_map[i]

            total_distance += abs(x2-x1)+abs(y2-y1)

        return total_distance

    @staticmethod
    def find_position(state, tile):
        for i in range(len(state)):
            try:
                return state[i].index(tile), i
            except ValueError:
                continue

    def generate_next_states(self, state):
        x, y = self.find_position(state, 0)
        candidate_moves = set()

        for direction in self.directions:
            d_x, d_y = direction

            candidate_moves.add((x+d_x, y+d_y))
            
        impossible_moves = set()

        for candidate in candidate_moves:
            c_x, c_y = candidate
            
            if 0 <= c_x < self.x_size and 0 <= c_y < self.y_size:
                continue
            
            impossible_moves.add(candidate)
            
        possible_moves = candidate_moves - impossible_moves

        list_version_of_state = []

        for line in state:
            list_version_of_state.append(list(line))

        next_states = set()

        for move in possible_moves:
            m_x, m_y = move
            swapped_list = deepcopy(list_version_of_state)
            swapped_list[m_y][m_x], swapped_list[y][x] = swapped_list[y][x], swapped_list[m_y][m_x]

            for i in range(len(swapped_list)):
                swapped_list[i] = tuple(swapped_list[i])

            next_states.add(tuple(swapped_list))

        return next_states

    @staticmethod
    def move_cost(*unused_arguments):
        return 1

    def linear_conflicts(self, current_state, *unused_arguments):
        no_of_linear_conflicts = 0

        for i in range(len(current_state)):
            row_i = current_state[i]
            for j in range(len(row_i)):
                elem_j_i = row_i[j]
                if elem_j_i == 0:
                    continue

                goal_j_i = self.goal_map[elem_j_i]
                if goal_j_i == (j, i):
                    continue

                g_x, g_y = goal_j_i

                if g_y == i:
                    for k in range(j+1, len(row_i)):
                        elem_k_i = row_i[k]
                        if elem_k_i == 0:
                            continue
                        goal_k_i = self.goal_map[elem_k_i]

                        k_x, k_y = goal_k_i
                        if k_y == i:  # Its goal is in the same line
                            if k_x < g_x:
                                no_of_linear_conflicts += 2
                    continue

                if g_x == j:
                    for l in range(i+1, len(current_state)):
                        elem_j_l = current_state[l][j]
                        if elem_j_l == 0:
                            continue
                        goal_j_l = self.goal_map[elem_j_l]

                        l_x, l_y = goal_j_l

                        if l_x == j:
                            if l_y < g_y:
                                no_of_linear_conflicts += 2

        return no_of_linear_conflicts

    def manhattan_and_linear(self, current_state, *unused_arguments):
        return self.manhattan_distance(current_state)+self.linear_conflicts(current_state)

    def solvable_from_state(self, state, *unused_arguments):
        open_square_pos = self.find_position(state, 0)
        open_square_goal = self.goal_map[0]
        osp_x, osp_y = open_square_pos
        osg_x, osg_y = open_square_goal
        manhattan_distance_of_open_square = abs(osg_y-osp_y)+abs(osg_x-osp_x)
        open_square_parity = manhattan_distance_of_open_square % 2

        state_as_1d_list = []
        goal_as_1d_list = []
        permutations = 0

        for i in range(self.y_size):
            for j in range(self.x_size):
                state_as_1d_list.append(state[i][j])
                goal_as_1d_list.append(self.goal_state[i][j])

        for i in range(len(state_as_1d_list)):
            goal_elem_i = goal_as_1d_list[i]
            j = state_as_1d_list.index(goal_elem_i)
            if j > i:
                state_as_1d_list[j], state_as_1d_list[i] = state_as_1d_list[i], state_as_1d_list[j]
                permutations += 1

        parity_of_permutations = permutations % 2

        return open_square_parity == parity_of_permutations

if __name__ == '__main__':
    start_3_by_3 = ((8, 6, 7),
                    (2, 5, 4),
                    (3, 0, 1))

    goal_3_by_3 = ((1, 2, 3),
                   (4, 5, 6),
                   (7, 8, 0))

    start_4_by_4 = ((15, 14, 13, 12),
                    (11, 10, 9, 8),
                    (7, 6, 5, 4),
                    (3, 1, 2, 0))

    goal_4_by_4 = ((1, 2, 3, 4),
                   (5, 6, 7, 8),
                   (9, 10, 11, 12),
                   (13, 14, 15, 0))

    start_easier_4_by_4 = ((15, 1, 2, 3),
                           (4, 5, 6, 7),
                           (8, 9, 10, 11),
                           (0, 13, 14, 12))

    goal_easier_4_by_4 = ((0, 1, 2, 3),
                          (4, 5, 6, 7),
                          (8, 9, 10, 11),
                          (12, 13, 14, 15))

    my_puzzle = NPuzzle(goal_easier_4_by_4)
    results = a_star(start_easier_4_by_4,
                     goal_easier_4_by_4,
                     my_puzzle.generate_next_states,
                     my_puzzle.move_cost,
                     my_puzzle.manhattan_and_linear,
                     solvability_test=my_puzzle.solvable_from_state)

    print(len(results['closed_set']))
