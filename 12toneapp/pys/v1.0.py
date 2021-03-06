#!usr/bin/env python3
from functools import partial
from os import listdir
from random import shuffle
from sys import argv
from tkinter import Entry, Frame, Label, Tk, font
from tkinter.messagebox import showerror
from tkinter.ttk import Button

import numpy as np


def create_prime():
    prime = list(range(len(PITCHES)))
    shuffle(prime)
    return [PITCHES[k] for k in prime], prime


def generate_inversion(tones: list):
    diffs = map(lambda p: (p - tones[0]) % 12, tones)
    inversion = map(lambda p: (tones[0] - p), diffs)
    return [PITCHES[k] for k in inversion]


def generate_matrix(prime: list, tones: list):
    inversion = generate_inversion(tones)
    matrix = [[str() for _ in range(12)] for _ in range(12)]

    for row in (prime, inversion):
        matrix[0] = row
        matrix = np.swapaxes(np.array(matrix, dtype=str), 0, 1).tolist()

    intervals = [(p - tones[0]) % 12 for p in tones]
    for row_num in range(1, len(matrix)):
        home_tone = PITCHES.index(matrix[row_num][0])
        matrix[row_num] = [PITCHES[(home_tone + i) % 12] for i in intervals]
    return matrix


def create_matrix(prime_row: list = None):
    prime, tones = (
        create_prime()
        if prime_row is None
        else (prime_row, [PITCHES.index(p) for p in prime_row])
    )
    matrix = generate_matrix(prime, tones)
    return matrix


def display_matrix(matrix: list):
    global mainframe, load_inpt
    mainframe = Frame(root, bg=BACKGROUND)
    mainframe.pack()
    LargeLabel = partial(Label, mainframe, font=(FONT, 24))
    SmallLabel = partial(Label, mainframe, font=(FONT, 18), bg=BACKGROUND)
    _Button = partial(Button, mainframe)

    xoff, yoff = (2, 2)
    for row_num, row in enumerate(matrix):
        for col_num, cell in enumerate(row):
            lbl = LargeLabel(text=cell, borderwidth=2, relief="groove")
            lbl.grid(row=row_num + yoff, column=col_num + xoff, sticky="nsew")

    # Add the standard 0 labels (which do not change no matter what order the matrix is in)
    SmallLabel(text="P 0").grid(row=xoff, column=yoff - 1, sticky="nsew")
    SmallLabel(text="I 0").grid(row=xoff - 1, column=yoff, sticky="nsew")
    SmallLabel(text="R 0").grid(row=xoff, column=12 + yoff, sticky="nsew")
    SmallLabel(text="RI 0").grid(row=12 + xoff, column=yoff, sticky="nsew")

    # Iterate over the matrix and find the row labels for the rest of the column / row
    normal = matrix[0][0]
    #   prime and retrograde labels
    for r, note in enumerate(np.array(matrix)[1:, 0]):
        interval = (PITCHES.index(note) - PITCHES.index(normal)) % 12
        prime_lbl = SmallLabel(text=f"P {interval}")
        retrograde_lbl = SmallLabel(text=f"R {interval}")
        prime_lbl.grid(row=r + 1 + xoff, column=yoff - 1, sticky="nsew")
        retrograde_lbl.grid(row=r + 1 + xoff, column=12 + yoff, sticky="nsew")

    #   inversion and retrograde inversion labels
    for c, note in enumerate(matrix[0][1:]):
        interval = (PITCHES.index(note) - PITCHES.index(normal)) % 12
        inversion_lbl = SmallLabel(text=f"I {interval}")
        retrograde_inversion_lbl = SmallLabel(text=f"RI {interval}")
        inversion_lbl.grid(row=xoff - 1, column=c + 1 + yoff, sticky="nsew")
        retrograde_inversion_lbl.grid(row=12 + xoff, column=c + 1 + yoff, sticky="nsew")

    # Add new matrix, save and load matrix buttons, and load matrix entry box
    new_btn = _Button(text="Generate new random matrix", command=refresh)
    new_btn.grid(row=yoff + 15, column=2, columnspan=yoff + 10, sticky="ew")
    save_btn = _Button(text="Save matrix", command=lambda: save_matrix(matrix))
    save_btn.grid(row=yoff + 16, column=2, columnspan=yoff + 10, sticky="ew")
    load_inpt = Entry(mainframe)
    load_inpt.insert(0, "Enter prime row to load here...")
    load_inpt.grid(row=yoff + 17, column=2, columnspan=yoff + 10, sticky="ew")
    load_btn = _Button(text="Load matrix from prime row", command=load_matrix)
    load_btn.grid(row=yoff + 18, column=2, columnspan=yoff + 10, sticky="ew")

    col_count, row_count = root.grid_size()
    for col in range(col_count):
        mainframe.grid_columnconfigure(col, minsize=20)
    for row in range(row_count):
        mainframe.grid_rowconfigure(row, minsize=20)


def get_enharmonic(pitch: str):
    enharms = {
        "A#": "Bb",
        "Cb": "B",
        "B#": "C",
        "C#": "Db",
        "D#": "Eb",
        "Fb": "E",
        "E#": "F",
        "F#": "Gb",
        "G#": "Ab",
    }
    return enharms[pitch] if pitch in enharms.keys() else pitch


def load_matrix():
    try:
        row = load_inpt.get().replace("\xa0", " ").split(" ")
        row = [get_enharmonic(p) for p in row]
        if len(set(row)) != 12:
            raise Exception("Prime row must contain excatly one instance of each pitch")
        elif not all([p in PITCHES for p in row]):
            raise Exception(
                """Prime row contains invalid note names, 
                sharps should be indicated by '#' and flats by 'b'"""
            )
        refresh(row)
    except Exception as e:
        showerror("Error loading matrix", str(e))


def save_matrix(matrix: list):
    if "matrices.txt" not in listdir():
        with open("matrices.txt", "w"):
            pass
    with open("matrices.txt", "a") as matrix_file:
        matrix_file.write(" ".join(matrix[0]) + "\n")


def refresh(prime: list = None):
    global mainframe
    try:
        mainframe.destroy()
    except:
        pass
    if prime is None:
        matrix = create_matrix()
    else:
        try:
            matrix = create_matrix(prime)
        except Exception as e:
            print("Could not load given prime... Generating new random prime")
            matrix = create_matrix()
    display_matrix(matrix)


if __name__ == "__main__":
    root = Tk()
    given = argv[1:] if len(argv) > 1 else None
    FONT = "Verdana" if "Verdana" in font.families() else None
    BACKGROUND = "#aaaaaa"
    PITCHES = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab"]
    root.title("12-tone matrix generator")
    root.resizable(False, False)
    refresh(given)
    root.mainloop()
