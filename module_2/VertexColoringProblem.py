from module_2.CSProblem import CSProblem
from module_2.Constraint import Constraint


class VertexColoringProblem(CSProblem):
    """
    Subclass of the constraint satisfaction problem class used in vertex coloring.
    """
    def __init__(self, specification, k):
        """
        Initializes the problem from a specification.

        :param specification: Specification on the form specified in the task description.
        :param k: Number of colors available
        :return:
        """
        super(VertexColoringProblem, self).__init__()

        # Structures used for graphical user interface
        self.vertices = {}  # A dictionary linking variable names to coordinates, form {var_name: (x, y)}
        self.edges = []  # A list of edges. Tuples of form (var_a_name, var_b_name)

        number_of_vertices, number_of_edges = specification[0]  # First line contains these important numbers
        number_of_vertices, number_of_edges = int(number_of_vertices), int(number_of_edges)

        # Getting initial values for maximums and minimums
        _, first_x, first_y = specification[1]
        self.x_min, self.y_min = self.x_max, self.y_max = float(first_x), float(first_y)

        # Initializing domains and vertices
        for i in range(1, number_of_vertices+1):
            vertex_name, vertex_x, vertex_y = specification[i]
            vertex_x, vertex_y = float(vertex_x), float(vertex_y)

            domain = set([i for i in range(k)])

            self.domains[vertex_name] = domain
            self.vertices[vertex_name] = (vertex_x, vertex_y)

            self.x_min, self.y_min = min(vertex_x, self.x_min), min(vertex_y, self.y_min)
            self.x_max, self.y_max = max(vertex_x, self.x_max), max(vertex_y, self.y_max)

        # Initializing constraints and edges
        for i in range(number_of_vertices+1, len(specification)):
            edge_i, edge_j = specification[i]

            self.constraints.append(Constraint(['x', 'y'], 'x != y', (edge_i, edge_j)))
            self.edges.append((edge_i, edge_j))

        # Run the initialization and filtering
        self.initialize_queue()
        self.domain_filtering()
