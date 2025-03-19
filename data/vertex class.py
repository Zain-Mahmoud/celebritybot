class _Vertex:
    """
    A vertex in a graph.

    Instance Attributes:
        - word: the word stored in the vertex
        - neighbours: all the vertices that are adjacent to this
    """

    def __init__(self, word) -> None:
        self._word = word
        self._neighbours = {}

    def degree(self) -> int:
        """"
        Returns the degree of the vertex
        """
        return sum(len(self._neighbours[key]) for key in self._neighbours)

    def add_neighbour(self, item, weight) -> None:
        """
        Adds the item with its weight as a neighbour of the vertex
        """
        if weight in self._neighbours:
            self._neighbours[weight].append(_Vertex(item))
        else:
            self._neighbours[weight] = [_Vertex(item)]

    def get_neighbours_weight(self, weight : float) -> set:
        """
        Returns a list of all the vertices adjacent to this
        vertex that have the given weight.

        Raises ValueError if no such vertex exists
        """
        if weight in self._neighbours:
            return self._neighbours[weight]
        raise ValueError
