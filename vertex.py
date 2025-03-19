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
        return sum(len(self.neighbours[key]) for key in self.neighbours)

    def add_neighbour(self, item, weight) -> None:
        """
        Adds the item with its weight as a neighbour of the vertex
        """
        if weight in self.neighbours:
            self.neighbours[weight].append(Vertex(item))
        else:
            self.neighbours[weight] = [Vertex(item)]

    def get_neighbours_weight(self, weight: float) -> set:
        """
        Returns a list of all the vertices adjacent to this
        vertex that have the given weight.

        Raises ValueError if no such vertex exists
        """
        if weight in self.neighbours:
            return self.neighbours[weight]
        raise ValueError
