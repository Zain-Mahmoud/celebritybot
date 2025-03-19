class Vertex:
    """
    A vertex in a graph.

    Instance Attributes:
        - word: the word stored in the vertex
        - neighbours: all the vertices that are adjacent to this vertex
    """

    def __init__(self, word) -> None:
        self.word = word
        self.neighbours = {}

    def degree(self) -> int:
        """"
        Returns the degree of the vertex
        """
        return len(self.neighbours)

    def add_neighbour(self, item) -> None:
        """
        Adds the item as a neighbour of the vertex
        """
        self.neighbours[Vertex(item)] = 1

    def get_neighbours_weight(self, weight: float) -> list:
        """
        Returns a list of all the vertices adjacent to this
        vertex with the given weight.

        """
        return [key for key in self.neighbours if self.neighbours[key] == weight]
