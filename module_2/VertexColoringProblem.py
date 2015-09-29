from module_2.CSProblem import CSProblem
from module_2.Constraint import Constraint


class VertexColoringProblem(CSProblem):
    def __init__(self, specification, k):
        super(VertexColoringProblem, self).__init__()
        self.coordinates = {}
        self.edges = []

        number_of_vertices, number_of_edges = specification[0]
        number_of_vertices, number_of_edges = int(number_of_vertices), int(number_of_edges)

        for i in range(1, number_of_vertices+1):
            vertex_name, vertex_x, vertex_y = specification[i]
            vertex_x, vertex_y = float(vertex_x), float(vertex_y)

            domain = set([i for i in range(k)])

            self.domains[vertex_name] = domain
            self.coordinates[vertex_name] = {'x':vertex_x, 'y':vertex_y}

        for i in range(number_of_vertices+1, len(specification)):
            edge_i, edge_j = specification[i]

            self.constraints.append(Constraint(['x', 'y'], 'x != y', (edge_i, edge_j)))
            self.edges.append((edge_i, edge_j))

        self.initialize_queue()
        self.domain_filtering()
