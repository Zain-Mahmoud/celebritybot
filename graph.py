import difflib
import nltk
import numpy as np
from typing import Any

from vertex import Vertex, VertexKind


# Ensure nltk punkt is installed
try:
    nltk.data.find('tokenizers/punkt_tab.zip')
except LookupError:
    nltk.download('punkt_tab')

# Helper functions
def contains_end_char(check_string: str | list | tuple) -> bool:
    """Return whether the sentence contains an end character, which is one of: . ! ?"""
    for i in [".", "!", "?"]:
        if i in check_string:
            return True
    return False


def get_lowered_text_from_file(file_name: str) -> str:
    """Return a string of the lower-case text from a file."""

    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    return text


class Graph:
    """A graph.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)

    Instance Attributes:
        - vertices: A collection of the vertices in the graph
        - ngram_value: The size of n-gram to use
        - file_name: The name of the text file represented by the graph
    """

    # Instance attributes
    vertices: dict[Any, Vertex]
    ngram_value: int
    file_name: str

    # Private instance attributes
    _available_ngrams: list[tuple]
    _available_words: list[str]

    def __init__(self, text_file: str, ngram_value) -> None:
        """Initialize a graph populated with the words from the text file and n-gram value."""
        self.vertices = {}
        self.ngram_value = ngram_value
        self.file_name = text_file

        self._parse_text(get_lowered_text_from_file(text_file))

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        if item not in self.vertices:
            self.vertices[item] = Vertex(item)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            v2 = self.vertices[item2]

            # Add the new edge
            v1.add_neighbour(v2)
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def _parse_text(self, text: str) -> None:
        """Parse the text and fill in the current graph."""

        tokens = nltk.word_tokenize(text)
        for i in range(len(tokens) - self.ngram_value):
            # Map ngram to next word
            ngram = tuple(tokens[i + j] for j in range(self.ngram_value))
            next_word = tokens[i + self.ngram_value]
            self.add_vertex(ngram)
            self.add_vertex(next_word)
            self.add_edge(ngram, next_word)

        # Map each individual word
        for i in range(len(tokens) - 1):
            v1_item = tokens[i]
            v2_item = tokens[i + 1]
            self.add_vertex(v1_item)
            self.add_vertex(v2_item)
            self.add_edge(v1_item, v2_item)

        self._find_available_words_and_ngrams()

    def _find_available_words_and_ngrams(self):
        """Puts all available words and ngrams into lists."""

        self._available_words = []
        self._available_ngrams = []

        for item in self.vertices:
            v = self.vertices[item]

            if v.kind == VertexKind.NGRAM:
                self._available_ngrams.append(item)
            elif v.kind == VertexKind.WORD:
                self._available_words.append(item)

    def predict_next_word(self, word: tuple | str) -> str:
        """
        Given a word or a tuple of n words, return a next-word.

        The word or tuple of words do not have to be in the graph. If it is not, it will pick the closest match.

        Parameters:
            - word: the word to start with
        """

        if word in self._available_words or word in self._available_ngrams:
            word_vertex = self.vertices[word]
            neighbours, probabilities = word_vertex.get_neighbours_and_probabilities()
            new_word_vertex = np.random.choice(neighbours, p=probabilities)
            return new_word_vertex.word
        else:

            if isinstance(word, tuple):
                return self.predict_next_word(word[-1])
            else:
                new_word = difflib.get_close_matches(word, self._available_words, n=1, cutoff=0)
                return self.predict_next_word(new_word[0])
