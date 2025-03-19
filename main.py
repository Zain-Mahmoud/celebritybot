"""
CSC111 Project 2

TrumpBot
"""

from vertex import Vertex, Stop
from graph import Graph

import difflib
import numpy as np
import nltk


TEXT_FILE = "data/dataset.txt"


def predict_sentence(graph: Graph, starting_word: str) -> list[str]:
    """
    ...

    Precondition:
        - starting_word in graph.vertices
    """

    sentence_list = [starting_word]

    word_vertex = graph.vertices[starting_word]

    while not isinstance(word_vertex, Stop):

        neighbours, probabilities = word_vertex.get_neighbours_and_probabilities()

        if not neighbours:
            break

        for i in range(len(neighbours)):
            print(f"{neighbours[i].word} : {probabilities[i]}")

        new_word_vertex = np.random.choice(neighbours, p=probabilities)
        sentence_list.append(new_word_vertex.word)

        word_vertex = new_word_vertex
        print(f"Chose: {word_vertex.word}")

    return sentence_list



def get_text_from_file(file_name: str) -> str:
    with open(file_name, 'r') as f:
        text = f.read()
    return text


def parse_text(text: str) -> Graph:
    """Return a Graph representation of text."""
    g = Graph()
    tokens = nltk.word_tokenize(text)
    for i in range(len(tokens)):
        if tokens[i] in ".?!":
            g.add_stop(tokens[i])
        else:
            g.add_vertex(tokens[i])
            g.add_vertex(tokens[i+1])
            g.add_edge(tokens[i], tokens[i+1])
    return g


if __name__ == "__main__":

    graph = parse_text(get_text_from_file(TEXT_FILE))

    while True:

        prompt = input("\nEnter prompt: ")
        if prompt in graph.vertices:

            sentence = predict_sentence(graph, prompt)
            print(" ".join(sentence))
        else:
            print("Word not available.")
