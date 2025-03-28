"""
CSC111 Project 2

CelebrityBot
"""

import os
import random

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as tkfiledialog
from tkinter import messagebox as tkmessagebox
from tkinter import simpledialog as tksimpledialog

import pyperclip

from graph import Graph
from visualization import visualize_graph_plotly


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

    # GUI elements
    generation_info: tuple[tk.StringVar, tk.StringVar]
    person_selector_combobox: ttk.Combobox
    prompt_text_var: tk.StringVar
    start_button_text_var: tk.StringVar
    copy_button: ttk.Button

    # Private Attributes:
    #     - _ongoing: whether the program is currently outputting text
    #     - _graph: the text generation's graph
    _ongoing: bool
    _graph: Graph

    def __init__(self) -> None:
        """Initialize the program, create a graph."""
        super().__init__()

        self.title("CelebrityBot")
        self.geometry("400x400")

        self._graph = Graph()  # created in parse text method
        self._ongoing = False

        self._draw()

    def _draw(self) -> None:
        """
        Draw the elements onto the screen.
        """

        self.generation_info = (tk.StringVar(), tk.StringVar())  # stores (person text file, prompt)

        # Title
        ttk.Label(self, text="CelebrityBot", font=(FONT, 30)).pack()

        # Dropdown
        ttk.Label(self, text="Select a person:", font=(FONT, 12)).pack()

        self.person_selector_combobox = ttk.Combobox(self, width=30, state="readonly",
                                                     textvariable=self.generation_info[0],
                                                     values=list(AVAILABLE_TEXT_FILES.keys()))
        self.person_selector_combobox.current(0)
        self.person_selector_combobox.pack()

        # Prompt
        ttk.Label(self, text="Initial prompt:", font=(FONT, 12)).pack()

        self.prompt_text_var = tk.StringVar()
        ttk.Entry(self, width=30, textvariable=self.prompt_text_var).pack()

        # Buttons (start, visualize, copy)
        self.start_button_text_var = tk.StringVar(value="Start")
        ttk.Button(self, textvariable=self.start_button_text_var, command=self._handle_start_button).pack()

        ttk.Button(self, text="Visualize graph", command=self._visualize_graph).pack()

        self.copy_button = ttk.Button(self, text="Copy output", command=self._copy_output)

        # Output
        ttk.Label(self, textvariable=self.generation_info[1], font=(FONT, 12), wraplength=300, justify=tk.LEFT).pack()

    def _handle_start_button(self) -> None:
        """
        Start generating output. Toggles self._ongoing boolean.

        Ensures all fields are filled out properly (text file, prompt).

        Creates new graph, if using new text file.
        """
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
                self.copy_button.pack()

                if not self._graph or self._graph.file_name != text_file:
                    self._graph = Graph(text_file, NGRAM_VALUE)
                self.generation_info[1].set(prompt)
                self._output_text()

    def _get_selected_text_file(self) -> str:
        """Return the selected text file, based on the user selection and file dialog (if custom file selected)."""
        text_file = AVAILABLE_TEXT_FILES[self.generation_info[0].get()]

        if not text_file:
            text_file = tkfiledialog.askopenfilename(filetypes=[("Text files", ".txt")])

            if text_file:
                friendly_text_file = os.path.basename(text_file)
                AVAILABLE_TEXT_FILES[friendly_text_file] = text_file
                self.generation_info[0].set(friendly_text_file)
                self.person_selector_combobox.config(values=list(AVAILABLE_TEXT_FILES.keys()))

        return text_file

    def _output_text(self) -> None:
        """
        Call the graph's generate text method based on existing words, and output text.
        Calls itself repeatedly.

        Precondition:
            - graph is not None
        """
        words = self.generation_info[1].get().split()
        next_word = self._graph.predict_next_word(tuple(words[-NGRAM_VALUE:]))
        words.append(next_word)

        self.generation_info[1].set(" ".join(words))

        if self._ongoing:
            self.after(random.randint(0, 500), self._output_text)

    def _copy_output(self) -> None:
        """Copy the text output."""
        output = self.generation_info[1].get()
        pyperclip.copy(output)

    def _visualize_graph(self) -> None:
        """Visualize graph, on button press."""
        tkmessagebox.showinfo("Visualization", "The visualizer will pick a word at random based on your "
                              "selected person, and show a portion of the graph.")

        graph_to_visualize_text_file = self._get_selected_text_file()
        graph_to_visualize = Graph(graph_to_visualize_text_file, 3)

        number = tksimpledialog.askinteger("Enter number", "Select number of vertices to display",
                                           minvalue=1, maxvalue=len(graph_to_visualize.vertices))

        if not graph_to_visualize_text_file:
            tkmessagebox.showerror("Error", "Text file or selection required.")
        elif number and graph_to_visualize_text_file:
            visualize_graph_plotly(graph_to_visualize, number)


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['os', 'random', 'tkinter', 'pyperclip', 'graph', 'visualization'],
        'max-line-length': 120
    })

    app = GUIApp()
    app.mainloop()
