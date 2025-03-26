from __future__ import annotations
from enum import Enum, auto


class VertexKind(Enum):
    """
    Represents whether the vertex is a single word, or an ngram of specified size.

    The size of the ngram is specified as an int in the Graph class.
    """
    NGRAM = auto()
    WORD = auto()


class Vertex:
    """
    A vertex in a graph.

    Instance Attributes:
        - word: the word stored in the vertex, or a tuple of n-grams, depending on the vertex type
        - neighbours: all the vertices that are adjacent to this vertex
        - kind: whether this is a word or n-gram
    """
    word: str | tuple
    neighbours: dict[Vertex, int]
    kind: VertexKind


    def __init__(self, word) -> None:
        """
        Initialize a vertex, given a word or ngram.

        Detects whether it is a word or ngram.
        """
        self.word = word
        self.neighbours = {}
        self.kind = VertexKind.WORD if isinstance(word, str) else VertexKind.NGRAM

    def add_neighbour(self, v: Vertex) -> None:
        """
        Adds the item as a neighbour of the vertex.
        """

        if v in self.neighbours:
            self.neighbours[v] += 1
        else:
            self.neighbours[v] = 1

    def _get_total_neighbour_weights(self) -> int:
        """
        Get the total weights of this vertex pointing to all neighbour nodes.
        """
        total_weight = 0

        for i in self.neighbours.values():
            total_weight += i

        return total_weight

    def get_neighbours_and_probabilities(self) -> tuple[list[Vertex], list[float]]:
        """
        Return a tuple containing:
            - a list of neighbours
            - a list of each neighbour's probability, calculated from weight / total weights of all neighbours

        Preconditions:
            - the index of each element in the probablities and neighbours tuple correspond to each other
        """
        neighbours = []
        probabilities = []

        total_weight = self._get_total_neighbour_weights()

        for k, v in self.neighbours.items():
            neighbours.append(k)
            probabilities.append(v / total_weight)

        return neighbours, probabilities
