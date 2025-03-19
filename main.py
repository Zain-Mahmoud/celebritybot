"""
CSC111 Project 2

TrumpBot
"""

from vertex import Vertex, Stop
from graph import Graph

import numpy
import nltk

def predict_sentence(graph: Graph, starting_word: str):
    ...


def parse_text(text: str) -> Graph:

    g = Graph()
    tokens = nltk.word_tokenize(text)
    for i in range(len(tokens)):
        if tokens[i] in ".?!":
            g.add_stop(tokens[i])
        else:
            g.add_vertex(tokens[i])
            g.add_edge(tokens[i], tokens[i+1], 1)
    return g
