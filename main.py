"""
CSC111 Project 2

TrumpBot
"""

from graph import Graph

import time
import random


TEXT_FILE = "data/donaldtrump.txt"
NGRAM_VALUE = 3


if __name__ == "__main__":

    graph = Graph(TEXT_FILE, NGRAM_VALUE)

    words = []

    prompt = input(f"\nEnter a prompt: ").lower().split()

    if len(prompt) > 1:
        words += list(prompt[-NGRAM_VALUE:])
    else:
        words.append(prompt[0])

    while True:

        next_word = graph.predict_next_word(tuple(words[-NGRAM_VALUE:]))
        words.append(next_word)
        print(next_word, end=" ")

        time.sleep(random.randint(0, 500) / 1000)
