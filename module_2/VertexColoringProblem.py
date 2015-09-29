from module_2.CSProblem import CSProblem
from module_2.Constraint import Constraint


class VertexColoringProblem(CSProblem):
    def __init__(self, specification, k):
        super(VertexColoringProblem, self).__init__()
        self.vertices = {}
        self.edges = []

        number_of_vertices, number_of_edges = specification[0]
        number_of_vertices, number_of_edges = int(number_of_vertices), int(number_of_edges)

        _, first_x, first_y = specification[1]
        self.x_min, self.y_min = self.x_max, self.y_max = float(first_x), float(first_y)

        for i in range(1, number_of_vertices+1):
            vertex_name, vertex_x, vertex_y = specification[i]
            vertex_x, vertex_y = float(vertex_x), float(vertex_y)

            domain = set([i for i in range(k)])

            self.domains[vertex_name] = domain
            self.vertices[vertex_name] = (vertex_x, vertex_y)

            self.x_min, self.y_min = min(vertex_x, self.x_min), min(vertex_y, self.y_min)
            self.x_max, self.y_max = max(vertex_x, self.x_max), max(vertex_y, self.y_max)

        for i in range(number_of_vertices+1, len(specification)):
            edge_i, edge_j = specification[i]

            self.constraints.append(Constraint(['x', 'y'], 'x != y', (edge_i, edge_j)))
            self.edges.append((edge_i, edge_j))

        self.initialize_queue()
        self.domain_filtering()
