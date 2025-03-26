"""
CSC111 Project 2

CelebrityBot
"""

from graph import Graph

import os
import random
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as tkfiledialog
from tkinter import messagebox as tkmessagebox


AVAILABLE_TEXT_FILES = {"Donald Trump": "data/donaldtrump.txt",
                        "Dr. Seuss": "data/drseuss.txt",
                        "Barack Obama": "data/Obama_Inaugural_Address.txt",
                        "Martin Luther King Jr.": "data/I_have_a_dream.txt",
                        "Choose your own text file": ""}
NGRAM_VALUE = 3
FONT = "Tahoma"


class GUIApp(tk.Tk):
    """
    GUI app that will demonstrate the program.
    """

    _graph: Graph

    # Private Attributes:
    #     - _ongoing: whether the program is currently outputting text
    _ongoing: bool

    def __init__(self):
        super().__init__()

        self.title("CelebrityBot")
        self.geometry("400x400")

        self._ongoing = False

        self.draw()

    def draw(self):

        # Title
        ttk.Label(self, text="CelebrityBot", font=(FONT, 30)).pack()

        ttk.Label(self, text="Select a person:", font=(FONT, 12)).pack()

        self.person_selector_var = tk.StringVar()
        self.person_selector_combobox = ttk.Combobox(self, width=30, state="readonly",
                                                     textvariable=self.person_selector_var,
                                                     values=list(AVAILABLE_TEXT_FILES.keys()))
        self.person_selector_combobox.current(0)
        self.person_selector_combobox.pack()

        ttk.Label(self, text="Initial prompt:", font=(FONT, 12)).pack()

        self.prompt_text_var = tk.StringVar()
        self.prompt_entry = ttk.Entry(self, width=30, textvariable=self.prompt_text_var)
        self.prompt_entry.pack()

        self.start_button_text_var = tk.StringVar(value="Start")
        self.start_button = ttk.Button(self, textvariable=self.start_button_text_var, command=self._handle_start_button)
        self.start_button.pack()

        self.output_text_var = tk.StringVar(value="")
        self.output_label = ttk.Label(self, textvariable=self.output_text_var, font=(FONT, 12), wraplength=300,
                                      justify=tk.LEFT)
        self.output_label.pack()

    def _handle_start_button(self):
        if self._ongoing:
            self._ongoing = False
            self.start_button_text_var.set("Start")
        else:

            text_file = self._get_selected_text_file()
            prompt = self.prompt_text_var.get()

            if not text_file:
                tkmessagebox.showerror("Error", "Text file or selection required.")
            elif not prompt:
                tkmessagebox.showerror("Error", "Prompt required.")
            else:
                self._ongoing = True
                self.start_button_text_var.set("Stop")

                self._graph = Graph(text_file, NGRAM_VALUE)
                self.output_text_var.set(prompt)
                self._output_text()

    def _get_selected_text_file(self) -> str:
        text_file = AVAILABLE_TEXT_FILES[self.person_selector_var.get()]

        if not text_file:
            text_file = tkfiledialog.askopenfilename(filetypes=[("Text files", ".txt")])

            if text_file:
                friendly_text_file = os.path.basename(text_file)
                AVAILABLE_TEXT_FILES[friendly_text_file] = text_file
                self.person_selector_var.set(friendly_text_file)
                self.person_selector_combobox.config(values=list(AVAILABLE_TEXT_FILES.keys()))

        return text_file

    def _output_text(self):
        words = self.output_text_var.get().split()
        next_word = self._graph.predict_next_word(tuple(words[-NGRAM_VALUE:]))
        words.append(next_word)

        self.output_text_var.set(" ".join(words))

        if self._ongoing:
            self.after(random.randint(0, 500), self._output_text)


if __name__ == "__main__":

    app = GUIApp()
    app.mainloop()
