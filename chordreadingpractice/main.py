import os
import random
from collections import deque
from sys import platform
from tkinter import IntVar, PhotoImage, StringVar
from typing import Callable, Union

import customtkinter as ctk
import mingus.core.chords as chords
import mingus.core.keys as keys
import mingus.extra.lilypond as lilypond
from mingus.containers import Bar, NoteContainer
from PIL import Image


class IntSpinBox(ctk.CTkFrame):
    def __init__(
        self,
        *args,
        width: int = 100,
        height: int = 32,
        step_size: Union[int, float] = 1,
        command: Callable = None,
        from_: int = 0,
        to: int = 10,
        default_value: int = 0,
        variable: IntVar,
        **kwargs,
    ):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.min, self.max = from_, to
        self.var = variable
        self.default_value = default_value

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(
            self,
            text="-",
            width=height - 6,
            height=height - 6,
            command=self.subtract_button_callback,
        )
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(
            self, width=width - (2 * height), height=height - 6, border_width=0
        )
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = ctk.CTkButton(
            self,
            text="+",
            width=height - 6,
            height=height - 6,
            command=self.add_button_callback,
        )
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, str(self.default_value))

    def add_button_callback(self):

        try:
            value = int(self.entry.get()) + self.step_size
            if value > self.max:
                return
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
            self.var.set(value)
        except ValueError:
            pass
        if self.command is not None:
            self.command()

    def subtract_button_callback(self):
        try:
            value = int(self.entry.get()) - self.step_size
            if value < self.min:
                return
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
            self.var.set(value)

        except ValueError:
            pass
        if self.command is not None:
            self.command()

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))


def setAppearance(new_appearance):
    if new_appearance == "Light":
        ctk.set_appearance_mode("light")
    elif new_appearance == "Dark":
        ctk.set_appearance_mode("dark")
    elif new_appearance == "System":
        ctk.set_appearance_mode("system")


def settings():
    global settings_popup
    try:
        settings_popup.focus_force()
    except:
        settings_popup = ctk.CTkToplevel()
        settings_popup.title("Settings")
        settings_popup.transient(window)
        settings_popup.minsize(200, 200)
        settings_popup.resizable(False, False)

        length_lbl = ctk.CTkLabel(settings_popup, text="Exercise length: ")
        length_sb = IntSpinBox(
            settings_popup,
            from_=MIN_EXERSISE_LENGTH,
            to=MAX_EXERSISE_LENGTH,
            variable=OPTIONS["EXERCISE_LENGTH"],
            default_value=DEFAULT_EXERCISE_LENGTH,
        )
        num_voices_lbl = ctk.CTkLabel(settings_popup, text="Number of voices: ")
        num_voices_sb = ctk.CTkSegmentedButton(
            settings_popup, values=["3", "4"], variable=OPTIONS["NUM_VOICES"]
        )
        # TODO: Dissonance (ie. suspensions)
        theme_lbl = ctk.CTkLabel(settings_popup, text="Application theme: ")
        theme_om = ctk.CTkOptionMenu(
            settings_popup,
            values=["System", "Light", "Dark"]
            if platform == "darwin"
            else ["Light", "Dark"],
            command=setAppearance,
        )

        length_lbl.grid(row=1, column=0, sticky="w", padx=PADX, pady=(10, 0))
        length_sb.grid(row=1, column=1, sticky="ew", padx=PADX, pady=(10, 0))
        num_voices_lbl.grid(row=2, column=0, sticky="w", padx=PADX)
        num_voices_sb.grid(row=2, column=1, sticky="ew", padx=PADX)

        theme_lbl.grid(row=3, column=0, sticky="w", padx=PADX, pady=(25, 0))
        theme_om.grid(row=3, column=1, sticky="ew", padx=PADX, pady=(25, 0))

        settings_popup.mainloop()


def whatsNew():
    global whats_new_popup
    try:
        whats_new_popup.focus_force()
    except:
        whats_new_popup = ctk.CTkToplevel()
        whats_new_popup.title("What's new")
        whats_new_popup.transient(window)
        whats_new_popup.resizable(False, False)

        parent_frame = ctk.CTkFrame(whats_new_popup)
        for i, (head, descr) in enumerate(WHATS_NEW.items()):
            ctk.CTkLabel(
                parent_frame,
                text=f"● {head}",
            ).pack(pady=(5, 0))
            ctk.CTkLabel(
                parent_frame,
                text=f"{descr}",
            ).pack()
            if i < len(WHATS_NEW) - 1:
                ctk.CTkSeparator(parent_frame, orient="horizontal").pack(
                    fill="x", pady=(PADX, 0)
                )
        parent_frame.pack(padx=15, pady=15, ipadx=15)
        whats_new_popup.mainloop()


