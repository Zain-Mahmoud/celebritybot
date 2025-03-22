from __future__ import annotations
from enum import Enum, auto
import graphviz


class VertexKind(Enum):
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
        self.word = word
        self.neighbours = {}
        self.kind = VertexKind.WORD if isinstance(word, str) else VertexKind.NGRAM

    def degree(self) -> int:
        """"
        Returns the degree of the vertex
        """
        return len(self.neighbours)

    def add_neighbour(self, v: Vertex) -> None:
        """
        Adds the item as a neighbour of the vertex

        Preconditions:
            - not (self.kind == VertexKind.WORD) or (v.kind == VertexKind.NGRAM)
            - not (self.kind == VertexKind.NGRAM) or (v.kind == VertexKind.WORD)
        """

        if v in self.neighbours:
            self.neighbours[v] += 1
        else:
            self.neighbours[v] = 1

    def _get_total_neighbour_weights(self) -> int:
        total_weight = 0

        for i in self.neighbours.values():
            total_weight += i

        return total_weight

    def get_neighbours_and_probabilities(self) -> tuple[list[Vertex], list[float]]:

        neighbours = []
        probabilities = []

        total_weight = self._get_total_neighbour_weights()

        for k, v in self.neighbours.items():
            neighbours.append(k)
            probabilities.append(v / total_weight)

        return neighbours, probabilities
