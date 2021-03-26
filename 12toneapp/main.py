#!usr/bin/env python37
from functools import partial
from os import listdir, mkdir, path, sep
from random import choice, shuffle
from sys import argv, platform
from tkinter import *
from tkinter import (Entry, Frame, Label, StringVar, Tk, Toplevel, filedialog,
                     font)
from tkinter.messagebox import showerror, showinfo
from tkinter.ttk import Button, Label, LabelFrame, OptionMenu, Style

import numpy as np

if platform == "win32":
    import threading
    from time import sleep
    from winsound import Beep as playtone


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


def display_matrix(matrix: list):
    global mainframe
    mainframe = Frame(root, bg=BACKGROUND)
    mainframe.pack()
    LargeLabel = partial(Label, mainframe, font=(FONT, 24))
    if platform == "win32":
        SmallButton = partial(Button, mainframe)
    else:
        SmallLabel = partial(Label, mainframe, font=(FONT, 18))
    _Button = partial(Button, mainframe)

    xoff, yoff = (2, 2)
    for row_num, row in enumerate(matrix):
        for col_num, cell in enumerate(row):
            lbl = LargeLabel(text=cell, borderwidth=2, relief="groove")
            lbl.grid(row=row_num + yoff, column=col_num + xoff, sticky="nsew")

    if platform == "win32":
        SmallButton(text="P 0", command=lambda: play_row('p-0')).grid(
            row=xoff, column=yoff - 1, sticky="nsew")
        SmallButton(text="I 0", command=lambda: play_row('i-0')).grid(
            row=xoff - 1, column=yoff, sticky="nsew")
        SmallButton(text="R 0", command=lambda: play_row('r-0')).grid(
            row=xoff, column=12 + yoff, sticky="nsew")
        SmallButton(text="RI 0", command=lambda: play_row('ri-0')).grid(
            row=12 + xoff, column=yoff, sticky="nsew")
    else:
        SmallLabel(text="P 0").grid(row=xoff, column=yoff - 1, sticky="nsew")
        SmallLabel(text="I 0").grid(row=xoff - 1, column=yoff, sticky="nsew")
        SmallLabel(text="R 0").grid(row=xoff, column=12 + yoff, sticky="nsew")
        SmallLabel(text="RI 0").grid(row=12 + xoff, column=yoff, sticky="nsew")

    normal = matrix[0][0]
    for r, note in enumerate(np.array(matrix)[1:, 0]):
        interval = (PITCHES.index(note) - PITCHES.index(normal)) % 12
        if platform == "win32":
            prime_lbl = SmallButton(
                text=f"P {interval}", command=partial(play_row, f"p-{r+1}"))
            retrograde_lbl = SmallButton(
                text=f"R {interval}", command=partial(play_row, f"r-{r+1}"))
        else:
            prime_lbl = SmallLabel(text=f"P {interval}")
            retrograde_lbl = SmallLabel(text=f"R {interval}")
        prime_lbl.grid(row=r + 1 + xoff, column=yoff - 1, sticky="nsew")
        retrograde_lbl.grid(row=r + 1 + xoff, column=12 + yoff, sticky="nsew")

    for c, note in enumerate(matrix[0][1:]):
        interval = (PITCHES.index(note) - PITCHES.index(normal)) % 12
        if platform == "win32":
            inversion_lbl = SmallButton(
                text=f"I {interval}", command=partial(play_row, f"i-{c+1}"))
            retrograde_inversion_lbl = SmallButton(
                text=f"RI {interval}", command=partial(play_row, f"ri-{c+1}"))
        else:
            inversion_lbl = SmallLabel(text=f"I {interval}")
            retrograde_inversion_lbl = SmallLabel(text=f"RI {interval}")
        inversion_lbl.grid(row=xoff - 1, column=c + 1 + yoff, sticky="nsew")
        retrograde_inversion_lbl.grid(
            row=12 + xoff, column=c + 1 + yoff, sticky="nsew")

    xspan, fs, ls = 6, 2, 8
    LargeLabel(text='').grid(row=yoff + 14, column=fs,
                             columnspan=xspan*2, sticky="ew")
    new_btn = _Button(text="Generate new random matrix", command=refresh)
    new_btn.grid(row=yoff + 15, column=ls, columnspan=xspan, sticky="ew")

    load_btn = _Button(text="Load saved matrix", command=load_matrix)
    load_btn.grid(row=yoff + 16, column=fs, columnspan=xspan, sticky="ew")

    inpt_btn = _Button(text="Input prime row", command=get_prime)
    inpt_btn.grid(row=yoff + 15, column=fs, columnspan=xspan, sticky="ew")

    save_btn = _Button(text="Save matrix", command=lambda: save_matrix(matrix))
    save_btn.grid(row=yoff + 16, column=ls, columnspan=xspan, sticky="ew")

    settings_btn = _Button(text="Options", command=settings)
    settings_btn.grid(row=yoff + 17, column=fs,
                      columnspan=xspan*2, sticky="ew")

    col_count, row_count = root.grid_size()
    for col in range(col_count):
        mainframe.grid_columnconfigure(col, minsize=20)
    for row in range(row_count):
        mainframe.grid_rowconfigure(row, minsize=20)


def create_matrix(prime_row: list = None):
    if prime_row is None:
        prime, tones = create_prime()
    else:
        prime = [get_enharmonic(p) for p in prime_row]
        tones = [PITCHES.index(k) for k in prime]
    matrix = generate_matrix(prime, tones)
    return matrix


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


