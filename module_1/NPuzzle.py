from copy import deepcopy
from module_1.BestFirstSearch import a_star


class NPuzzle:
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

    def manhattan_distance(self, current_state, goal_state):
        current_map = {}

        for i in range(len(current_state)):
            for j in range(len(goal_state[i])):
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
    def move_cost(*useless_arguments):
        return 1


if __name__ == '__main__':
    advanced_start_state = ((8, 6, 7),
                            (2, 5, 4),
                            (3, 0, 1))

    advanced_goal_state = ((1, 2, 3),
                           (4, 5, 6),
                           (7, 8, 0))

    my_puzzle = NPuzzle(advanced_goal_state)
    results = a_star(advanced_start_state,
                     advanced_goal_state,
                     my_puzzle.generate_next_states,
                     my_puzzle.move_cost,
                     my_puzzle.manhattan_distance)
    print("success")