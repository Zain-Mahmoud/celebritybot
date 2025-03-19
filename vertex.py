from __future__ import annotations
import graphviz

class Vertex:
    """
    A vertex in a graph.

    Instance Attributes:
        - word: the word stored in the vertex
        - neighbours: all the vertices that are adjacent to this vertex
        - vertex
    """
    word: str
    neighbours: dict[Vertex, int]

    def __init__(self, word) -> None:
        self.word = word
        self.neighbours = {}

    def degree(self) -> int:
        """"
        Returns the degree of the vertex
        """
        return len(self.neighbours)

    def add_neighbour(self, v: Vertex) -> None:
        """
        Adds the item as a neighbour of the vertex
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


class Stop(Vertex):
    """A vertex containing stopping punctuation (.!?) instead of a word

    Note: no functionality change from the Vertex class, but differentiated for ease in parsing."""

    pass