def get_prime():
    popup = Toplevel(root)
    popup.geometry("400x150")
    popup.title("Enter prime row")
    lbl0 = Label(
        popup,
        text="Enter the note values for the prime row separated by spaces"
    )
    lbl1 = Label(popup, text="(eg. 'E F G Db Gb Eb Ab D B C A Bb')")
    error_msg = StringVar()
    err_lbl = Label(popup, textvariable=error_msg, fg='#ee4444')
    prime_entry = Entry(popup, width=50)

    def callback():
        try:
            row = prime_entry.get().split(" ")
            if len(set(row)) != 12:
                raise Exception(
                    "Row must contain exactly one instance of each pitch")
            popup.destroy()
            refresh(row)
        except Exception as e:
            error_msg.set(str(e))

    ent_btn = Button(popup, text="Generate matrix", command=callback, width=50)
    lbl0.pack(pady=(20, 0))
    lbl1.pack()
    prime_entry.pack(pady=(0, 5))
    ent_btn.pack()
    err_lbl.pack(anchor="s")
    popup.mainloop()
    

def play_row(a):
    global play_row_thread
    t, n = a.split('-')
    n = int(n)
    if t == 'p':
        notes = matrix[n]
    elif t == 'i':
        notes = [matrix[k][n] for k in range(len(PITCHES))]
    elif t == 'r':
        notes = matrix[n][::-1]
    elif t == 'ri':
        notes = [matrix[k][n] for k in range(len(PITCHES)-1, -1, -1)]
    freqs_to_play = [FREQUENCY_DICT[p] for p in notes]
    RESET = True
    play_row_thread = threading.Thread(
        target=play_freqs, args=(freqs_to_play,), daemon=True)
    play_row_thread.start()


def play_freqs(freqs):
    global RESET
    pause, RESET = .3, False
    basefreq = dict(zip(BASE_FREQS, [220, 440, None]))[OPTIONS['BASE_FREQ'].get()]
    bfr = basefreq
    for freq in freqs:
        if RESET:
            RESET = False
            return
        if basefreq is None:
            bfr = choice([220, 440])
        playtone(int(bfr*freq), 750)
        sleep(pause)


def load_matrix():
    filename = filedialog.askopenfilename(
        initialdir="matrices",
        title="Select file",
        filetypes=(("matrix files", "*.matrix"), ("all files", "*.*")),
    )
    if not filename:
        return
    with open(filename, "r") as matr_file:
        prime_row = matr_file.readline().replace("\n", "")
    refresh(prime_row.split(" "))


def save_matrix(matrix: list):
    if "matrices" not in listdir():
        mkdir("matrices")
    with open(f"matrices{sep}{'-'.join(matrix[0])}.matrix", "w") as matr_file:
        matr_file.writelines([f"{' '.join(line)}\n" for line in matrix])


def settings():
    global settings_popup
    try: settings_popup.destroy()
    except: pass
    settings_styles = Style()
    settings_styles.configure(
        "SettingsLabelframe.TLabelframe.Label", font=("Verdana", 18, "normal"))
    settings_styles.configure(
        "SettingsLabelframe.TLabelframe.Label", foreground=COLORS['TEXTCOLOR'])

    settings_popup = Toplevel()
    settings_popup.title("Settings")
    settings_popup.transient(root)
    settings_popup.resizable(False, False)

    other_frame = LabelFrame(settings_popup, text="Settings", style="SettingsLabelframe.TLabelframe")
    basefreq_lbl = Label(other_frame, text="Octave")
    basefreq_om = OptionMenu(other_frame, OPTIONS['BASE_FREQ'], BASE_FREQS[-1], *BASE_FREQS)
    

    basefreq_lbl.grid(row=0, column=0, padx=5)
    basefreq_om.grid(row=0, column=1, padx=5)
    other_frame.pack(padx=15, pady=15, ipadx=5, ipady=5)

    settings_popup.mainloop()


def refresh(prime: list = None):
    global mainframe, matrix, RESET
    RESET = True
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
    __version__ = "v1.6.2"
    
    try:
        from application_update import execute_update
        if execute_update('12toneapp', __version__, path.basename(__file__)):
            exit()

    except ModuleNotFoundError:
        pass
        
    root = Tk()
    given = argv[1:] if len(argv) > 1 else None
    RESET = False
    FONT = "Verdana" if "Verdana" in font.families() else None
    BACKGROUND = "#eeeeee" if platform == "win32" else None
    PITCHES = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab"]
    FREQUENCY_DICT = dict(zip(PITCHES, [(2**(i/12)) for i in range(len(PITCHES))]))

    BASE_FREQS = ['A3-A4', 'A4-A5', 'Spread (A3-A5)']
    OPTIONS = dict(
        BASE_FREQ = StringVar(value=BASE_FREQS[-1])
    )

    if platform in ["win32", 'linux']:
        COLORS = {
            "WINDOW_BACKGROUND": '#cccccc',
            "TEXTCOLOR": 'black'
        }
    elif platform == "darwin":
        COLORS = {
            "WINDOW_BACKGROUND": 'systemWindowBackgroundColor',
            "TEXTCOLOR": 'systemTextColor'
        }

    root.title(f"12-tone matrix generator {__version__}")
    root.resizable(False, False)
    root.tk.call('wm', 'iconphoto', root._w,
                 PhotoImage(file=f'assets{sep}icon.png'))
    root.after(500, root.focus_force)
    refresh(given)
    root.mainloop()
