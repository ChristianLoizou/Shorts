#!usr/bin/env python3
import os
import random
import threading
import turtle
from math import acos, degrees, hypot
from numpy import abs, int16, linspace, max, pi, sin
from simpleaudio import play_buffer
from sys import exit, platform
from time import sleep
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import (Button, Checkbutton, Label, LabelFrame, OptionMenu,
                         Separator, Spinbox, Style)


class Interval:
    def __init__(self, interval_string, direction):
        self.interval = interval_string
        self.direction = direction
        self.value = self.get_value()
        self.semitones = SEMITONES[self.interval] * self.direction

    def __str__(self):
        return self.interval.replace("8th", "Octave")

    def __repr__(self):
        return self.interval.replace("8th", "Octave")

    def get_value(self):
        return (INTERVALS.index(self.interval)+1) * self.direction

    def get_dy(self):
        return self.value * MAX_DY // MAX_INTERVAL


def get_activated_intervals():
    return [interval for (interval, value) in OPTIONS['INTERVALS_ACTIVATED'].items() if value.get() == 1]


def generate_exercise():
    activated_intervals = get_activated_intervals()
    if activated_intervals == list():
        return
    num_intervals = int(OPTIONS['EXERCISE_LENGTH'].get())
    intervals = list()
    for _ in range(num_intervals):
        ni = random.choice(activated_intervals)
        if intervals:
            adjacent, repeated = intervals[-1] == ni, ni in intervals
            allowing_repetitions = OPTIONS['ALLOW_REPETITIONS'].get() == 1
            while adjacent or (not allowing_repetitions and repeated):
                ni = random.choice(activated_intervals)
                adjacent, repeated = intervals[-1] == ni, ni in intervals
                allowing_repetitions = OPTIONS['ALLOW_REPETITIONS'].get() == 1
        intervals.append(ni)

    directions = random.choices([-1, 1], k=num_intervals)
    exercise = [Interval(ex, dr) for (ex, dr) in zip(intervals, directions)]
    return exercise


def setup_window():
    global play_btn
    root = Tk()
    root.title(f"Interval Practice {__version__}")
    root.resizable(False, False)
    try:
        root.tk.call('wm', 'iconphoto', root._w,
                     PhotoImage(file=f'assets{os.sep}icon.png'))
    except:
        pass
    root.after(500, root.focus_force)

    canvas = Canvas(root, width=WIDTH, height=HEIGHT)
    btn_canvas = Canvas(root, width=WIDTH, height=75)
    new_btn = Button(btn_canvas, text="Generate new exercise",
                     command=rerun_application)
    play_btn = Button(btn_canvas, text="Play exercise",
                      command=play_exercise, state="disabled")
    play_home_tone_btn = Button(
        btn_canvas, text="Play starting note", command=play_home_tone)
    settings_btn = Button(btn_canvas, text="Settings", command=settings)
    whats_new_btn = Button(btn_canvas, text="What's new?", command=whats_new)

    canvas.grid(row=0, column=0)
    btn_canvas.grid(row=1, column=0)
    new_btn.grid(row=0, column=0, sticky='nsew')
    play_btn.grid(row=0, column=1, sticky='nsew')
    play_home_tone_btn.grid(row=0, column=2, sticky='nsew')
    settings_btn.grid(row=0, column=3, sticky='nsew')
    whats_new_btn.grid(row=0, column=4, sticky='nsew')

    root.bind('<ButtonPress-1>', mousePressed)

    return root, canvas, turtle.TurtleScreen(canvas)


def create_new_turtle(canvas):
    turt = turtle.RawTurtle(canvas)
    turt.speed(10)
    turt.penup()
    turt.shape("circle")
    turt.hideturtle()
    turt.turtlesize(*TURTLESIZE)
    for _ in range(2):
        turt.penup()
        turt.pendown()
    return turt


def reset_turtle(turt, x=None, y=None):
    canvas.delete("all")
    turt.speed(10)
    turt.pencolor('black')
    turt.setposition(x if x else 0, y if y else 0)