def generateAndDisplayExercise():
    global imageframe
    exercise_length = OPTIONS["EXERCISE_LENGTH"].get()
    voices_per_chord = int(OPTIONS["NUM_VOICES"].get())
    exercise = list()

    for _ in range(exercise_length):
        chord_mode = random.choice(
            [chords.major_triad, chords.minor_triad, chords.dominant_seventh]
        )
        chord_key = random.choice(keys.major_keys)
        voices = chord_mode(chord_key)
        if len(voices) < voices_per_chord:
            voices.append(voices[0])
        elif len(voices) > voices_per_chord:
            voices.remove(voices[2])
        inversion = 4 - random.randint(0, 4)
        chord = deque(voices)
        chord.rotate(inversion)
        chord = list(chord)
        exercise.append(chord)
        # print(chord, "\t\t", chord_key, chord_mode.__name__)
    notation_string = generateNotationAsLilyPondString(exercise)
    lilypond.to_png(notation_string, "test.png")
    # TODO: Light vs Dark mode images
    loaded_notation_image = loadFormattedImage()
    for child in imageframe.winfo_children():
        child.destroy()
    img_lbl = ctk.CTkLabel(imageframe, text="", image=loaded_notation_image)
    img_lbl.pack(expand=True, fill="both")


def loadFormattedImage():
    img = Image.open("test.png")
    img = img.crop((50, 20, img.size[0] * 0.8, 120))
    return ctk.CTkImage(light_image=img, size=(WIDTH - (PADX * 2), HEIGHT - (PADY * 5)))


def generateNotationAsLilyPondString(chords):
    dur = 4
    b = Bar("C", (len(chords), dur))
    for chord in enumerate(chords):
        nc = NoteContainer(chord[1])
        b.place_notes(nc, dur)
    notation_string = formatNotationString(lilypond.from_Bar(b), len(chords))
    print(notation_string)
    return notation_string


def formatNotationString(notation_string, num_chords):
    indent = 60 - (num_chords * 5)
    return (
        notation_string
        + f"""\layout {{ 
            indent = #{indent} 
            ragged-right = ##t 
            \context {{ 
                \Score 
                \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/32)
                \override SpacingSpanner.common-shortest-duration = #(ly:make-moment 1/32)
            }}
        }}"""
    )


def setup_window():
    window = ctk.CTk()

    window.geometry(f"{WIDTH}x{HEIGHT}")
    window.title("Chord Reading Practice")
    try:
        window.tk.call(
            "wm", "iconphoto", window._w, PhotoImage(file=f"assets{os.sep}icon.png")
        )
    except:
        pass
    window.after(500, window.focus_force)

    topframe = ctk.CTkFrame(
        master=window,
        width=WIDTH - (2 * PADX),
        height=HEIGHT - BTN_FRAME_HEIGHT - (3 * PADY),
    )
    topframe.grid(row=0, column=0, padx=PADX, pady=(PADY, PADY / 2))

    bottomframe = ctk.CTkFrame(
        master=window, width=WIDTH - (2 * PADX), height=BTN_FRAME_HEIGHT
    )
    bottomframe.grid(row=1, column=0, padx=PADX, pady=(PADY / 2, PADY))

    generate_btn = ctk.CTkButton(
        bottomframe, text="Generate new exercise", command=generateAndDisplayExercise
    )
    generate_btn.grid(row=0, column=2, padx=PADX, sticky="nsew")

    settings_btn = ctk.CTkButton(bottomframe, text="Settings", command=settings)
    settings_btn.grid(row=0, column=3, padx=PADX, sticky="nsew")

    whats_new_btn = ctk.CTkButton(bottomframe, text="What's new?", command=whatsNew)
    whats_new_btn.grid(row=0, column=4, padx=PADX, sticky="nsew")

    return topframe, window


if __name__ == "__main__":
    __version__ = "v0.1.5"

    WHATS_NEW = {
        "Fixed spacing issues": "Added more spacing between notes for better readability",
    }

    try:
        from application_update import execute_update

        if execute_update(
            "chordreadingpractice", __version__, os.path.basename(__file__)
        ):
            exit()

    except ModuleNotFoundError:
        pass

    WIDTH, HEIGHT = (1400, 500)
    PADX, PADY = 10, 20
    BTN_FRAME_HEIGHT = 40

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")

    imageframe, window = setup_window()

    MIN_EXERSISE_LENGTH, MAX_EXERSISE_LENGTH = 4, 12
    DEFAULT_EXERCISE_LENGTH = 8

    OPTIONS = dict(
        EXERCISE_LENGTH=IntVar(value=DEFAULT_EXERCISE_LENGTH),
        NUM_VOICES=StringVar(value="4"),
    )

    window.mainloop()
