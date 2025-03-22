"""
CSC111 Project 2

TrumpBot
"""

from vertex import Vertex
from graph import Graph

import difflib
import numpy as np
import nltk
import time
import random


TEXT_FILE = "data/speeches_text.txt"
NGRAM_VALUE = 3


def contains_end_char(check_string: str | list | tuple) -> bool:
    """
    Return whether the sentence contains a stop character,
    which is one of: . ! ?
    """

    for i in [".", "!", "?"]:
        if i in check_string:
            return True
    return False


def get_lowered_text_from_file(file_name: str) -> str:
    """Return a string of the lower-case text from a file."""

    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    return text


def parse_text(text: str) -> Graph:
    """Return a Graph representation of text."""

    g = Graph()
    tokens = nltk.word_tokenize(text)
    for i in range(len(tokens) - NGRAM_VALUE):

        # Map ngram to next word
        ngram = tuple(tokens[i + j] for j in range(NGRAM_VALUE))
        next_word = tokens[i + NGRAM_VALUE]
        g.add_vertex(ngram)
        g.add_vertex(next_word)
        g.add_edge(ngram, next_word)

    # Map each individual word
    for i in range(len(tokens) - 1):
        v1_item = tokens[i]
        v2_item = tokens[i + 1]
        g.add_vertex(v1_item)
        g.add_vertex(v2_item)
        g.add_edge(v1_item, v2_item)

    return g


def predict_next_word(graph: Graph, word: tuple | str) -> str:
    """
    Given a word or a tuple of n words, return a next-word.

    The word or tuple of words do not have to be in the graph. If it is not, it will pick the closest match.
    """
    available_tuples = [item for item in graph.vertices if isinstance(item, tuple)]
    available_strings = [item for item in graph.vertices if isinstance(item, str)]

    if word in available_strings or word in available_tuples:
        word_vertex = graph.vertices[word]
        neighbours, probabilities = word_vertex.get_neighbours_and_probabilities()
        new_word_vertex = np.random.choice(neighbours, p=probabilities)
        return new_word_vertex.word
    else:

        if isinstance(word, tuple):
            return predict_next_word(graph, word[-1])
        else:
            new_word = difflib.get_close_matches(word, available_strings, n=1, cutoff=0)
            return predict_next_word(graph, new_word[0])



if __name__ == "__main__":

    global_graph = parse_text(get_lowered_text_from_file(TEXT_FILE))

    words = []

    prompt = input(f"\nEnter a prompt: ").lower().split()

    if len(prompt) > 1:
        words += list(prompt)
        prompt = tuple(prompt[-NGRAM_VALUE:])
    else:
        words.append(prompt)

    while True:

        next_word = predict_next_word(global_graph, tuple(words[-NGRAM_VALUE:]))
        words.append(next_word)
        print(next_word, end=" ")

        time.sleep(random.randint(0, 500) / 1000)