def draw_exercise(exercise, canvas):
    global play_btn, stamp_positions
    play_btn.config(state="enabled")

    ox = -(WIDTH-XPAD)//2
    cx = ox
    dx = (WIDTH - (XPAD)) // (len(exercise)*2)
    stamp_positions = list()
    reset_turtle(turt, cx)
    turt.stamp()
    turt.pendown()
    turt.pensize(2)
    turt.setpos(-ox, 0)
    turt.setpos(ox, 0)
    turt.pensize(1)
    if OPTIONS['SHOW_GUIDELINES'].get():
        screen.tracer(0, 0)
        turt.penup()
        turt.speed(-1)
        ys = set([Interval(interval, ym).get_dy()
                 for interval in INTERVALS for ym in [-1, 1]])
        _turtles = list()
        for y in sorted(list(ys)):
            for x in range(-52, 52, 2):
                nt = create_new_turtle(screen)
                nt.penup()
                nt.pencolor('#aaaaaa')
                nt.setpos(x * ((2*-ox)//100), y)
                nt.pendown()
                _turtles.append(nt)
        for t in _turtles:
            t.forward((3*-ox)//100)
        del _turtles
        screen.update()
        screen.tracer(1, 5)

    for interval in exercise:
        nx, ny = cx + dx, interval.get_dy()
        lx, cx = cx, nx + dx
        txtangle = degrees(acos(dx/hypot(dx, ny))) * (ny/abs(ny))
        t = canvas.create_text(
            lx + (dx//2), -ny//2, text=str(interval), angle=txtangle, fill='black')
        bb = canvas.create_rectangle(canvas.bbox(t), fill='white', width=0)
        canvas.tag_lower(bb, t)

        for k, pos in enumerate([(nx, ny), (cx, 0)]):
            if k:
                turt.pendown()
            else:
                turt.penup()
                stamp_positions.append(pos)
            turt.setposition(*pos)
            turt.stamp()


def play_exercise():
    notes_to_play, home_idx = [HOME_NOTE], PITCHES.index(HOME_NOTE)

    for interval in exercise:
        new_note = PITCHES[home_idx + interval.semitones]
        notes_to_play.append(new_note)
        notes_to_play.append(HOME_NOTE)

    freqs_to_play = [FREQUENCY_DICT[p] for p in notes_to_play]
    play_thread = threading.Thread(
        target=play_notes, args=(freqs_to_play,), daemon=True)
    play_thread.start()


def play_home_tone():
    play_thread = threading.Thread(target=play_freqs, args=(
        FREQUENCY_DICT[HOME_NOTE], TONE_DURATION), daemon=True)
    play_thread.start()


def play_notes(notes):
    pause = [.6, .2, .005][int(OPTIONS['PLAYBACK_SPEED'].get())-1]
    if int(OPTIONS['SIMULTANEOUS_PLAYBACK'].get()):
        pairs = [(notes[i], notes[i+1]) for i in range(0, len(notes)-1, 2)]
        for pair in pairs:
            play_freqs(*pair, duration=TONE_DURATION)
            sleep(pause)
    else:
        for freq in notes:
            play_freqs(freq, duration=TONE_DURATION)
            sleep(pause)


def play_freqs(*freqs, duration=1):
    sr = 44100
    t = linspace(0, duration, duration * sr, False)

    notes = [sin(freq * t * 2 * pi) for freq in freqs]
    audios = [(note * (2**15 - 1) / max(abs(note))) for note in notes]
    audios = [audio.astype(int16) for audio in audios]
    for audio in audios:
        play_obj = play_buffer(audio, 1, 2, sr)
    play_obj.wait_done()


def rerun_application():
    global exercise
    exercise = generate_exercise()
    if exercise is not None:
        draw_exercise(exercise, canvas)
    else:
        messagebox.showerror("Could not create exercise",
                             "No intervals have been selected to test. Please select at least one interval in the 'intervals' menu and try again")


def update_starting_note(_=None):
    global HOME_NOTE, OPTIONS
    HOME_NOTE = f"{OPTIONS['HOME_NOTE_VARIABLE'].get()}5"


def settings():
    global settings_popup
    try:
        settings_popup.focus_force()
    except:
        settings_popup = Toplevel()
        settings_popup.title("Settings")
        settings_popup.transient(window)
        settings_popup.resizable(False, False)

        settings_styles = Style()
        settings_styles.configure(
            "SettingsLabelframe.TLabelframe.Label", font=("Verdana", 18, "normal"))
        settings_styles.configure(
            "SettingsLabelframe.TLabelframe.Label", foreground=COLORS['TEXTCOLOR'])

        interval_frame = LabelFrame(
            settings_popup, text="Intervals to test", style="SettingsLabelframe.TLabelframe")
        for idx, (setting, value) in enumerate(OPTIONS['INTERVALS_ACTIVATED'].items()):
            cb = Checkbutton(interval_frame, text=str(Interval(
                setting, 1)), variable=value, style="SettingsCheckbutton.TCheckbutton")
            cb.grid(row=(idx//2)+1, column=(idx % 2)+1, sticky='nsew')
        interval_frame.pack(fill='both', expand=True,
                            padx=15, pady=15, ipadx=5, ipady=5)

        other_frame = LabelFrame(
            settings_popup, text="General settings", style="SettingsLabelframe.TLabelframe")
        homenote_lbl = Label(other_frame, text="Starting note: ")
        homenote_om = OptionMenu(
            other_frame, OPTIONS['HOME_NOTE_VARIABLE'], NOTE_NAMES[0], *NOTE_NAMES, command=update_starting_note)
        length_lbl = Label(other_frame, text="Exercise length: ")
        length_sb = Spinbox(other_frame, from_=3, to=10,
                            textvariable=OPTIONS['EXERCISE_LENGTH'], state="readonly", width=5)
        playbackspeed_lbl = Label(other_frame, text="Playback speed: ")
        playbackspeed_sb = Spinbox(
            other_frame, from_=1, to=3, textvariable=OPTIONS['PLAYBACK_SPEED'], state="readonly", width=5)
        allowrepetitions_cb = Checkbutton(other_frame, text="Allow repetitions",
                                          variable=OPTIONS['ALLOW_REPETITIONS'], style="SettingsCheckbutton.TCheckbutton")
        showguidelines_cb = Checkbutton(other_frame, text="Show semitone guidelines\n(Applied on redraw)",
                                        variable=OPTIONS['SHOW_GUIDELINES'], style="SettingsCheckbutton.TCheckbutton")
        simultaneousplayback_cb = Checkbutton(
            other_frame, text="Simultaneous playback", variable=OPTIONS['SIMULTANEOUS_PLAYBACK'],
            style="SettingsCheckbutton.TCheckbutton")

        homenote_lbl.grid(row=0, column=0, sticky='w', padx=15)
        homenote_om.grid(row=0, column=1, sticky='e')
        length_lbl.grid(row=1, column=0, sticky='w', padx=15)
        length_sb.grid(row=1, column=1, sticky='e')
        playbackspeed_lbl.grid(row=2, column=0, sticky='w', padx=15)
        playbackspeed_sb.grid(row=2, column=1, sticky='e')
        allowrepetitions_cb.grid(
            row=3, column=0, columnspan=2, sticky='w', padx=15)
        showguidelines_cb.grid(
            row=4, column=0, columnspan=2, sticky='w', padx=15)
        simultaneousplayback_cb.grid(
            row=5, column=0, columnspan=2, sticky='w', padx=15)
        other_frame.pack(fill='both', expand=True, padx=15,
                         pady=15, ipadx=5, ipady=5)

        settings_popup.mainloop()


def whats_new():
    global whats_new_popup
    try:
        whats_new_popup.focus_force()
    except:
        whats_new_popup = Toplevel()
        whats_new_popup.title("Settings")
        whats_new_popup.transient(window)
        whats_new_popup.resizable(False, False)

        whats_new_styles = Style()
        whats_new_styles.configure(
            "WhatsNewLabelframe.TLabelframe.Label",
            font=("Verdana", 18, "normal"),
            foreground=COLORS['TEXTCOLOR'])
        whats_new_styles.configure(
            "WhatsNewHeadLabel.TLabel", font=("Verdana", "14", "normal"), anchor='w')
        whats_new_styles.configure(
            "WhatsNewDescrLabel.TLabel", font=("Verdana", "12", "italic"), anchor='w', wraplength=270)

        lf = LabelFrame(whats_new_popup, text="What's new?",
                        style="WhatsNewLabelframe.TLabelframe")
        for i, (head, descr) in enumerate(WHATS_NEW.items()):
            Label(lf, text=f"● {head}",
                  style="WhatsNewHeadLabel.TLabel").pack(pady=(5, 0))
            Label(lf, text=f"{descr}",
                  style="WhatsNewDescrLabel.TLabel").pack()
            if i < len(WHATS_NEW)-1:
                Separator(lf, orient='horizontal').pack(fill='x', pady=(5, 0))
        lf.pack(padx=15, pady=15, ipadx=15)
        whats_new_popup.mainloop()


def mousePressed(event):
    global exercise, stamp_positions
    try:
        x, y = event.x - WIDTH/2 - 4, - (event.y - HEIGHT/2 - 4)
        for pos in stamp_positions:
            if abs(x-pos[0]) < 5 and abs(y-pos[1]) < 5:
                idx = stamp_positions.index(pos)
                interval = exercise[idx]
                break
        home_note = PITCHES.index(HOME_NOTE)
        home_pitch, interval_pitch = PITCHES[home_note], PITCHES[home_note +
                                                                 interval.semitones]
        home_frequency, interval_frequency = FREQUENCY_DICT[home_pitch], FREQUENCY_DICT[interval_pitch]
        play_freqs(home_frequency, interval_frequency)
    except NameError:
        pass


if __name__ == "__main__":

    __version__ = "v1.6.6"

    WHATS_NEW = {
        'Added this \"What\'s new?\" section': "This section will contain all the updates from the current version",
        'Added click-to-play functionality': "You can now click on an interval to play it alone."
    }

    try:
        from application_update import execute_update
        if execute_update('intervalpractice', __version__, os.path.basename(__file__)):
            exit()

    except ModuleNotFoundError:
        pass

    if platform in ["win32", 'linux']:
        COLORS = {
            "WINDOW_BACKGROUND": '#cccccc',
            "TEXTCOLOR": 'black'
        }
    elif platform == "darwin":
        COLORS = {
            "WINDOW_BACKGROUND": 'systemWindowBackgroundColor',
            "TEXTCOLOR": '#333333'
        }

    WIDTH, HEIGHT = (1200, 500)
    XPAD = 50
    MAX_INTERVAL = 8
    MAX_DY = HEIGHT // 4
    TURTLESIZE = (.4, .4)

    HOME_NOTE = "C5"
    TONE_DURATION = 1

    MAX_EXERSISE_LENGTH = 8
    MIN_EXERSISE_LENGTH = 3

    INTERVAL_DESCRIPTORS = {
        2: ('nd', ['Minor', 'Major']),
        3: ('rd', ['Minor', 'Major']),
        4: ('th', ['Perfect', ]),
        5: ('th', ['Diminished', 'Perfect']),
        6: ('th', ['Minor', 'Major']),
        7: ('th', ['Minor', 'Major']),
        8: ('th', ['Perfect'])
    }

    INTERVALS = [f"{t} {a}{b[0]}" for (
        a, b) in INTERVAL_DESCRIPTORS.items() for t in b[1]]
    SEMITONES = {INTERVALS[k]: k+1 for k in range(len(INTERVALS))}

    start_freq, octaves = 261.63, 3
    NOTE_NAMES = ["C", "Db", "D", "Eb", "E",
                  "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    PITCHES = [
        f"{NOTE_NAMES[i%len(NOTE_NAMES)]}{(i//len(NOTE_NAMES))+4}" for i in range((len(NOTE_NAMES)*octaves)+1)]
    FREQUENCY_DICT = dict(
        zip(PITCHES, [int(start_freq*(2**(i/12))) for i in range(len(PITCHES))]))

    window, canvas, screen = setup_window()

    OPTIONS = dict(
        HOME_NOTE_VARIABLE=StringVar(value="C"),
        EXERCISE_LENGTH=StringVar(value="7"),
        PLAYBACK_SPEED=StringVar(value="1"),
        ALLOW_REPETITIONS=IntVar(value=0),
        SHOW_GUIDELINES=IntVar(value=1),
        SIMULTANEOUS_PLAYBACK=IntVar(value=0),
        INTERVALS_ACTIVATED={interval: IntVar(
            value=1) for interval in INTERVALS}
    )
    turt = create_new_turtle(canvas)
    window.mainloop()
